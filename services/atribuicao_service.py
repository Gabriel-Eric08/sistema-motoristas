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
        """
        Método auxiliar para montar a mensagem e disparar para o ntfy.
        """
        try:
            # Formatação de Datas e Horas para ficar bonito na mensagem
            data_fmt = viagem.data_viagem.strftime('%d/%m/%Y')
            
            # Tratamento caso os horários sejam None
            hora_partida = viagem.horario_estimado_partida.strftime('%H:%M') if viagem.horario_estimado_partida else "--:--"
            hora_volta = viagem.horario_estimado_volta.strftime('%H:%M') if viagem.horario_estimado_volta else "--:--"
            
            # Data/Hora atual da atribuição
            agora = datetime.now().strftime('%d/%m/%Y às %H:%M')
            
            # Descrição (se não tiver, coloca vazio)
            descricao = viagem.descricao if viagem.descricao else "Sem observações."

            # Montagem da Mensagem Completa
            mensagem = (
                f"📅 Data: {data_fmt}\n"
                f"📍 Rota: {viagem.local_partida} ➝ {viagem.local_destino}\n"
                f"⏰ Horário: {hora_partida} até {hora_volta}\n"
                f"📝 Obs: {descricao}\n"
                f"----------------\n"
                f"Atribuição realizada em: {agora}"
            )

            # Envio do POST para o ntfy.sh
            # URL: ntfy.sh/<topico_do_usuario>
            requests.post(
                f"https://ntfy.sh/{motorista.topico_ntfy}",
                data=mensagem.encode('utf-8'),
                headers={
                    "Title": f"Nova Viagem: {viagem.titulo} 🚚".encode('utf-8'),
                    "Priority": "high",  # Alta prioridade (pode vibrar/tocar som)
                    "Tags": "car,calendar,warning" # Ícones que aparecem na notificação
                },
                timeout=5 # Timeout curto para não travar o sistema se o ntfy demorar
            )
            print(f"Notificação enviada para {motorista.nome} no tópico {motorista.topico_ntfy}")

        except Exception as e:
            # Se der erro na notificação, APENAS printa o erro. 
            # NÃO faz rollback, pois a viagem já foi salva no banco com sucesso.
            print(f"Erro ao enviar notificação ntfy: {e}")