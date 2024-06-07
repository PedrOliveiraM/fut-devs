import streamlit as st
import pandas as pd
import random

def atualizarDF():
    # Esta função será chamada quando a tabela for alterada
    qtd_jogadores = len(st.session_state.df_tabela)
    lista_jogadores = st.session_state.df_tabela.values.tolist()
    return qtd_jogadores, lista_jogadores

st.set_page_config(page_title='Gerador de Times', page_icon='icone-fut.png')
st.image('./background.png', width=700)
st.title('Gerador de Times')

# Inicializa o dataframe vazio se não estiver no estado da sessão
if 'df_tabela' not in st.session_state:
    st.session_state.df_tabela = pd.DataFrame(columns=["JOGADORES", "CAPITÃO"])

st.markdown("##### LISTA DE PARTICIPANTES")

txt = st.text_area("Lista dos jogadores")

if st.button('Adicionar Jogadores'):
    lista_jogadores = txt.split("\n")
    lista_jogadores = [jogador for jogador in lista_jogadores if jogador.strip() != ""]  # Remove entradas vazias
    df_tabela = pd.DataFrame([[jogador, False] for jogador in lista_jogadores], columns=["JOGADORES", "CAPITÃO"])
    st.session_state.df_tabela = df_tabela

st.markdown("##### QUADRO DOS JOGADORES")

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
    captains = [jogador[0] for jogador in lista_jogadores if jogador[1]]  # Lista de capitães
    lista_jogadores = [jogador[0] for jogador in lista_jogadores if not jogador[1]]  # Remove os capitães da lista de jogadores
    
    n_teams = max(1, (len(captains) + len(lista_jogadores)) // qtd_por_time)  # Número de times

    for i in range(n_teams):
        team = []
        if captains:  # Adiciona um capitão ao time se disponível
            team.append(captains.pop(0) + " (Capitão)")
        
        for j in range(qtd_por_time - 1):  # Adiciona jogadores ao time (quantidade por time - 1)
            if lista_jogadores:
                team.append(lista_jogadores.pop(0))
            else:
                break
        
        teams.append(team)

    return teams

qtd_por_time = st.number_input('Quantidade de jogadores por time:', min_value=1, step=1)

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
