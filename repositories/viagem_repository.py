from models.models import Viagem, Atribuicao, db 
from datetime import time, datetime, date

class ViagemRepository:
    def get_all(self):
        viagens = Viagem.query.order_by(Viagem.data_viagem.desc()).all()
        return viagens
    
    # --- CORREÇÃO AQUI ---
    # Renomeei os argumentos para bater com o que o Service envia
    def create(self, titulo, descricao, local_partida, local_destino, 
               distancia_km, tempo_estimado, 
               horario_estimado_partida,  # Antes era h_partida
               horario_estimado_volta,    # Antes era h_volta
               data_viagem, 
               id_admin_criador):         # Antes era id_admin
        
        nova_viagem = Viagem(
            titulo=titulo,
            descricao=descricao,
            local_partida=local_partida,
            local_destino=local_destino,
            
            distancia_km=distancia_km,
            tempo_estimado=tempo_estimado,
            
            # Agora as variáveis têm o mesmo nome
            horario_estimado_partida=horario_estimado_partida,
            horario_estimado_volta=horario_estimado_volta,
            
            data_viagem=data_viagem,
            id_admin_criador=id_admin_criador, 
            status='Pendente'
        )
        db.session.add(nova_viagem)
        db.session.flush() 
        return True
    
    def concluir(self, id_viagem):
        viagem = Viagem.query.filter_by(id=id_viagem).first()
        if viagem:
            viagem.status='Concluída'
            db.session.add(viagem)
            db.session.flush() 
            return True
        return False 

    def existing(self, id_viagem):
        viagem = Viagem.query.filter_by(id=id_viagem).first()
        if not viagem:
            return False
        return True

    def get_by_motorista(self, id_motorista):
        return (db.session.query(Viagem)
                .join(Atribuicao, Atribuicao.id_viagem == Viagem.id)
                .filter(Atribuicao.id_motorista == id_motorista)
                .all())

    def get_by_id(self, id_viagem):
        return Viagem.query.get(id_viagem)

    def search(self, status=None, id_motorista=None, data_inicio=None, data_fim=None):
        query = db.session.query(Viagem)

        if status:
            query = query.filter(Viagem.status == status)

        if id_motorista:
            query = query.join(Atribuicao, Atribuicao.id_viagem == Viagem.id)\
                         .filter(Atribuicao.id_motorista == id_motorista)

        if data_inicio:
            query = query.filter(Viagem.data_viagem >= data_inicio)

        if data_fim:
            query = query.filter(Viagem.data_viagem <= data_fim)

        return query.order_by(Viagem.data_viagem.desc()).all()