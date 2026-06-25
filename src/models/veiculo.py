from abc import ABC, abstractmethod

class Veiculo(ABC):
    """Classe Abstrata que serve como base para todos os veículos."""

    def __init__(self, marca: str, modelo: str, ano: int, preco_base: float):
        # _id começa como None; será preenchido pelo banco após o INSERT
        self._id = None
        self._marca = marca
        self._modelo = modelo
        self._ano = ano
        self._preco_base = preco_base
        self._status = "Disponível"

    @property
    def id(self): 
        return self._id

    @property
    def marca(self): 
        return self._marca

    @property
    def modelo(self): 
        return self._modelo

    @property
    def ano(self): 
        return self._ano

    @property
    def preco_base(self): 
        return self._preco_base

    @property
    def status(self): 
        return self._status

    @status.setter
    def status(self, novo_status: str):
        self._status = novo_status

    @abstractmethod
    def calcular_preco_final(self) -> float:
        pass

    @abstractmethod
    def converter_para_texto(self) -> str:
        pass


class Alugavel(ABC):
    """Interface (via ABC) que define as regras para itens locáveis."""

    @abstractmethod
    def iniciar_aluguel(self) -> None:
        pass

    @abstractmethod
    def finalizar_aluguel(self) -> None:
        pass


class Carro(Veiculo, Alugavel):
    def __init__(self, marca: str, modelo: str, ano: int, preco_base: float, tipo_combustivel: str):
        super().__init__(marca, modelo, ano, preco_base)
        self._tipo_combustivel = tipo_combustivel

    def calcular_preco_final(self) -> float:
        return self._preco_base * 1.05

    def iniciar_aluguel(self):
        self.status = "Alugado"

    def finalizar_aluguel(self):
        self.status = "Disponível"

    def converter_para_texto(self) -> str:
        return f"ID: {self.id} | Carro: {self.marca} {self.modelo} ({self.ano}) | Status: {self.status}"


class Moto(Veiculo, Alugavel):
    def __init__(self, marca: str, modelo: str, ano: int, preco_base: float):
        super().__init__(marca, modelo, ano, preco_base)

    def calcular_preco_final(self) -> float:
        return self._preco_base * 1.10

    def iniciar_aluguel(self):
        self.status = "Alugado"

    def finalizar_aluguel(self):
        self.status = "Disponível"

    def converter_para_texto(self) -> str:
        return f"ID: {self.id} | Moto: {self.marca} {self.modelo} ({self.ano}) | Preço Base: R${self.preco_base:.2f} | Status: {self.status}"