from repositories.atribuicao_repository import AtribuicaoRepository
from models.models import db, Viagem  # Importar o model 'Viagem'
# 'datetime' não é mais necessário aqui

class AtribuicaoService:
    def __init__(self):
        self.repo = AtribuicaoRepository()

    # A rota envia id_admin_criador, então podemos recebê-lo,
    # mesmo que não o usemos diretamente para *criar* a atribuição.
    def create(self, id_motorista, id_viagem, id_admin_criador):
        
        # Validação simples
        if not id_motorista or not id_viagem:
            print("Erro: ID do motorista ou da viagem está faltando.")
            return False
        
        # --- Lógica de 'horario' e 'status' removida daqui ---
        # (Não pertence mais à Atribuição)

        try:
            # 1. (NOVO) Buscar a Viagem que será atualizada
            viagem = Viagem.query.get(id_viagem)
            if not viagem:
                print(f"Erro: Viagem com ID {id_viagem} não encontrada.")
                return False
            
            # 2. Criar a Atribuição (a ligação)
            # Chamada corrigida: só passa os 2 IDs
            create = self.repo.create(id_motorista, id_viagem)
            
            if not create:
                # O repositório falhou (provavelmente motorista já atribuído)
                db.session.rollback()
                print("Erro: O repositório de atribuição falhou (motorista já pode estar atribuído).")
                return False

            # 3. (NOVO) Atualizar o status da Viagem
            viagem.status = 'Atribuída'
            db.session.add(viagem) # Adiciona a mudança da viagem à sessão

            # 4. Commitar as duas mudanças (Atribuição E Viagem)
            db.session.commit()
            return True
            
        except Exception as e:
            # Pega erros como "UNIQUE constraint failed" (motorista já atribuído)
            print(f"Erro no AtribuicaoService: {e}")
            db.session.rollback()
            return False