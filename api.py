"""
api.py  —  Camada de API REST da Concessionária
Rode com:  python api.py
Acesse em: http://localhost:5000
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime
from src.models.veiculo import Carro, Moto
from src.models.pessoa import Cliente, Funcionario

# Importa o DatabaseManager já existente no projeto
# (ajuste o caminho se necessário conforme sua estrutura de pastas)
from src.controllers.database import DatabaseManager

app = Flask(__name__)
CORS(app)  # Permite que o HTML aberto localmente acesse a API

db = DatabaseManager()   # Uma única instância compartilhada por todas as rotas


# ═══════════════════════════════════════════════════════════
#  UTILITÁRIO
# ═══════════════════════════════════════════════════════════

def preco_final(veiculo: dict) -> float:
    """Replica a regra de negócio polimórfica dos modelos Python."""
    if veiculo['tipo'] == 'Carro':
        return veiculo['preco_base'] * 1.05
    return veiculo['preco_base'] * 1.10   # Moto


# ═══════════════════════════════════════════════════════════
#  VEÍCULOS
# ═══════════════════════════════════════════════════════════

@app.route('/api/veiculos', methods=['GET'])
def listar_veiculos():
    veiculos = db.listar_veiculos()
    # Adiciona o preço final calculado em cada registro
    for v in veiculos:
        v['preco_final'] = preco_final(v)
    return jsonify(veiculos)


@app.route('/api/veiculos', methods=['POST'])
def cadastrar_veiculo():
    dados = request.get_json()

    # Valida campos obrigatórios
    campos = ['tipo', 'marca', 'modelo', 'ano', 'preco_base']
    if not all(dados.get(c) for c in campos):
        return jsonify({'erro': 'Campos obrigatórios ausentes'}), 400

    # Usa os modelos POO para manter a lógica centralizada
    tipo = dados['tipo']

    if tipo == 'Carro':
        obj = Carro(
            marca=dados['marca'],
            modelo=dados['modelo'],
            ano=int(dados['ano']),
            preco_base=float(dados['preco_base']),
            tipo_combustivel=dados.get('tipo_combustivel', 'Flex')
        )
    elif tipo == 'Moto':
        obj = Moto(
            marca=dados['marca'],
            modelo=dados['modelo'],
            ano=int(dados['ano']),
            preco_base=float(dados['preco_base'])
        )
    else:
        return jsonify({'erro': 'Tipo de veículo inválido'}), 400

    id_gerado = db.salvar_veiculo(obj)
    return jsonify({'id': id_gerado, 'mensagem': 'Veículo cadastrado com sucesso'}), 201


# ═══════════════════════════════════════════════════════════
#  CLIENTES
# ═══════════════════════════════════════════════════════════

@app.route('/api/clientes', methods=['GET'])
def listar_clientes():
    return jsonify(db.listar_clientes())


@app.route('/api/clientes', methods=['POST'])
def cadastrar_cliente():
    dados = request.get_json()

    campos = ['nome', 'cpf', 'telefone']
    if not all(dados.get(c) for c in campos):
        return jsonify({'erro': 'Campos obrigatórios ausentes'}), 400

    obj = Cliente(
        nome=dados['nome'],
        cpf=dados['cpf'],
        telefone=dados['telefone']
    )

    try:
        id_gerado = db.salvar_cliente(obj)
    except Exception as e:
        # CPF duplicado cai aqui (UNIQUE constraint)
        return jsonify({'erro': 'CPF já cadastrado'}), 409

    return jsonify({'id': id_gerado, 'mensagem': 'Cliente cadastrado com sucesso'}), 201


# ═══════════════════════════════════════════════════════════
#  FUNCIONÁRIOS
# ═══════════════════════════════════════════════════════════

@app.route('/api/funcionarios', methods=['GET'])
def listar_funcionarios():
    return jsonify(db.listar_funcionarios())


@app.route('/api/funcionarios', methods=['POST'])
def cadastrar_funcionario():
    dados = request.get_json()

    campos = ['nome', 'cpf', 'telefone', 'cargo', 'salario']
    if not all(dados.get(c) for c in campos):
        return jsonify({'erro': 'Campos obrigatórios ausentes'}), 400

    obj = Funcionario(
        nome=dados['nome'],
        cpf=dados['cpf'],
        telefone=dados['telefone'],
        cargo=dados['cargo'],
        salario=float(dados['salario'])
    )

    try:
        id_gerado = db.salvar_funcionario(obj)
    except Exception as e:
        return jsonify({'erro': 'CPF já cadastrado'}), 409

    return jsonify({'id': id_gerado, 'mensagem': 'Funcionário cadastrado com sucesso'}), 201


# ═══════════════════════════════════════════════════════════
#  TRANSAÇÕES
# ═══════════════════════════════════════════════════════════

@app.route('/api/transacoes', methods=['GET'])
def listar_transacoes():
    return jsonify(db.listar_transacoes())


@app.route('/api/transacoes/venda', methods=['POST'])
def registrar_venda():
    dados = request.get_json()

    campos = ['veiculo_id', 'cliente_id', 'funcionario_id']
    if not all(dados.get(c) for c in campos):
        return jsonify({'erro': 'Campos obrigatórios ausentes'}), 400

    veiculo = db.buscar_veiculo_por_id(int(dados['veiculo_id']))
    if not veiculo:
        return jsonify({'erro': 'Veículo não encontrado'}), 404
    if veiculo['status'] != 'Disponível':
        return jsonify({'erro': 'Veículo não está disponível'}), 409

    valor = preco_final(veiculo)
    agora = datetime.now().isoformat()

    # Atualiza status no banco
    db.atualizar_status_veiculo(veiculo['id'], 'Vendido')

    # Salva a transação
    id_transacao = db.salvar_transacao(
        tipo='Venda',
        id_cliente=int(dados['cliente_id']),
        id_veiculo=veiculo['id'],
        id_funcionario=int(dados['funcionario_id']),
        data=agora,
        valor_total=valor
    )

    return jsonify({
        'id': id_transacao,
        'valor_total': valor,
        'mensagem': 'Venda registrada com sucesso'
    }), 201


@app.route('/api/transacoes/aluguel', methods=['POST'])
def registrar_aluguel():
    dados = request.get_json()

    campos = ['veiculo_id', 'cliente_id', 'funcionario_id', 'dias']
    if not all(dados.get(c) for c in campos):
        return jsonify({'erro': 'Campos obrigatórios ausentes'}), 400

    veiculo = db.buscar_veiculo_por_id(int(dados['veiculo_id']))
    if not veiculo:
        return jsonify({'erro': 'Veículo não encontrado'}), 404
    if veiculo['status'] != 'Disponível':
        return jsonify({'erro': 'Veículo não está disponível'}), 409

    dias = int(dados['dias'])
    diaria = veiculo['preco_base'] * 0.02
    valor_total = dias * diaria
    agora = datetime.now().isoformat()

    db.atualizar_status_veiculo(veiculo['id'], 'Alugado')

    id_transacao = db.salvar_transacao(
        tipo='Aluguel',
        id_cliente=int(dados['cliente_id']),
        id_veiculo=veiculo['id'],
        id_funcionario=int(dados['funcionario_id']),
        data=agora,
        valor_total=valor_total,
        dias_locacao=dias,
        valor_diaria=diaria
    )

    return jsonify({
        'id': id_transacao,
        'valor_diaria': diaria,
        'valor_total': valor_total,
        'mensagem': 'Aluguel registrado com sucesso'
    }), 201


# ═══════════════════════════════════════════════════════════
#  DASHBOARD  (agrega tudo em uma única chamada)
# ═══════════════════════════════════════════════════════════

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    veiculos     = db.listar_veiculos()
    clientes     = db.listar_clientes()
    funcionarios = db.listar_funcionarios()
    transacoes   = db.listar_transacoes()

    disponiveis = sum(1 for v in veiculos if v['status'] == 'Disponível')
    vendidos    = sum(1 for v in veiculos if v['status'] == 'Vendido')
    alugados    = sum(1 for v in veiculos if v['status'] == 'Alugado')

    return jsonify({
        'total_veiculos':     len(veiculos),
        'disponiveis':        disponiveis,
        'vendidos':           vendidos,
        'alugados':           alugados,
        'total_clientes':     len(clientes),
        'total_funcionarios': len(funcionarios),
        'total_transacoes':   len(transacoes),
    })

@app.route('/')
def frontend():
    return send_from_directory('src/views/templates', 'concessionaria.html')

# ═══════════════════════════════════════════════════════════
#  INICIALIZAÇÃO
# ═══════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("✅ API da Concessionária rodando em http://localhost:5000")
    app.run(debug=True, port=5000)