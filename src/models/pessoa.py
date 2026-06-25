from abc import ABC

class Pessoa(ABC):
    """Classe Abstrata para as entidades humanas do sistema."""
    def __init__(self, nome: str, cpf: str, telefone: str):
        if len(cpf) != 11:
            raise ValueError(f'CPF precisa ter obrigatoriamente 11 dígitos.')
        self._id = None  # Começa vazio, mas será preenchido pelo Banco de Dados
        self._nome = nome
        self._cpf = cpf
        self._telefone = telefone

    # Adicione este Getter para o ID
    @property
    def id(self): return self._id

    @property
    def nome(self): return self._nome



class Cliente(Pessoa):
    def __init__(self, nome: str, cpf: str, telefone: str):
        super().__init__(nome, cpf, telefone)
        self.historico_transacoes = []


class Funcionario(Pessoa):
    def __init__(self, nome: str, cpf: str, telefone: str, cargo: str, salario: float):
        super().__init__(nome, cpf, telefone)
        self._cargo = cargo
        self._salario = salario
        # Composição: Lista que guardará objetos do tipo Venda ou Aluguel
        self._historico_transacoes = []

    @property
    def historico_transacoes(self):
        return self._historico_transacoes

    def adicionar_transacao(self, transacao):
        self._historico_transacoes.append(transacao)

    def calcular_comissao_total(self) -> float:
        """Exemplo de Polimorfismo/Regra de negócio: calcula 5% de cada venda/aluguel."""
        total_comissao = 0.0
        for t in self._historico_transacoes:
            # Chama o método de calcular o valor total de cada transação de forma polimórfica
            total_comissao += t.calcular_valor_total() * 0.05
        return total_comissao