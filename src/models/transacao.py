from abc import ABC, abstractmethod
from datetime import datetime
from src.models.veiculo import Alugavel  # Importa a interface que criamos antes

class Transacao(ABC):
    """Classe Abstrata que define o esqueleto de qualquer operação financeira."""
    _total_transacoes = 0

    def __init__(self, cliente, veiculo, funcionario):
        Transacao._total_transacoes += 1
        self._id = Transacao._total_transacoes
        self._cliente = cliente          # Composição: objeto Cliente
        self._veiculo = veiculo          # Composição: objeto Veiculo
        self._funcionario = funcionario  # Composição: objeto Funcionario
        self._data = datetime.now()

    @property
    def id(self): return self._id
    @property
    def veiculo(self): return self._veiculo

    @abstractmethod
    def calcular_valor_total(self) -> float:
        """Método abstrato para o cálculo financeiro polimórfica."""
        pass


class Venda(Transacao):
    """Subclasse para vendas diretas."""
    def __init__(self, cliente, veiculo, funcionario):
        super().__init__(cliente, veiculo, funcionario)
        # Ao vender, o status do veículo muda automaticamente no CRUD
        self._veiculo.status = "Vendido" 

    def calcular_valor_total(self) -> float:
        # Puxa o preço final polimórfico calculado pelo próprio veículo
        return self._veiculo.calcular_preco_final()


class Aluguel(Transacao):
    """Subclasse para locações por período que gerencia o contrato Alugavel."""
    def __init__(self, cliente, veiculo, funcionario, dias_locacao: int):
        super().__init__(cliente, veiculo, funcionario)
        self._dias = dias_locacao
        self._valor_diaria = veiculo.preco_base * 0.02 # Define a diária como 2% do valor do carro
        
        # Se o veículo aceitar aluguel (assinar a interface), ativa o método correspondente
        if isinstance(self._veiculo, Alugavel):
            self._veiculo.iniciar_aluguel()

    def calcular_valor_total(self) -> float:
        return self._dias * self._valor_diaria

    def encerrar_locacao(self):
        """Finaliza o fluxo devolvendo o veículo para o pátio disponível."""
        if isinstance(self._veiculo, Alugavel):
            self._veiculo.finalizar_aluguel()