import streamlit as st
from math import atan
from math import degrees
from math import sin
from math import cos
from math import radians

def m_p_g(mil):
    grau = mil * 0.05625
    return radians(grau)


# conversor de graus em milésimos:
def grau_p_mils(g):
    return (g * 160) / 9

# tangente do rumo AB
def tang(e, n):
    return e / n

# Função para encontrar alcance peça alvo
def encontrar_alcance(delta_e, delta_n):
    alcance = ((delta_e ** 2) + (delta_n ** 2)) ** (1/2)
    return alcance

# Função para encontrar o lançamento/azimute topo da lançadora para o alvo.
def azimute_topo(eco_alvo, eco_lanc, delta_e, delta_n):
    if delta_n == 0:
        if eco_alvo > eco_lanc:
            azimute_topo_mils = 1600
        if eco_alvo < eco_lanc:
            azimute_topo_mils = 4800
        if eco_alvo - eco_lanc == 0:
            azimute_topo_mils = 0
        return azimute_topo_mils
    # 1º Quadrante
    if delta_e >= 0 and delta_n >= 0:
        azimute_topo_graus = degrees(atan(tang(delta_e, delta_n)))
        azimute_topo_mils = grau_p_mils(azimute_topo_graus)
        return azimute_topo_mils
    # 2º Quadrante
    if delta_e >= 0 and delta_n <= 0:
        azimute_topo_graus = 180 - abs(degrees(atan(tang(delta_e, delta_n))))
        azimute_topo_mils = grau_p_mils(azimute_topo_graus)
        return azimute_topo_mils
    # 3º Quadrante
    if delta_e <= 0 and delta_n <= 0:
        azimute_topo_graus = abs(degrees(atan(tang(delta_e, delta_n)))) + 180
        azimute_topo_mils = grau_p_mils(azimute_topo_graus)
        return azimute_topo_mils
    # 4º Quadrante
    if delta_e <= 0 and delta_n >= 0:
        azimute_topo_graus = 360 - abs(degrees(atan(tang(delta_e, delta_n))))
        azimute_topo_mils = grau_p_mils(azimute_topo_graus)
        return azimute_topo_mils






# Add a selectbox to the sidebar:
st.sidebar.title('Menu')
paginaSelecionada = st.sidebar.selectbox(
    'Qual cálculo deseja realizar?',
    ('Lançamento e distância', 'Radiamento'))
if paginaSelecionada == 'Lançamento e distância':
    st.title('Lançamento e distância (coordenadas UTM)')
    form = st.form(key='my_form')
    eco_alvo = form.number_input(label='E do Alvo')
    november_alvo = form.number_input(label='N do Alvo')
    eco_lancadora = form.number_input(label='E da Lançadora')
    november_lancadora = form.number_input(label='N da Lançadora')
    delta_eco = eco_alvo - eco_lancadora
    delta_november = november_alvo - november_lancadora
    submit_button = form.form_submit_button(label='Calcular')
    alcance = encontrar_alcance(delta_eco, delta_november)
    az_topo = azimute_topo(eco_alvo, eco_lancadora, delta_eco, delta_november)
    if submit_button:
        st.write(f'O alcance é {int(alcance)} metros. O Azimute Topo é {int(az_topo)} \'\'\'')
if paginaSelecionada == 'Radiamento':
    st.title('Radiamento')
    form = st.form(key='my_form')
    E = form.number_input(label='Informe a coordenada E da Estação:')
    N = form.number_input(label='Informe a coordenada N da Estação:')
    dist = form.number_input(label='Informe a distância para o ponto desconhecido (metros):')
    lan = form.number_input(label='Informe o Lançamento em milésimos para o ponto desconhecido:')
    submit_button = form.form_submit_button(label='Calcular')
    E_f = E + (dist * (sin(m_p_g(lan))))
    N_f = N + (dist * (cos(m_p_g(lan))))
    if submit_button:
        st.write(f'Coordenada do ponto desconhecido: \n  E ({int(E_f)}) - N ({int(N_f)})')