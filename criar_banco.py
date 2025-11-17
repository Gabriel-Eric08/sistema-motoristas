import sqlite3

# Nome do arquivo do banco de dados
NOME_BANCO = "database.db"
# Nome do arquivo SQL a ser executado
NOME_ARQUIVO_SQL = "script.sql"

def criar_banco():
    conn = None # Inicializa a conexão como None
    try:
        # --- 1. Ler o script SQL do arquivo ---
        print(f"Lendo o script de '{NOME_ARQUIVO_SQL}'...")
        with open(NOME_ARQUIVO_SQL, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{NOME_ARQUIVO_SQL}' não foi encontrado.")
        print("Por favor, crie o arquivo com o código SQL na mesma pasta.")
        return
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo SQL: {e}")
        return

    try:
        # --- 2. Conectar ao banco e executar o script ---
        print(f"Conectando ao banco de dados '{NOME_BANCO}'...")
        conn = sqlite3.connect(NOME_BANCO)
        cursor = conn.cursor()
        
        print("Executando o script SQL...")
        # 'executescript' permite rodar múltiplos comandos SQL de uma vez
        cursor.executescript(sql_script)
        
        # Salva as mudanças
        conn.commit()
        print(f"Banco de dados '{NOME_BANCO}' criado/atualizado com sucesso.")
        print("Tabelas: motorista, administrador, viagem, atribuicao.")

    except sqlite3.Error as e:
        print(f"Ocorreu um erro ao executar o script SQL no banco: {e}")
    
    finally:
        # Fecha a conexão
        if conn:
            print("Fechando conexão com o banco.")
            conn.close()

if __name__ == "__main__":
    criar_banco()