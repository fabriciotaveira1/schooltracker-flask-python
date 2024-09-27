-- Criação da tabela Usuario
CREATE TABLE Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

-- Criação da tabela Viagem
CREATE TABLE Viagem (
    id_viagem INT AUTO_INCREMENT PRIMARY KEY,
    data_inicio DATE NOT NULL,
    localizacao VARCHAR(100) NOT NULL,
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

-- Criação da tabela Registro
CREATE TABLE Registro (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    id_viagem INT NOT NULL,
    id_usuario INT NOT NULL,  -- Adicionando a coluna para a chave estrangeira
    data_hora_registro DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Adicionando a coluna para data e hora
    cidade VARCHAR(100) NOT NULL,
    observacoes TEXT NOT NULL,
    temperatura DECIMAL(5,2),
    velocidade_do_vento DECIMAL(5,2),
    umidade_do_ar DECIMAL(5,2),
    FOREIGN KEY (id_viagem) REFERENCES Viagem(id_viagem),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)  -- Chave estrangeira para Usuario
);

