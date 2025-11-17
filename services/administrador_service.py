from repositories.administrador_repository import AdministradorRepository,db
import hashlib

class AdministradorService:
    def __init__(self):
        self.repo=AdministradorRepository()

    def get_all(self):
        admins=self.repo.get_all()
        return admins
    
    def create(self, nome, email, senha_hash):
        if not nome or not email or not senha_hash:
            return False
        senha_em_bytes = senha_hash.encode('utf-8')
        hash_obj = hashlib.sha256(senha_em_bytes)
        hash_hex=hash_obj.hexdigest()

        create = self.repo.create(nome,email,hash_hex)
        if create:
            db.session.commit()
            return True
        return False
    
    def validate(self, nome, senha):
        if not nome or not senha:
            return False
        senha_em_bytes = senha.encode('utf-8')
        hash_obj = hashlib.sha256(senha_em_bytes)
        hash_hex=hash_obj.hexdigest()
        
        validate = self.repo.validate(nome, hash_hex)
        if validate:
            return True
        return False