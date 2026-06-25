# ConcessioPro 🚗

Sistema de gerenciamento de concessionária e locadora de veículos desenvolvido com foco na aplicação dos pilares da **Programação Orientada a Objetos (POO)** em Python, com persistência em SQLite e interface web conectada via API REST Flask.

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Diagrama UML](#diagrama-uml)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Execução](#instalação-e-execução)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Endpoints da API](#endpoints-da-api)
- [Testes](#testes)
- [Escalabilidade — Serviço de IA](#escalabilidade--serviço-de-ia)
- [Autor](#autor)

---

## Sobre o Projeto

O ConcessioPro é um sistema back-end + front-end que permite:

- Cadastrar e listar **veículos** (Carros e Motos)
- Cadastrar e listar **clientes** e **funcionários**
- Registrar **vendas** e **aluguéis** de veículos
- Visualizar um **dashboard** com resumo da operação em tempo real

Todos os dados são persistidos em um banco **SQLite** local e expostos via **API REST** consumida pelo frontend em HTML/CSS/JS puro.

---

## Diagrama UML

> Diagrama de classes representando toda a arquitetura orientada a objetos do projeto.

![Diagrama UML](/projeto_final_poo_oficial.png)

<!-- 
  Substitua o caminho acima pela imagem exportada do draw.io ou mermaid.live.
  Sugestão de pasta: docs/diagrama_uml.png
-->

---

## Arquitetura

O projeto segue uma arquitetura em camadas:

```
┌─────────────────────────────────┐
│        Frontend (HTML/JS)       │  ← views/templates/concessionaria.html
├─────────────────────────────────┤
│         API REST (Flask)        │  ← api.py
├─────────────────────────────────┤
│      Controllers / Services     │  ← src/controllers/
├─────────────────────────────────┤
│         Models (POO)            │  ← src/models/
├─────────────────────────────────┤
│         SQLite (Banco)          │  ← data/concessionaria.db
└─────────────────────────────────┘
```

**Pilares de POO aplicados:**

| Pilar | Onde aparece no projeto |
|---|---|
| **Abstração** | Classes `Veiculo`, `Pessoa`, `Transacao` (ABC) |
| **Herança** | `Carro` e `Moto` herdam de `Veiculo` |
| **Polimorfismo** | `calcular_preco_final()` com regras diferentes por tipo |
| **Encapsulamento** | Atributos privados com `_` e acesso via `@property` |
| **Composição** | `Concessionaria` possui `DatabaseManager`; `Transacao` possui `Cliente`, `Veiculo` e `Funcionario` |
| **Interface/Mixin** | `Alugavel` (ABC) implementado por `Carro` e `Moto` |

---

## Tecnologias

- **Python 3.12**
- **Flask** — API REST
- **Flask-CORS** — liberação de requisições cross-origin
- **SQLite3** — banco de dados relacional embutido
- **HTML / CSS / JavaScript** — frontend sem frameworks
- **pytest** — testes automatizados
- **unittest.mock** — mocks para testes de serviços externos

---

## Pré-requisitos

- Python 3.10 ou superior
- pip

---

## Instalação e Execução

```bash
# 1. Clone o repositório
git clone https://github.com/hiurysousa/Projeto-Final-POO.git
cd concessionaria

# 2. Crie e ative o ambiente virtual
python -m venv .venv

# Windows
.\.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode a API
python api.py
```

Acesse em: [http://localhost:5000](http://localhost:5000)

---

## Estrutura de Pastas

```
concessiopro/
│
├── api.py                          # Camada REST (Flask)
├── requirements.txt
│
├── src/
│   ├── models/
│   │   ├── veiculo.py              # Veiculo (ABC), Carro, Moto, Alugavel
│   │   ├── pessoa.py               # Pessoa (ABC), Cliente, Funcionario
│   │   └── transacao.py            # Transacao (ABC), Venda, Aluguel
│   │
│   ├── controllers/
│   │   ├── concessionaria.py       # Orquestrador do CRUD
│   │   └── database.py             # DatabaseManager (SQLite)
│   │
│   └── services/
│       └── ia_service.py           # IAConcessionariaService (LLM)
│
├── views/
│   └── templates/
│       └── concessionaria.html     # Frontend completo
│
├── tests/
│   └── test_sistema.py             # Testes automatizados (unittest)
│
├── data/
│   └── concessionaria.db           # Banco SQLite (gerado automaticamente)
│
└── docs/
    └── diagrama_uml.png            # Diagrama de classes exportado
```

---

## Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/api/dashboard` | Resumo geral da operação |
| `GET` | `/api/veiculos` | Lista todos os veículos |
| `POST` | `/api/veiculos` | Cadastra um novo veículo |
| `GET` | `/api/clientes` | Lista todos os clientes |
| `POST` | `/api/clientes` | Cadastra um novo cliente |
| `GET` | `/api/funcionarios` | Lista todos os funcionários |
| `POST` | `/api/funcionarios` | Cadastra um novo funcionário |
| `GET` | `/api/transacoes` | Lista todas as transações |
| `POST` | `/api/transacoes/venda` | Registra uma venda |
| `POST` | `/api/transacoes/aluguel` | Registra um aluguel |

**Exemplo de payload para cadastro de veículo:**
```json
{
  "tipo": "Carro",
  "marca": "Toyota",
  "modelo": "Corolla",
  "ano": 2023,
  "preco_base": 120000,
  "tipo_combustivel": "Flex"
}
```

---

## Testes

```bash
# Rode todos os testes
pytest tests/

# Com detalhes
pytest tests/ -v
```

Os testes cobrem:
- Polimorfismo no cálculo de preço final
- Interface `Alugavel` e mudança de status
- CRUD completo com persistência no banco
- Fluxo de ponta a ponta: cadastro → venda → comissão

---

## Escalabilidade — Serviço de IA

> 🚧 **Tópico de escalabilidade futura**

O projeto já conta com a estrutura da classe `IAConcessionariaService` em `src/services/ia_service.py`, projetada para receber injeção de dependência de qualquer cliente LLM (Groq, OpenAI, Gemini).

O serviço lê a frota disponível diretamente do banco de dados e monta um prompt contextualizado para recomendar o veículo ideal com base na necessidade descrita pelo cliente em linguagem natural:

```python
service = IAConcessionariaService(cliente_llm=groq_client)
recomendacao = service.recomendar_veiculo(
    necessidade="Preciso de um carro econômico para rodar bastante na estrada",
    concessionaria=minha_loja
)
```

**Fluxo previsto:**

```
Cliente descreve necessidade
        ↓
IAConcessionariaService lê frota disponível no banco
        ↓
Monta prompt com contexto real da concessionária
        ↓
Envia para LLM (Groq / OpenAI / Gemini)
        ↓
Retorna recomendação personalizada em linguagem natural
```

Para ativar, basta configurar a variável de ambiente da API escolhida e injetar o cliente na instância do serviço. A arquitetura já está preparada para isso sem nenhuma mudança estrutural no restante do projeto.

---

## Autor

Desenvolvido por **Hiury** — IFCE, Disciplina de Programação Orientada a Objetos, 2026.