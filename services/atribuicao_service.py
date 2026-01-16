import requests # Necessário instalar: pip install requests
from datetime import datetime
from repositories.atribuicao_repository import AtribuicaoRepository
from models.models import db, Viagem, Motorista # Importamos Motorista também

class AtribuicaoService:
    def __init__(self):
        self.repo = AtribuicaoRepository()

    def create(self, id_motorista, id_viagem, id_admin_criador):
        
        # 1. Validação básica
        if not id_motorista or not id_viagem:
            print("Erro: ID do motorista ou da viagem está faltando.")
            return False
        
        try:
            # 2. Buscar a Viagem
            viagem = Viagem.query.get(id_viagem)
            if not viagem:
                print(f"Erro: Viagem {id_viagem} não encontrada.")
                return False

            # 3. Buscar o Motorista (Necessário para pegar o tópico ntfy)
            motorista = Motorista.query.get(id_motorista)
            if not motorista:
                print(f"Erro: Motorista {id_motorista} não encontrado.")
                return False

            # 4. Tentar criar a Atribuição no Repositório
            create = self.repo.create(id_motorista, id_viagem)
            
            if not create:
                db.session.rollback()
                print("Erro: Repositório falhou (provável duplicação).")
                return False

            # 5. Atualizar Status da Viagem
            viagem.status = 'Atribuída'
            db.session.add(viagem)

            # 6. Salvar tudo no Banco
            db.session.commit()

            # ========================================================
            # 7. ENVIO DA NOTIFICAÇÃO (Após o commit ser bem sucedido)
            # ========================================================
            if motorista.topico_ntfy:
                self._enviar_notificacao_ntfy(motorista, viagem)
            
            return True
            
        except Exception as e:
            print(f"Erro no AtribuicaoService: {e}")
            db.session.rollback()
            return False

    def _enviar_notificacao_ntfy(self, motorista, viagem):
        try:
            data_fmt = viagem.data_viagem.strftime('%d/%m/%Y')
            hora_partida = viagem.horario_estimado_partida.strftime('%H:%M') if viagem.horario_estimado_partida else "--:--"
            
            # Tratamento visual para distância e tempo
            dist = f"{viagem.distancia_km} km" if viagem.distancia_km else "N/A"
            tempo = f"{viagem.tempo_estimado} min" if viagem.tempo_estimado else "N/A"
            
            descricao = viagem.descricao if viagem.descricao else "Sem observações."

            # --- MENSAGEM COM NOVOS DADOS ---
            mensagem = (
                f"📅 Data: {data_fmt} às {hora_partida}\n"
                f"📍 Rota: {viagem.local_partida} ➝ {viagem.local_destino}\n"
                f"⛽ Info: {dist} | ⏱️ {tempo}\n"  # <--- NOVA LINHA
                f"📝 Obs: {descricao}"
            )

            requests.post(
                f"https://ntfy.sh/{motorista.topico_ntfy}",
                data=mensagem.encode('utf-8'),
                headers={
                    "Title": f"Nova Viagem: {viagem.titulo} 🚚".encode('utf-8'),
                    "Priority": "high",
                    "Tags": "car,map"
                },
                timeout=5
            )
            print(f"Notificação enviada para {motorista.nome}")

        except Exception as e:
            print(f"Erro ao enviar notificação ntfy: {e}")