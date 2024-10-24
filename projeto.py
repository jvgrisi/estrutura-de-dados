import streamlit as st
import heapq
import networkx as nx
import matplotlib.pyplot as plt

# Definindo o grafo com bairros de João Pessoa e distâncias em minutos
graph = {
    'Tambaú': {'Manaíra': 5, 'Cabo Branco': 7, 'Centro': 12},
    'Manaíra': {'Tambaú': 5, 'Bessa': 10, 'Brisamar': 8},
    'Bessa': {'Manaíra': 10, 'Aeroclube': 7},
    'Cabo Branco': {'Tambaú': 7, 'Altiplano': 5},
    'Altiplano': {'Cabo Branco': 5, 'Miramar': 10},
    'Miramar': {'Altiplano': 10, 'Torre': 7},
    'Torre': {'Miramar': 7, 'Jaguaribe': 6, 'Centro': 10},
    'Centro': {'Tambaú': 12, 'Torre': 10, 'Jaguaribe': 8},
    'Jaguaribe': {'Centro': 8, 'Torre': 6, 'Cristo Redentor': 12},
    'Cristo Redentor': {'Jaguaribe': 12, 'Bancários': 10},
    'Bancários': {'Cristo Redentor': 10, 'Mangabeira': 7},
    'Mangabeira': {'Bancários': 7, 'Valentina': 12},
    'Valentina': {'Mangabeira': 12},
    'Brisamar': {'Manaíra': 8, 'Aeroclube': 5}, 
    'Aeroclube': {'Bessa': 7, 'Brisamar': 5}   
}


# Função de Dijkstra adaptada para o Streamlit
def dijkstra(graph, origem, destino):
    # Inicializa as distâncias como infinito para todos os bairros
    distancias = {bairro: float('inf') for bairro in graph}
    distancias[origem] = 0
    
    # 'Anteriores' guardam tanto o bairro anterior quanto o custo associado
    anteriores = {bairro: (None, None) for bairro in graph}
    fila_prioridade = [(0, origem)]  # Fila de prioridade inicializada com a origem

    while fila_prioridade:
        distancia_atual, bairro_atual = heapq.heappop(fila_prioridade)

        # Se chegamos ao destino, reconstruímos o caminho
        if bairro_atual == destino:
            caminho_bairros = []
            while bairro_atual:
                caminho_bairros.append(bairro_atual)
                bairro_atual, _ = anteriores[bairro_atual]
            return caminho_bairros[::-1], distancias[destino]  # Retorna o caminho e a distância total

        # Explora os vizinhos (bairros conectados)
        for vizinho, custo in graph[bairro_atual].items():
            nova_distancia = distancia_atual + custo
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                anteriores[vizinho] = (bairro_atual, custo)  # Salva o bairro anterior e o custo
                heapq.heappush(fila_prioridade, (nova_distancia, vizinho))

    return None, float('inf')  # Retorna None se não houver caminho

def plot_grafo(graph, caminho):
    G = nx.Graph()

    # Adiciona as arestas do grafo
    for bairro in graph:
        for vizinho, peso in graph[bairro].items():
            G.add_edge(bairro, vizinho, weight=peso)

    pos = nx.spring_layout(G)  # Layout para o grafo

    # Desenhar todos os nós e arestas
    nx.draw(G, pos, with_labels=True, node_size=50, node_color='lightblue', font_size=5, font_weight='bold')

    # Destacar o caminho mais curto
    caminho_edges = [(caminho[i], caminho[i+1]) for i in range(len(caminho)-1)]
    nx.draw_networkx_edges(G, pos, edgelist=caminho_edges, width=4, edge_color='r')

    # Mostrar pesos nas arestas
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Exibir o gráfico
    plt.show()

# Função principal do Streamlit
def main():
    st.set_page_config(page_title='Navegação', page_icon='🧭', layout='wide')
    
    st.title("Rotador de Navegação - Bairros de João Pessoa 🧭")

    # Interface para selecionar bairros
    origem = st.selectbox("Selecione o bairro de partida", list(graph.keys()))
    destino = st.selectbox("Selecione o bairro de destino", list(graph.keys()))

    if st.button("Calcular caminho mais curto"):
        # Executando o algoritmo de Dijkstra
        caminho, distancia_total = dijkstra(graph, origem, destino)

        # Mostrando o resultado
        if caminho:
            st.success(f"O caminho mais curto de {origem} até {destino} é: {' -> '.join(caminho)}")
            st.info(f"Distância total: {distancia_total} minutos")

            # Plotar o grafo com o caminho mais curto
            fig, ax = plt.subplots()
            plot_grafo(graph, caminho)
            st.pyplot(fig)
        else:
            st.error(f"Não há caminho entre {origem} e {destino}")

# Executar o app
if __name__ == '__main__':
    main()
