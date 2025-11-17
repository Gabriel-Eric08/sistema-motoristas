from models.models import Motorista, db

class MotoristaRepository:
    def get_all(self):
        admins = Motorista.query.all()
        return admins # <-- CORRIGIDO (faltava 'return' no seu código original)
    
    # ATUALIZADO: Adicionado 'ativo'
    def create(self, nome, email, telefone, topico_ntfy, ativo):
        novo_motorista = Motorista(
            nome=nome,
            email=email,
            telefone=telefone,
            topico_ntfy=topico_ntfy,
            ativo=ativo # <-- ADICIONADO AO MODELO
        )
        db.session.add(novo_motorista)
        db.session.flush()
        return True
    
    def validate(self, nome, senha_hash):
        # ... (sua função de validação, se houver) ...
        admin = Motorista.query.filter_by(nome=nome,senha_hash=senha_hash).first()
        if admin:
            return True
        return False