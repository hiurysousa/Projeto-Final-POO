from src.models.veiculo import Carro, Moto, Veiculo
from src.models.pessoa import Cliente, Funcionario
from src.models.transacao import Venda, Aluguel
from src.controllers.database import DatabaseManager  # <-- Importando nosso Banco de Dados

class Concessionaria:
    """Classe responsável por gerenciar as coleções e o Banco de Dados."""
    def __init__(self, nome: str):
        self._nome = nome
        self._db = DatabaseManager()  # <-- Instanciando a conexão com o banco
        
        # Mantemos as listas em memória (Composição) para consultas rápidas
        self._lista_veiculos = [] 
        self._lista_clientes = [] 
        self._lista_funcionarios = [] 

    @property
    def lista_veiculos(self):
        return self._lista_veiculos

    # --- CRUD VEÍCULOS --- 
    def cadastrar_veiculo(self, veiculo: Veiculo):
        # 1. Salva no Banco de Dados (Persistência)
        id_gerado = self._db.salvar_veiculo(veiculo)
        
        # 2. Atualiza o ID do objeto na memória com o ID real gerado pelo SQLite
        veiculo._id = id_gerado
        
        # 3. Adiciona à lista em memória (Composição)
        self._lista_veiculos.append(veiculo)
        print(f"Veículo {veiculo.modelo} cadastrado no Banco com sucesso (ID: {id_gerado})!")

    def listar_veiculos(self):
        return [v.converter_para_texto() for v in self._lista_veiculos]

    def buscar_veiculo_por_id(self, id_veiculo: int):
        return next((v for v in self._lista_veiculos if v.id == id_veiculo), None)

    def atualizar_veiculo(self, id_veiculo: int, novo_preco: float):
        veiculo = self.buscar_veiculo_por_id(id_veiculo)
        if veiculo:
            veiculo._preco_base = novo_preco
            # No futuro, podemos adicionar um self._db.atualizar_preco_veiculo(id_veiculo, novo_preco) aqui
            return True
        return False

    def remover_veiculo(self, id_veiculo: int):
        veiculo = self.buscar_veiculo_por_id(id_veiculo)
        if veiculo:
            self._lista_veiculos.remove(veiculo)
            # No futuro, podemos adicionar um self._db.deletar_veiculo(id_veiculo) aqui
            return True
        return False
    
    # --- CRUD PESSOAS ---
    def cadastrar_cliente(self, cliente: Cliente):
        id_gerado = self._db.salvar_cliente(cliente)
        cliente._id = id_gerado
        self._lista_clientes.append(cliente)
        print(f"Cliente {cliente.nome} cadastrado com ID {id_gerado}!")

    def cadastrar_funcionario(self, funcionario: Funcionario):
        id_gerado = self._db.salvar_funcionario(funcionario)
        funcionario._id = id_gerado
        self._lista_funcionarios.append(funcionario)
        print(f"Funcionário {funcionario.nome} cadastrado com ID {id_gerado}!")

    # --- TRANSAÇÕES ---
    def registrar_venda(self, id_cliente: int, id_veiculo: int, id_funcionario: int):
        # Busca os objetos nas listas em memória
        cliente = next((c for c in self._lista_clientes if c._id == id_cliente), None)
        veiculo = self.buscar_veiculo_por_id(id_veiculo)
        funcionario = next((f for f in self._lista_funcionarios if f._id == id_funcionario), None)
        
        if cliente and veiculo and funcionario and veiculo.status == "Disponível":
            # Instancia a nova venda passando as composições
            nova_venda = Venda(cliente, veiculo, funcionario)
            
            # Alimenta os históricos de forma cruzada
            cliente.historico_transacoes.append(nova_venda)
            funcionario.adicionar_transacao(nova_venda)
            
            # Persiste a transação e sincroniza o status do veículo no banco
            id_transacao = self._db.salvar_transacao(nova_venda)
            nova_venda._id = id_transacao
            self._db.atualizar_status_veiculo(veiculo._id, veiculo.status)

            return True
        return False

    def registrar_aluguel(self, id_cliente: int, id_veiculo: int, id_funcionario: int, dias: int):
        cliente = next((c for c in self._lista_clientes if c._id == id_cliente), None)
        veiculo = self.buscar_veiculo_por_id(id_veiculo)
        funcionario = next((f for f in self._lista_funcionarios if f._id == id_funcionario), None)

        if cliente and veiculo and funcionario and veiculo.status == "Disponível":
            novo_aluguel = Aluguel(cliente, veiculo, funcionario, dias)

            cliente.historico_transacoes.append(novo_aluguel)
            funcionario.adicionar_transacao(novo_aluguel)

            id_transacao = self._db.salvar_transacao(novo_aluguel)
            novo_aluguel._id = id_transacao
            self._db.atualizar_status_veiculo(veiculo._id, veiculo.status)

            return True
        return False