import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.veiculo import Carro, Moto
from src.controllers.concessionaria import Concessionaria
from src.models.pessoa import Cliente, Funcionario

class TestSistemaConcessionaria(unittest.TestCase):
    
    def setUp(self):
        self.loja = Concessionaria("Loja de Teste")
        
        conexao = self.loja._db.conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM transacoes")
        cursor.execute("DELETE FROM veiculos")
        cursor.execute("DELETE FROM clientes")
        cursor.execute("DELETE FROM funcionarios")
        cursor.execute("DELETE FROM sqlite_sequence")
        conexao.commit()
        conexao.close()
        
        self.carro = Carro("Honda", "Civic", 2022, 100000.0, "Flex")
        self.moto = Moto("Yamaha", "MT-07", 2023, 50000.0)

    def test_polimorfismo_calculo_preco(self):
        """Verifica se o Polimorfismo está calculando os valores corretamente com as novas regras."""
        self.assertAlmostEqual(self.carro.calcular_preco_final(), 105000.0)
        self.assertAlmostEqual(self.moto.calcular_preco_final(), 55000.0)

    def test_interface_alugavel_moto(self):
        """Verifica se a interface Alugavel altera os status corretamente na Moto."""
        self.assertEqual(self.moto.status, "Disponível")
        self.moto.iniciar_aluguel()
        self.assertEqual(self.moto.status, "Alugado")
        self.moto.finalizar_aluguel()
        self.assertEqual(self.moto.status, "Disponível")

    def test_cadastro_veiculo_crud_e_banco(self):
        """Verifica se o CRUD está adicionando na lista e gerando ID no Banco de Dados."""
        tamanho_inicial = len(self.loja.lista_veiculos)
        self.loja.cadastrar_veiculo(self.carro)
        self.loja.cadastrar_veiculo(self.moto)
        self.assertEqual(len(self.loja.lista_veiculos), tamanho_inicial + 2)
        self.assertIsInstance(self.carro._id, int)
        self.assertIsInstance(self.moto._id, int)

    def test_fluxo_completo_venda(self):
        """Testa o fluxo de ponta a ponta: Cadastro de entidades e Registro de Venda."""
        self.loja.cadastrar_veiculo(self.carro)
        self.loja.cadastrar_veiculo(self.moto)
        
        cliente = Cliente("João da Silva", "12345678900", "88999999999")
        self.loja.cadastrar_cliente(cliente)
        
        funcionario = Funcionario("Carlos Vendedor", "09876543211", "88988888888", "Vendedor", 2500.0)
        self.loja.cadastrar_funcionario(funcionario)
        
        sucesso = self.loja.registrar_venda(cliente.id, self.carro.id, funcionario.id)
        
        self.assertTrue(sucesso)
        self.assertEqual(self.carro.status, "Vendido")
        self.assertEqual(len(funcionario.historico_transacoes), 1)
        self.assertEqual(len(cliente.historico_transacoes), 1)
        self.assertAlmostEqual(funcionario.calcular_comissao_total(), 5250.0)

    def test_venda_persistida_no_banco(self):
        """Verifica se a transação de venda é gravada no banco de dados."""
        self.loja.cadastrar_veiculo(self.carro)
        
        cliente = Cliente("Maria Souza", "11122233344", "88977777777")
        self.loja.cadastrar_cliente(cliente)
        
        funcionario = Funcionario("Ana Vendedora", "55566677788", "88966666666", "Vendedor", 3000.0)
        self.loja.cadastrar_funcionario(funcionario)
        
        self.loja.registrar_venda(cliente.id, self.carro.id, funcionario.id)

        # Consulta direta no banco para confirmar persistência
        transacoes = self.loja._db.listar_transacoes()
        self.assertEqual(len(transacoes), 1)
        
        tipo, nome_cliente, modelo_veiculo = transacoes[0][1], transacoes[0][2], transacoes[0][3]
        self.assertEqual(tipo, "Venda")
        self.assertEqual(nome_cliente, "Maria Souza")
        self.assertEqual(modelo_veiculo, "Civic")

    def test_fluxo_completo_aluguel(self):
        """Testa o fluxo de aluguel com persistência no banco."""
        self.loja.cadastrar_veiculo(self.moto)
        
        cliente = Cliente("Pedro Lima", "99988877766", "88955555555")
        self.loja.cadastrar_cliente(cliente)
        
        funcionario = Funcionario("Lucas Atendente", "44433322211", "88944444444", "Atendente", 2000.0)
        self.loja.cadastrar_funcionario(funcionario)
        
        sucesso = self.loja.registrar_aluguel(cliente.id, self.moto.id, funcionario.id, dias=7)
        
        self.assertTrue(sucesso)
        self.assertEqual(self.moto.status, "Alugado")
        
        # Valor total: 7 dias × (50000 × 2%) = 7 × 1000 = 7000.0
        self.assertAlmostEqual(funcionario.calcular_comissao_total(), 350.0)  # 5% de 7000
        
        # Confirma no banco
        transacoes = self.loja._db.listar_transacoes()
        self.assertEqual(len(transacoes), 1)
        self.assertEqual(transacoes[0][1], "Aluguel")

if __name__ == '__main__':
    unittest.main()