DROP TABLE IF EXISTS usuarios;
CREATE TABLE usuarios (
cod_usuario integer PRIMARY KEY AUTOINCREMENT,
nome VARCHAR(255),
Senha VARCHAR(255),
data_criada DATETIME,
data_modificada DATETIME,
admin INTEGER,
obs VARCHAR(255));

DROP TABLE IF EXISTS clientes;
CREATE TABLE clientes (
cod_clientes INTEGER PRIMARY KEY,
cod_usuario INTEGER,
nome VARCHAR(255) UNIQUE NOT NULL,
contactos VARCHAR(255),
email VARCHAR(255),
endereco VARCHAR(255),
nuit VARCHAR(255),
web VARCHAR(255),
data_criada DATETIME,
data_modificada DATETIME,
obs VARCHAR(255),
CONSTRAINT usuario FOREIGN KEY (cod_usuario) REFERENCES usuarios (cod_usuario));

DROP TABLE IF EXISTS produtos;
CREATE TABLE produtos (
cod_produto integer PRIMARY KEY AUTOINCREMENT,
cod_usuario INTEGER,
nome VARCHAR(255) UNIQUE NOT NULL,
preco REAL,
preco1 REAL,
preco2 REAL,
preco3 REAL,
preco4 REAL,
quantidade REAL,
quantidade_minima REAL,
validade DATETIME,
data_criada DATETIME,
data_modificada DATETIME,
unidade VARCHAR(255),
Obs VARCHAR(255),
CONSTRAINT usuario FOREIGN KEY (cod_usuario) REFERENCES usuarios (cod_usuario));

DROP TABLE IF EXISTS fornecedores;
CREATE TABLE fornecedores (
cod_fornecedor integer PRIMARY KEY AUTOINCREMENT,
cod_usuario INTEGER,
nome VARCHAR(255) UNIQUE NOT NULL,
contactos VARCHAR(255),
email VARCHAR(255),
endereco VARCHAR(255),
nuit VARCHAR(255),
web VARCHAR(255),
data_criada DATETIME,
data_modificada DATETIME,
obs VARCHAR(255),
CONSTRAINT usuario FOREIGN KEY (cod_usuario) REFERENCES usuarios (cod_usuario));

DROP TABLE IF EXISTS turnos;
CREATE TABLE turnos (
cod_turno integer PRIMARY KEY AUTOINCREMENT,
nome VARCHAR UNIQUE NOT NULL,
cod_usuario integer,
CONSTRAINT usuario FOREIGN KEY (cod_usuario) REFERENCES usuarios (cod_usuario));

DROP TABLE IF EXISTS caixa;
CREATE TABLE caixa (
cod_caixa integer PRIMARY KEY AUTOINCREMENT,
data_abertura DATETIME,
data_feixo DATETIME,
user_abertura VARCHAR,
user_fecho VARCHAR,
subtotal REAL,
taxa REAL,
total REAL;

DROP TABLE IF EXISTS taxas;
CREATE TABLE taxas(
cod_taxas INTEGER PRIMARY KEY AUTOINCREMENT,
nome VARCHAR UNIQUE NOT NULL,
valor REAL
);

DROP TABLE IF EXISTS stock;
CREATE TABLE stock (
cod_stock integer PRIMARY KEY AUTOINCREMENT,
cod_produto
Nome VARCHAR(255),
Quantidade REAL,
Venda REAL,
Obs VARCHAR(50),
Compra REAL,
Datas DATETIME,
Hora DATETIME,
Func VARCHAR(255),
Empresa VARCHAR(255),
Doc VARCHAR(255),
ID INTEGER,
Tipo VARCHAR(255),
Total REAL,
IVA REAL,
minima REAL,
nota VARCHAR(255));

DROP TABLE IF EXISTS vendas;
CREATE TABLE vendas(
cod_vendas INTEGER PRIMARY KEY AUTOINCREMENT,
cod_clientes INTEGER,
cod_usuario INTEGER,
data DATETIME,
Valor REAL,
taxa REAL,
Total REAL,
Desconto REAL,
cash REAL,
banco REAL,
cheque,
moeda VARCHAR,
extenso TEXT);

DROP TABLE IF EXISTS vendasdetalhe;
CREATE TABLE vendas(
cod integer PRIMARY KEY AUTOINCREMENT,
cod_vendas INTEGER,
cod_produto INTEGER,
preco REAL,
quantidade REAL,
subtotal REAL
taxa REAL,
desconto REAL,
total REAL,
CONSTRAINT venda FOREIGN KEY (cod_vendas) REFERENCES vendas (cod_vendas),
CONSTRAINT produto FOREIGN KEY (cod_produto) REFERENCES produtos (cod_produto));

DROP TABLE IF EXISTS USERS;
CREATE TABLE USERS(
cod TEXT NOT NULL PRIMARY KEY;
senha VARCHAR(50),
senha2 VARCHAR(50),
nome VARCHAR(50),
endereco VARCHAR(255),
sexo VARCHAR(10),
email VARCHAR(100),
nascimento DATE,
contacto VARCHAR(255)
tipo VARCHAR(50),
numero VARCHAR(20)
nacionalidade VARCHAR(50)
obs TEXT,
created DATE,
modified DATE,
modified_by VARCHAR(50),
created_by VARCHAR(50),
estado BOOLEAN
)
