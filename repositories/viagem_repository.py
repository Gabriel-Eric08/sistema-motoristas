from models.models import Viagem, db
from datetime import time, datetime, date # Importar 'date'

class ViagemRepository:
    def get_all(self):
        # --- CORRIGIDO ---
        # Ordenar pelo novo campo 'data_viagem'
        viagens = Viagem.query.order_by(Viagem.data_viagem.desc()).all()
        return viagens
    
    # --- CORRIGIDO ---
    # Trocado 'data_hora_inicio' por 'data_viagem'
    def create(self, titulo, descricao, local_partida, local_destino, 
                   h_partida, h_volta, data_viagem, id_admin):
        
        nova_viagem = Viagem(
            titulo=titulo,
            descricao=descricao,
            local_partida=local_partida,
            local_destino=local_destino,
            horario_estimado_partida=h_partida,
            horario_estimado_volta=h_volta,
            
            # --- CAMPO CORRIGIDO ---
            data_viagem=data_viagem,     # O objeto 'date'
            id_admin_criador=id_admin, 
            status='Pendente'
        )
        db.session.add(nova_viagem)
        # O flush() aqui é opcional, 
        # mas pode ser útil se você precisar do ID da nova_viagem logo em seguida
        db.session.flush() 
        return True