import sqlite3
import os

class DatabaseManager:
    """Classe responsável por gerenciar a persistência de dados no SQLite."""

    def __init__(self, db_path="data/concessionaria.db"):
        self._db_path = db_path
        self._garantir_pasta_existe()
        self.criar_tabelas()

    def _garantir_pasta_existe(self):
        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)

    def conectar(self):
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row   # permite acessar colunas pelo nome
        return conn

    def criar_tabelas(self):
        conexao = self.conectar()
        cursor = conexao.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS veiculos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                ano INTEGER NOT NULL,
                preco_base REAL NOT NULL,
                status TEXT NOT NULL,
                tipo_combustivel TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                telefone TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS funcionarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                telefone TEXT NOT NULL,
                cargo TEXT NOT NULL,
                salario REAL NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_transacao TEXT NOT NULL,
                id_cliente INTEGER NOT NULL,
                id_veiculo INTEGER NOT NULL,
                id_funcionario INTEGER NOT NULL,
                data_transacao TEXT NOT NULL,
                dias_locacao INTEGER,
                valor_diaria REAL,
                valor_total REAL NOT NULL,
                FOREIGN KEY(id_cliente) REFERENCES clientes(id),
                FOREIGN KEY(id_veiculo) REFERENCES veiculos(id),
                FOREIGN KEY(id_funcionario) REFERENCES funcionarios(id)
            )
        ''')

        conexao.commit()
        conexao.close()

    # ── ESCRITA ──────────────────────────────────────────────────────────────

    def salvar_veiculo(self, veiculo) -> int:
        conexao = self.conectar()
        cursor = conexao.cursor()
        tipo_combustivel = getattr(veiculo, '_tipo_combustivel', None)
        cursor.execute('''
            INSERT INTO veiculos (tipo, marca, modelo, ano, preco_base, status, tipo_combustivel)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (veiculo.__class__.__name__, veiculo.marca, veiculo.modelo,
              veiculo.ano, veiculo.preco_base, veiculo.status, tipo_combustivel))
        id_gerado = cursor.lastrowid
        conexao.commit()
        conexao.close()
        return id_gerado

    def salvar_cliente(self, cliente) -> int:
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute(
            'INSERT INTO clientes (nome, cpf, telefone) VALUES (?, ?, ?)',
            (cliente.nome, cliente._cpf, cliente._telefone)
        )
        id_gerado = cursor.lastrowid
        conexao.commit()
        conexao.close()
        return id_gerado

    def salvar_funcionario(self, funcionario) -> int:
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute(
            'INSERT INTO funcionarios (nome, cpf, telefone, cargo, salario) VALUES (?, ?, ?, ?, ?)',
            (funcionario.nome, funcionario._cpf, funcionario._telefone,
             funcionario._cargo, funcionario._salario)
        )
        id_gerado = cursor.lastrowid
        conexao.commit()
        conexao.close()
        return id_gerado

    def salvar_transacao(self, tipo: str, id_cliente: int, id_veiculo: int,
                         id_funcionario: int, data: str, valor_total: float,
                         dias_locacao: int = None, valor_diaria: float = None) -> int:
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute('''
            INSERT INTO transacoes
                (tipo_transacao, id_cliente, id_veiculo, id_funcionario,
                 data_transacao, dias_locacao, valor_diaria, valor_total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (tipo, id_cliente, id_veiculo, id_funcionario,
              data, dias_locacao, valor_diaria, valor_total))
        id_gerado = cursor.lastrowid
        conexao.commit()
        conexao.close()
        return id_gerado

    def atualizar_status_veiculo(self, id_veiculo: int, novo_status: str):
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute(
            'UPDATE veiculos SET status = ? WHERE id = ?',
            (novo_status, id_veiculo)
        )
        conexao.commit()
        conexao.close()

    # ── LEITURA ──────────────────────────────────────────────────────────────

    def listar_veiculos(self) -> list:
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM veiculos ORDER BY id')
        rows = [dict(row) for row in cursor.fetchall()]
        conexao.close()
        return rows

    def listar_clientes(self) -> list:
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM clientes ORDER BY id')
        rows = [dict(row) for row in cursor.fetchall()]
        conexao.close()
        return rows

    def listar_funcionarios(self) -> list:
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM funcionarios ORDER BY id')
        rows = [dict(row) for row in cursor.fetchall()]
        conexao.close()
        return rows

    def listar_transacoes(self) -> list:
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM transacoes ORDER BY id')
        rows = [dict(row) for row in cursor.fetchall()]
        conexao.close()
        return rows

    def buscar_veiculo_por_id(self, id_veiculo: int) -> dict:
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM veiculos WHERE id = ?', (id_veiculo,))
        row = cursor.fetchone()
        conexao.close()
        return dict(row) if row else None