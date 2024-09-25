CREATE TABLE usuarios (
    id_usuario INT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    senha VARCHAR(255)
);

CREATE TABLE viagens (
    id_viagem INT PRIMARY KEY,
    data_inicio DATE,
    localizacao VARCHAR(255)
);

CREATE TABLE registros (
    id_registro INT PRIMARY KEY,
    id_viagem INT,
    data_registro DATE,
    condicoes_climaticas VARCHAR(255),
    observacoes TEXT,
    FOREIGN KEY (id_viagem) REFERENCES viagens(id_viagem)
);