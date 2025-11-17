from models.models import Atribuicao, db

class AtribuicaoRepository:
    
    # Corrigido: O método create SÓ precisa dos IDs de ligação.
    # Os outros campos (status, admin) não existem neste model.
    def create(self, id_motorista, id_viagem):
        try:
            nova_atribuicao = Atribuicao(
                id_motorista=id_motorista,
                id_viagem=id_viagem
                # Removidos: id_admin_criador, data_hora_inicio, status
            )
            db.session.add(nova_atribuicao)
            # db.session.flush() # O flush é opcional aqui, o commit é no service
            return True
        except Exception as e:
            # Isso vai pegar erros de "UNIQUE constraint" (atribuição duplicada)
            print(f"Erro no AtribuicaoRepository: {e}")
            return False