from repositories.viagem_repository import ViagemRepository
from models.models import db
from datetime import datetime, time # Não precisamos mais de 'time' aqui, mas mantendo

class ViagemService:
    def __init__(self):
        self.repo = ViagemRepository()

    def get_all(self):
        return self.repo.get_all()
    
    # --- CORRIGIDO ---
    # 1. Trocado 'data_hora_inicio_str' por 'data_viagem_str'
    def create(self, titulo, descricao, local_partida, local_destino, 
                   h_partida_str, h_volta_str, data_viagem_str):
        
        # 2. Validação atualizada
        if not titulo or not data_viagem_str:
            print("Erro de validação: Título ou Data da Viagem faltando.")
            return False

        # 3. Conversão de todas as strings de data/hora
        try:
            # --- MUDANÇA NA CONVERSÃO ---
            # Converte a string "AAAA-MM-DD" para um objeto 'date'
            data_viagem_obj = datetime.strptime(data_viagem_str, '%Y-%m-%d').date()
            
            # Conversão dos horários (continua igual)
            h_partida_obj = datetime.strptime(h_partida_str, '%H:%M').time() if h_partida_str else None
            h_volta_obj = datetime.strptime(h_volta_str, '%H:%M').time() if h_volta_str else None
            
        except ValueError as e:
            print(f"Erro de conversão de data/hora: {e}")
            return False

        # 4. Adicionado 'id_admin' (provisoriamente)
        #    (Você deve trocar '1' pelo ID do admin logado)
        id_admin = 1 
        
        # 5. Chamada correta ao repositório com 8 argumentos
        create = self.repo.create(
            titulo, descricao, local_partida, local_destino,
            h_partida_obj, h_volta_obj, 
            data_viagem_obj, # Passando o objeto 'date'
            id_admin
        )
        
        if create:
            db.session.commit()
            return True
        return False