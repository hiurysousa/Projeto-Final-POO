from src.controllers.concessionaria import Concessionaria 

class IAConcessionariaService:
    """Camada de Serviço isolada para interações com Inteligência Artificial[cite: 95]."""
    def __init__(self, cliente_llm_configurado):
        # Aqui você receberia o objeto de conexão da biblioteca de LLM escolhida
        self._llm = cliente_llm_configurado 

    def recomendar_veiculo(self, necessidade_cliente: str, concessionaria: Concessionaria) -> str:
        """
        Lê a frota atual da concessionária, envia para a LLM junto com o perfil de uso
        informado pelo cliente e retorna as sugestões formatadas[cite: 81, 83, 84].
        """
        # Extrai as informações em formato puramente textual da frota ativa 
        frota_disponivel = [v.converter_para_texto() for v in concessionaria.lista_veiculos if v.status == "Disponível"]
        
        if not frota_disponivel:
            return "No momento, não temos veículos disponíveis no pátio para recomendação."

        # Montagem do contexto textual estruturado para a IA
        contexto_frota = "\n".join(frota_disponivel)
        
        prompt = f"""
        Você é um consultor automotivo especialista e inteligente da nossa Concessionária.
        
        Frota de Veículos Disponíveis Atualmente:
        {contexto_frota}
        
        Pedido/Necessidade do Cliente: 
        "{necessidade_cliente}"
        
        Com base APENAS na nossa frota disponível acima, filtre os melhores modelos que se encaixam no perfil do cliente. 
        Justifique de forma amigável a sua escolha baseando-se nos atributos técnicos fornecidos (como ano, espaço/portas, preço ou cilindrada).
        """
        
        # Exemplo simulado de envio para o modelo (Substitua pela chamada real da API da LLM)
        # response = self._llm.generate(prompt)
        # return response.text
        
        return f"[Simulação da LLM] Prompt enviado com sucesso contendo {len(frota_disponivel)} veículos cadastrados no CRUD."