import streamlit as st
import pandas as pd
import random

def atualizarDF():
    # Esta função será chamada quando a tabela for alterada
    qtd_jogadores = len(st.session_state.df_tabela)
    lista_jogadores = st.session_state.df_tabela.values.tolist()
    return qtd_jogadores, lista_jogadores

st.set_page_config(page_title='Gerador de Times', page_icon='icone-fut.png')
st.title('Gerador de Times')

# Variáveis
qtd_jogadores = 0   
lista_jogadores = []

# Campo para indicar a quantidade de jogadores por time
qtd_por_time = st.number_input('Quantidade de jogadores por time:', min_value=1, step=1)

st.markdown("##### QUADRO DOS JOGADORES") 

columns = ["JOGADORES","CAPITÃO"]

# Inicializa o dataframe vazio se não estiver no estado da sessão
if 'df_tabela' not in st.session_state:
    st.session_state.df_tabela = pd.DataFrame(columns=columns)

# Editor de dados
df_tabela = st.data_editor(
    st.session_state.df_tabela, 
    column_config={
        "CAPITÃO": st.column_config.CheckboxColumn(
            default=False,
        )
    }, 
    hide_index=True,
    num_rows='dynamic', 
    use_container_width=True,
    on_change=atualizarDF
)

def generate_teams(df_tabela, qtd_por_time):
    teams = []
    lista_jogadores = df_tabela.values.tolist()
    random.shuffle(lista_jogadores)
    captains = [jogador[0] for jogador in lista_jogadores if jogador[1] == True] # Lista de capitães
    n_teams = len(lista_jogadores)//max(1, qtd_por_time)  # Evita a divisão por zero
    lista_jogadores = [jogador for jogador in lista_jogadores if jogador[1] == False] # Remove os capitães da lista de jogadores
    
    for i in range(n_teams):
        team = []
        for j in range(qtd_por_time - 1):  # Adiciona jogadores ao time (quantidade por time - 1)
            if lista_jogadores:
                player = lista_jogadores.pop(0)[0]
                team.append(player)
            else:
                break
        if captains:  # Adiciona um capitão ao final do time
            team.append(captains.pop(0) + " (Capitão)")
        teams.append(team)
    
    return teams

# Botão para gerar times
btn_gerar = st.button('Gerar Times')
if btn_gerar:
    st.markdown("#### TIMES GERADOS")
    teams = generate_teams(df_tabela, qtd_por_time)

    # Determinar o número de colunas a serem criadas (um por time)
    num_teams = len(teams)
    columns = st.columns(num_teams)

    # Adicionar os times às colunas
    for idx, team in enumerate(teams, start=1):
        with columns[idx - 1]:
            st.markdown("##### TIME {0}".format(idx))
            for player in team:
                st.write(player)
