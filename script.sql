PRAGMA foreign_keys = ON;

CREATE TABLE motorista (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    topico_ntfy VARCHAR(100) UNIQUE,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE administrador (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL
);

/*
 * Tabela VIAGEM (O EVENTO)
 * Contém a DATA da viagem (tipo DATE), mas NÃO o motorista.
*/
CREATE TABLE viagem (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Campos da Viagem
    titulo VARCHAR(100) NOT NULL,
    descricao TEXT,
    local_partida VARCHAR(200),
    local_destino VARCHAR(200),
    
    -- NOVAS COLUNAS --
    distancia_km FLOAT,          -- Ex: 12.5
    tempo_estimado VARCHAR(50),  -- Ex: "45" ou "45 min"
    -------------------

    horario_estimado_partida TIME,
    horario_estimado_volta TIME,
    
    -- Campo de Data
    data_viagem DATE NOT NULL,
    
    status VARCHAR(50) DEFAULT 'Pendente', 
    
    id_admin_criador INTEGER,
    FOREIGN KEY (id_admin_criador) REFERENCES administrador (id)
);

/*
 * Tabela ATRIBUICAO (A LIGAÇÃO)
 * Liga um Motorista a uma Viagem.
*/
CREATE TABLE atribuicao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Correção de "NOTNULL" para "NOT NULL"
    id_motorista INTEGER NOT NULL,
    
    id_viagem INTEGER NOT NULL,
    
    FOREIGN KEY (id_motorista) REFERENCES motorista (id) ON DELETE CASCADE,
    FOREIGN KEY (id_viagem) REFERENCES viagem (id) ON DELETE CASCADE,
    
    -- Garante que um motorista não seja atribuído à mesma viagem duas vezes
    UNIQUE(id_motorista, id_viagem) 
);