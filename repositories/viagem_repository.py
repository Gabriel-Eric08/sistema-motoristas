from models.models import Viagem, Atribuicao, db # <--- Adicione Atribuicao aqui
from datetime import time, datetime, date

class ViagemRepository:
    def get_all(self):
        viagens = Viagem.query.order_by(Viagem.data_viagem.desc()).all()
        return viagens
    
    def create(self, titulo, descricao, local_partida, local_destino, 
                   h_partida, h_volta, data_viagem, id_admin):
        
        nova_viagem = Viagem(
            titulo=titulo,
            descricao=descricao,
            local_partida=local_partida,
            local_destino=local_destino,
            horario_estimado_partida=h_partida,
            horario_estimado_volta=h_volta,
            data_viagem=data_viagem,
            id_admin_criador=id_admin, 
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
        return False # Boa prática retornar False se não achar

    def existing(self, id_viagem):
        viagem = Viagem.query.filter_by(id=id_viagem).first()
        if not viagem:
            return False
        return True

    # --- NOVO MÉTODO PARA CORRIGIR O ERRO ---
    def get_by_motorista(self, id_motorista):
        """
        Busca todas as viagens associadas a um motorista específico.
        Faz um JOIN entre a tabela Viagem e a tabela Atribuicao.
        """
        return (db.session.query(Viagem)
                .join(Atribuicao, Atribuicao.id_viagem == Viagem.id)
                .filter(Atribuicao.id_motorista == id_motorista)
                .all())
    def get_by_id(self, id_viagem):
        """Busca a viagem pelo ID, trazendo relacionamentos se necessário."""
        # O SQLAlchemy já carrega relacionamentos lazy por padrão, 
        # mas se der erro, pode precisar de .options(joinedload(Viagem.atribuicoes))
        return Viagem.query.get(id_viagem)
    def search(self, status=None, id_motorista=None, data_inicio=None, data_fim=None):
        """
        Filtra viagens baseadas em múltiplos critérios opcionais.
        """
        query = db.session.query(Viagem)

        # 1. Filtro por Status
        if status:
            query = query.filter(Viagem.status == status)

        # 2. Filtro por Motorista (Exige JOIN com Atribuicao)
        if id_motorista:
            query = query.join(Atribuicao, Atribuicao.id_viagem == Viagem.id)\
                         .filter(Atribuicao.id_motorista == id_motorista)

        # 3. Filtro por Data Inicial (Maior ou igual)
        if data_inicio:
            query = query.filter(Viagem.data_viagem >= data_inicio)

        # 4. Filtro por Data Final (Menor ou igual)
        if data_fim:
            query = query.filter(Viagem.data_viagem <= data_fim)

        # Ordenar por data (mais recentes primeiro)
        return query.order_by(Viagem.data_viagem.desc()).all()