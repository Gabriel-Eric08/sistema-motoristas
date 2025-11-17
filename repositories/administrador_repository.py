from models.models import Administrador,db

class AdministradorRepository:
    def get_all(self):
        admins=Administrador.query.all()
        return admins
    
    def create(self, nome, email, senha_hash):
        novo_admin=Administrador(
            nome=nome,
            email=email,
            senha_hash=senha_hash
        )
        db.session.add(novo_admin)
        db.session.flush()
        return True
    
    def validate(self, nome, senha_hash):
        admin = Administrador.query.filter_by(nome=nome,senha_hash=senha_hash).first()
        if admin:
            return True
        return False