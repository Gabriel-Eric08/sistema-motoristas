from db_config import db
from datetime import datetime

# --- Modelos Motorista e Administrador (Sem alterações) ---

class Motorista(db.Model):
    __tablename__ = 'motorista'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    topico_ntfy = db.Column(db.String(100), unique=True, nullable=True)
    ativo = db.Column(db.Boolean, default=True)

    # Relação: Um motorista pode ter várias atribuições
    atribuicoes = db.relationship('Atribuicao', backref='motorista', lazy=True)

class Administrador(db.Model):
    __tablename__ = 'administrador'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)

    # Relação: Um admin pode criar várias viagens
    viagens_criadas = db.relationship('Viagem', backref='criador', lazy=True)


# --- Modelo Viagem (CORRIGIDO) ---

class Viagem(db.Model):
    """
    Tabela CORRIGIDA.
    Esta é a tabela do "Evento" ou "Agendamento".
    Ela contém a DATA (separada), STATUS e quem a criou.
    """
    __tablename__ = 'viagem'
    id = db.Column(db.Integer, primary_key=True)
    
    # Detalhes da viagem
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    local_partida = db.Column(db.String(200))
    local_destino = db.Column(db.String(200))
    horario_estimado_partida = db.Column(db.Time, nullable=True)
    horario_estimado_volta = db.Column(db.Time, nullable=True)

    # ==================================================
    # MUDANÇA AQUI: 'data_hora_inicio' (DateTime) virou 'data_viagem' (Date)
    # ==================================================
    data_viagem = db.Column(db.Date, nullable=False)
    # ==================================================

    status = db.Column(db.String(50), default='Pendente') # Pendente, Atribuída, etc.
    id_admin_criador = db.Column(db.Integer, db.ForeignKey('administrador.id'), nullable=True)


    # Relação: Uma Viagem (evento) pode ter um ou mais motoristas atribuídos
    atribuicoes = db.relationship('Atribuicao', backref='viagem', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Viagem {self.id} - {self.titulo}>'


# --- Modelo Atribuicao (Sem alterações) ---

class Atribuicao(db.Model):
    """
    Tabela de "Ligação".
    Ela apenas liga um Motorista a uma Viagem.
    """
    __tablename__ = 'atribuicao'
    id = db.Column(db.Integer, primary_key=True)
    
    id_motorista = db.Column(db.Integer, db.ForeignKey('motorista.id', ondelete='CASCADE'), nullable=False)
    id_viagem = db.Column(db.Integer, db.ForeignKey('viagem.id', ondelete='CASCADE'), nullable=False)
    
    # Garante que um motorista não possa ser atribuído à mesma viagem duas vezes
    __table_args__ = (db.UniqueConstraint('id_motorista', 'id_viagem', name='_motorista_viagem_uc'),)

    def __repr__(self):
        return f"Atribuição {self.id} (Motorista: {self.id_motorista} -> Viagem: {self.id_viagem})"