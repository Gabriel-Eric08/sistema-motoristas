# Importe o 'db' do seu db_config ou models, dependendo da sua estrutura
# Ex: from models.models import db 
# ou from db_config import db
from repositories.motorista_repository import MotoristaRepository
from models.models import db # Ajuste esta importação se necessário

class MotoristaService:
    def __init__(self):
        self.repo = MotoristaRepository()

    def get_all(self):
        """ Adicionado para alimentar a tabela na página """
        return self.repo.get_all()
    
    # ATUALIZADO: Adicionado 'ativo'
    def create(self, nome, telefone, email, topico_ntfy, ativo):
        
        # A validação principal já foi feita na rota
        if not nome or not email or not telefone or not topico_ntfy:
            return False
        
        # 'ativo' é um booleano (true/false) vindo do JSON
        
        create = self.repo.create(
            nome=nome, 
            email=email, 
            telefone=telefone, 
            topico_ntfy=topico_ntfy, 
            ativo=ativo # <-- REPASSADO
        )
        
        if create:
            db.session.commit()
            return True
        return False