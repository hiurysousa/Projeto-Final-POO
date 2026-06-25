# Arquivo: main.py
import os
from google import genai  # Exemplo usando a biblioteca oficial do Gemini
from src.controllers.concessionaria import Concessionaria
from src.services.ia_service import IAConcessionariaService

# 1. O sistema lê a chave direto do ambiente de forma segura
CHAVE_IA = os.environ.get("GEMINI_API_KEY")

# 2. Configura e cria o cliente da IA
cliente_gemini = genai.Client(api_key=CHAVE_IA)

# 3. Instancia as classes do seu sistema
minha_loja = Concessionaria("Dev Motors")
servico_ia = IAConcessionariaService(cliente_gemini) # <--- INJEÇÃO DE DEPENDÊNCIA

# Agora o sistema está pronto para rodar junto com a interface!