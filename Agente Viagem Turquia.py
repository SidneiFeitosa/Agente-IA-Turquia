from datetime import date
import textwrap
from IPython.display import Markdown
from vertexai.generative_models import Agent, Runner, types
from vertexai.generative_models import GenerativeModel, Tool

# Supondo que você já configurou o acesso ao Vertex AI e importou as ferramentas necessárias, como `google_search`.
# Se não, você precisará adicionar essa configuração.

# --- Agente 1: Buscador de Destinos Turcos --- #
def agente_buscador_turquia(data_de_hoje):
    buscador = Agent(
        name="agente_buscador_turquia",
        model="gemini-2.0-flash",
        instruction=f"""
        Você é um especialista em viagens para a Turquia. Sua tarefa é usar a ferramenta de busca do Google (google_search)
        para identificar os 5 destinos mais interessantes e populares na Turquia para visitar na época de maio de 2025.
        Considere a relevância turística, a infraestrutura para turistas e possíveis eventos ou festivais que possam estar acontecendo.
        Apresente brevemente cada destino e o porquê de sua relevância.
        """,
        description="Agente que busca os melhores destinos na Turquia.",
        tools=[google_search]
    )
    entrada_do_agente_buscador = f"Melhores destinos turísticos para visitar em maio de 2025."
    destinos = call_agent(buscador, entrada_do_agente_buscador)
    return destinos

# --- Agente 2: Planejador de Roteiro --- #
def agente_planejador_roteiro(destinos_buscados):
    planejador = Agent(
        name="agente_planejador_roteiro",
        model="gemini-2.0-flash",
        instruction=f"""
        Você é um planejador de roteiros de viagem experiente. Com base nos seguintes destinos turísticos:
        {destinos_buscados}
        Crie um roteiro sugerido de 7 a 10 dias, considerando o deslocamento lógico entre eles.
        Sugira a duração ideal da estadia em cada local e mencione uma ou duas atividades imperdíveis em cada um.
        """,
        description="Agente que planeja um roteiro de viagem pela Turquia.",
        tools=[] # Este agente pode não precisar de ferramentas externas inicialmente
    )
    entrada_do_agente_planejador = f"Destinos na Turquia: {destinos_buscados}"
    roteiro = call_agent(planejador, entrada_do_agente_planejador)
    return roteiro

# --- Agente 3: Detalhador de Experiências --- #
def agente_detalhador_experiencias(roteiro_sugerido):
    detalhador = Agent(
        name="agente_detalhador_experiencias",
        model="gemini-2.5-pro-preview-03-25",
        instruction=f"""
        Você é um especialista em experiências de viagem. Com base no seguinte roteiro pela Turquia:
        {roteiro_sugerido}
        Para cada destino mencionado, use a ferramenta de busca do Google (google_search) para encontrar:
        - Pelo menos 3 atrações imperdíveis com informações relevantes.
        - Uma sugestão de restaurante com culinária local.
        - Uma dica cultural importante para os viajantes.
        """,
        description="Agente que detalha as experiências em cada destino.",
        tools=[google_search]
    )
    entrada_do_agente_detalhador = f"Roteiro de viagem na Turquia: {roteiro_sugerido}"
    detalhes = call_agent(detalhador, entrada_do_agente_detalhador)
    return detalhes

# --- Agente 4: Revisor de Viagem --- #
def agente_revisor_viagem(roteiro_detalhado):
    revisor = Agent(
        name="agente_revisor_viagem",
        model="gemini-2.5-pro-preview-03-25",
        instruction=f"""
        Você é um revisor de planos de viagem. Analise o seguinte plano de viagem para a Turquia:
        {roteiro_detalhado}
        Verifique se o roteiro é lógico, se as sugestões são relevantes e se há alguma informação faltando
        que seria importante para um viajante.
        Se o plano estiver bom, responda apenas 'O plano de viagem está ótimo!'.
        Caso haja problemas ou sugestões de melhoria, aponte-os de forma clara e concisa.
        """,
        description="Agente que revisa o plano de viagem.",
        tools=[] # Este agente pode não precisar de ferramentas externas inicialmente
    )
    entrada_do_agente_revisor = f"Plano de viagem para a Turquia: {roteiro_detalhado}"
    revisao = call_agent(revisor, entrada_do_agente_revisor)
    return revisao

data_de_hoje = date.today().strftime("%d/%m/%Y")

print("✈️ Iniciando o Planejamento da sua Viagem para a Turquia com 4 Agentes 🇹🇷")

# --- Definir o Tópico da Viagem ---
topico_viagem = "Viagem para a Turquia"

# --- Lógica do sistema de agentes para a viagem ---
print(f"Maravilha! Vamos planejar sua viagem para a Turquia.")

destinos_turisticos = agente_buscador_turquia(data_de_hoje)
print("\n--- 🌍 Resultado do Agente 1 (Buscador de Destinos) ---\n")
display(to_markdown(destinos_turisticos))
print("--------------------------------------------------------------")

roteiro_sugerido = agente_planejador_roteiro(destinos_turisticos)
print("\n--- 🗺️ Resultado do Agente 2 (Planejador de Roteiro) ---\n")
display(to_markdown(roteiro_sugerido))
print("--------------------------------------------------------------")

detalhes_experiencias = agente_detalhador_experiencias(roteiro_sugerido)
print("\n--- 💡 Resultado do Agente 3 (Detalhador de Experiências) ---\n")
display(to_markdown(detalhes_experiencias))
print("--------------------------------------------------------------")

plano_final_viagem = agente_revisor_viagem(detalhes_experiencias)
print("\n--- ✅ Resultado do Agente 4 (Revisor de Viagem) ---\n")
display(to_markdown(plano_final_viagem))
print("--------------------------------------------------------------")

print("\n🎉 Seu plano de viagem para a Turquia está pronto! 🎉")