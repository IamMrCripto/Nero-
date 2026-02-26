import streamlit as st
import math
import plotly.graph_objects as go
import numpy as np
import os

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Engine Reliability Observer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILIZAÇÃO CSS (Dark Mode Premium) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&family=Inter:wght@300;400;600;800&display=swap');
    
    /* Fundo Escuro Global */
    .stApp { background-color: #0a0e17; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #06090e !important; border-right: 1px solid #1e293b; }
    [data-testid="stSidebar"] * { color: #94a3b8 !important; }
    
    /* Textos Gradientes (Azul Claro e Verde) */
    .gradient-text { 
        background: linear-gradient(90deg, #00B0FF 0%, #00C853 100%); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700; 
    }
    
    /* Cards Estilo Plataforma (Netflix/Amazon) */
    .modern-card { 
        background: #111827; 
        padding: 24px; 
        border-radius: 12px; 
        border: 1px solid #1f2937; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); 
        transition: all 0.3s ease; 
        height: 100%; 
    }
    .modern-card:hover { 
        transform: translateY(-5px); 
        border-color: #00B0FF; 
        box-shadow: 0 15px 40px rgba(0, 176, 255, 0.15); 
    }
    
    /* Badges */
    .status-badge { 
        display: inline-block; padding: 6px 14px; border-radius: 6px; 
        font-weight: 800; font-size: 0.85rem; letter-spacing: 0.1em; 
        text-transform: uppercase; font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Cabeçalhos e Fontes */
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; color: #ffffff; }
    hr { border-color: #1e293b; }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. MOTOR MATEMÁTICO DE CONFIABILIDADE (EM MINUTOS) ---
def calcular_indice_motor(falhas_ano: int, uso_diario_h: float, dias_desde_conserto: float):
    # Conversão obrigatória para MINUTOS
    u = max(uso_diario_h * 60.0, 0.1) # Uso diário em minutos (min 0.1 para evitar div/0)
    tc = dias_desde_conserto * 24.0 * 60.0 # Tempo sem conserto em minutos

    # Lambda: Taxa de falha anual distribuída
    lambd = falhas_ano / 365.0

    # Lógica Condicional do Numerador de Alfa
    if u == tc:
        num_alpha = 1.0
    elif tc == 0:
        num_alpha = math.log(abs(u))
    else:
        num_alpha = abs(tc - u)

    # Calculo de Alfa
    alpha = num_alpha / (tc + 1.0)

    # Componentes da Equação Principal
    try:
        # Fator 1: Base de Euler Dinâmica
        if tc == 0:
            termo_1 = 1.0
        else:
            termo_1 = (1.0 + 1.0 / tc) ** tc

        # Fator 2: ln(lnGama(alfa + 2))
        # Utiliza-se lgamma que é o logaritmo natural da função gama. 
        # Proteção (1e-9) para evitar logaritmo de zero no limite inferior.
        ln_gama = math.lgamma(alpha + 2.0)
        ln_gama = max(ln_gama, 1e-9) 
        termo_2 = math.log(ln_gama)

        # Fator 3: Fator Estocástico
        termo_3 = math.exp(alpha * lambd)

        # Equação Completa (Assumindo a divisão por 'u' padrão para normalizar)
        numerador = termo_1 * termo_2 * termo_3
        indice = abs(numerador / u)
        
    except Exception:
        indice = float('inf')

    return indice, lambd, alpha, u, tc

# --- PARÂMETROS VISUAIS ---
def get_status_motor(indice):
    if indice < 0.005:
        return "CONFIABILIDADE MÁXIMA", "rgba(0, 200, 83, 0.2)", "#00c853", "🟢"
    elif indice < 0.025:
        return "REGIME OPERACIONAL", "rgba(0, 176, 255, 0.2)", "#00b0ff", "🔵"
    elif indice < 0.070:
        return "ALERTA DE DESGASTE", "rgba(255, 196, 0, 0.2)", "#ffc400", "🟠"
    else:
        return "RISCO DE RUPTURA", "rgba(255, 61, 0, 0.2)", "#ff3d00", "🔴"

# --- 4. NAVEGAÇÃO LATERAL ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #00B0FF; font-size: 3em;'>⚙️</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-bottom: 0; color: white;'>EngineMetrics</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #00C853; font-weight: bold; letter-spacing: 2px;'>CORE V7</p>", unsafe_allow_html=True)
    st.divider()
    
    pagina = st.radio(
        "Navegação",
        ["🌐 Visão Geral do Protocolo", "🏎️ Monitor de Motores", "🚀 Telemetria de Frota", "⚖️ Comparador de Propulsores"],
        label_visibility="collapsed"
    )

    if pagina == "🏎️ Monitor de Motores":
        st.divider()
        st.markdown("<p style='color: #00B0FF; font-weight: 600;'>🖥️ PAINEL DE CONTROLE</p>", unsafe_allow_html=True)
        nome_motor = st.text_input("Designação do Motor", "Raptor V2 (Foguete)")
        falhas_in = st.number_input("Falhas (Últimos 365d)", min_value=0, value=2)
        dias_in = st.number_input("Dias desde última manutenção", min_value=0, value=15)
        uso_horas_in = st.slider("Uso Diário (Horas)", 0.1, 24.0, 2.5, 0.1)

# --- 5. ROTEAMENTO DE PÁGINAS ---

if pagina == "🌐 Visão Geral do Protocolo":
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px;">
        <h1 class="gradient-text" style="font-size: 4.5em; margin-bottom: 10px; line-height: 1.1;">Dinâmica de Fluidos e Estresse Mecânico</h1>
        <h3 style="color: #94a3b8; font-weight: 300; font-size: 1.4em; max-width: 900px; margin: 0 auto;">
            Um novo paradigma matemático para calcular o <b>Índice de Confiabilidade</b> de motores automotivos, turbinas de aviação e propulsores aeroespaciais.
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col_img1, col_img2 = st.columns(2)
    with col_img1:
        if os.path.exists("BCO.ad96e715-3f80-4890-8452-c916d844511e.jpg"):
            st.image("BCO.ad96e715-3f80-4890-8452-c916d844511e.jpg", caption="Propulsão Aeroespacial em Estresse Termodinâmico", use_container_width=True)
    with col_img2:
        if os.path.exists("BCO.46320da6-8731-4951-83d9-c2b5fd96709e.jpg"):
            st.image("BCO.46320da6-8731-4951-83d9-c2b5fd96709e.jpg", caption="Combustão Interna e Desgaste de Pistões", use_container_width=True)

    st.markdown("---")
    
    st.markdown("### 🔬 O Motor Matemático (A Fórmula de Ruptura)")
    st.write("A equação a seguir avalia a propensão à falha estrutural. **Quanto menor o resultado, maior a confiabilidade do motor.** Todo o processamento interno de tempo é convertido em minutos na camada de máquina.")
    
    col_eq, col_exp = st.columns([1.2, 1])
    with col_eq:
        st.markdown("<div class='modern-card'>", unsafe_allow_html=True)
        st.latex(r"\text{Índice} = \frac{\left(1 + \frac{1}{t_c}\right)^{t_c} \cdot \ln(\ln\Gamma(\alpha + 2)) \cdot e^{\alpha \cdot \lambda}}{u}")
        st.markdown("<hr>", unsafe_allow_html=True)
        st.latex(r"\lambda = \frac{\text{Falhas}}{365}")
        st.latex(r"\alpha = \frac{|t_c - u|}{t_c + 1}")
        st.markdown("<p style='font-size: 0.8em; color: #64748b; text-align: center;'>(Condições especiais: Se $u=t_c$, num=1. Se $t_c=0$, num=$\ln|u|$)</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_exp:
        st.markdown("""
        <div class='modern-card'>
        <h4 style='color: #00B0FF; margin-top: 0;'>Dicionário de Variáveis</h4>
        <ul style='color: #e2e8f0; line-height: 1.8;'>
            <li><b style='color:#00C853;'>u (Uso):</b> Minutos de operação diária. O amortecedor do risco.</li>
            <li><b style='color:#00C853;'>t_c (Tempo de Conserto):</b> Minutos acumulados desde a última intervenção.</li>
            <li><b style='color:#00C853;'>Termo (1 + 1/tc)^tc:</b> Fator Euler de degradação base.</li>
            <li><b style='color:#00C853;'>ln(lnΓ(α + 2)):</b> Dupla compressão logarítmica da função Gama de ordem superior, atuando como um filtro de choque para sistemas recém-consertados.</li>
            <li><b style='color:#00C853;'>e^(α·λ):</b> Risco de estocástico de novas falhas (catalisador).</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

elif pagina == "🏎️ Monitor de Motores":
    # Cálculo rodando por trás
    indice, lambd_atual, alpha_atual, u_minutos, tc_minutos = calcular_indice_motor(falhas_in, uso_horas_in, dias_in)
    status_txt, bg_cor, borda_cor, icon = get_status_motor(indice)

    st.markdown(f"<h2>Telemetria em Tempo Real: <span class='gradient-text'>{nome_motor}</span></h2>", unsafe_allow_html=True)
    
    col_kpi, col_info = st.columns([1, 2])
    
    with col_kpi:
        st.markdown(f"""
        <div class="modern-card" style="border-top: 6px solid {borda_cor}; background: {bg_cor}; text-align: center;">
            <p style="color: #94a3b8; font-size: 0.9em; font-weight: 700; margin: 0; letter-spacing: 1px;">ÍNDICE DE DESGASTE</p>
            <h2 style="font-size: 3.5em; color: white; margin: 10px 0; font-family: 'Space Grotesk';">{indice:.4e}</h2>
            <div class="status-badge" style="background: {borda_cor}; color: #000;">
                {icon} {status_txt}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_info:
        st.markdown("<div class='modern-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #00C853; margin-top:0;'>🔬 Parâmetros de Motor Convertidos</h4>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Tempo s/ Conserto ($t_c$)", f"{tc_minutos:,.0f} min")
        c2.metric("Uso Diário ($u$)", f"{u_minutos:,.0f} min")
        c3.metric("Taxa Estocástica ($\lambda$)", f"{lambd_atual:.4f}")
        st.markdown("<hr style='border-color: #334155;'>", unsafe_allow_html=True)
        st.markdown(f"**Variação de Alfa ($\alpha$):** O módulo termodinâmico calculou uma distorção de esforço de `{alpha_atual:.6f}`.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Gráfico Logarítmico Moderno
    st.markdown("### 📈 Curva de Fadiga vs. Tempo de Negligência")
    st.write("Projeção do desgaste do motor caso a manutenção continue sendo ignorada.")
    
    dias_projecao = max(dias_in + 90, 100)
    eixo_x = np.linspace(1, dias_projecao, 150)
    eixo_y = [calcular_indice_motor(falhas_in, uso_horas_in, d)[0] for d in eixo_x]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=eixo_x, y=eixo_y, mode='lines', name='Linha de Falha',
        line=dict(color='#00B0FF', width=4, shape='spline'),
        fill='tozeroy', fillcolor='rgba(0, 176, 255, 0.1)'
    ))
    fig.add_trace(go.Scatter(
        x=[max(dias_in, 1)], y=[indice], mode='markers', name='Momento Atual',
        marker=dict(color='#00C853', size=16, line=dict(color='white', width=2))
    ))
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=450, margin=dict(l=0, r=0, t=20, b=0),
        xaxis=dict(title="Dias sem Manutenção", showgrid=True, gridcolor='#1e293b'),
        yaxis=dict(type="log", title="Índice de Risco (Escala Log)", tickformat=".1e", showgrid=True, gridcolor='#1e293b')
    )
    st.plotly_chart(fig, use_container_width=True)

elif pagina == "🚀 Telemetria de Frota":
    st.markdown("<h2 class='gradient-text'>Mapeamento de Múltiplos Motores</h2>", unsafe_allow_html=True)
    st.write("Análise de componentes críticos para frotas aeroespaciais e automotivas.")
    
    motores = ["Turbina Esquerda (GE90)", "Motor Principal (Raptor)", "Auxiliar de Partida"]
    
    c1, c2, c3 = st.columns(3)
    cols = [c1, c2, c3]
    
    for i, sys_name in enumerate(motores):
        with cols[i]:
            cores_borda = ["#00B0FF", "#00C853", "#9C27B0"]
            st.markdown(f"<div class='modern-card' style='border-top: 4px solid {cores_borda[i]};'>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='color: white;'>{sys_name}</h4>", unsafe_allow_html=True)
            
            f = st.number_input(f"Falhas/Ano", 0, 50, 1 + i, key=f"f_{i}")
            d = st.number_input(f"Dias s/ Manut.", 0, 2000, 10 + i*30, key=f"d_{i}")
            u = st.slider(f"Uso (Horas/Dia)", 0.5, 24.0, 4.0, key=f"u_{i}")
            
            p, _, _, _, _ = calcular_indice_motor(f, u, d)
            status, bg, borda, icon = get_status_motor(p)
            
            st.markdown(f"<p style='color: {borda}; font-family: Space Grotesk; font-size: 1.5em; font-weight: 700; margin: 10px 0;'>{p:.3e}</p>", unsafe_allow_html=True)
            st.markdown(f"<span class='status-badge' style='background: {bg}; border: 1px solid {borda}; color: {borda}; font-size: 0.65rem;'>{icon} {status}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

elif pagina == "⚖️ Comparador de Propulsores":
    st.markdown("## ⚖️ Teste de Resistência Cruzada")
    st.write("Submeta dois motores a parâmetros de estresse. O propulsor com **menor índice de desgaste** ganha a certificação de confiabilidade.")
    
    colA, colVS, colB = st.columns([1, 0.2, 1])
    
    with colA:
        st.markdown("<div class='modern-card' style='border-top: 4px solid #00B0FF;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #00B0FF;'>Motor Alfa</h3>", unsafe_allow_html=True)
        nome_a = st.text_input("Modelo A", "Rolls-Royce Trent", key="n_a")
        f_a = st.number_input("Falhas", 0, 100, 2, key="f_a")
        d_a = st.number_input("Dias de Uso", 0, 7000, 60, key="d_a")
        u_a = st.number_input("Horas/Dia", 1.0, 24.0, 14.0, key="u_a")
        p_a, _, _, _, _ = calcular_indice_motor(f_a, u_a, d_a)
        _, _, cor_a, icon_a = get_status_motor(p_a)
        st.markdown(f"<h1 style='color: white; margin-top: 15px;'>{p_a:.4e}</h1>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with colVS:
        st.markdown("<h1 style='text-align: center; color: #334155; margin-top: 100px;'>VS</h1>", unsafe_allow_html=True)

    with colB:
        st.markdown("<div class='modern-card' style='border-top: 4px solid #00C853;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #00C853;'>Motor Beta</h3>", unsafe_allow_html=True)
        nome_b = st.text_input("Modelo B", "Pratt & Whitney", key="n_b")
        f_b = st.number_input("Falhas", 0, 100, 5, key="f_b")
        d_b = st.number_input("Dias de Uso", 0, 7000, 45, key="d_b")
        u_b = st.number_input("Horas/Dia", 1.0, 24.0, 12.0, key="u_b")
        p_b, _, _, _, _ = calcular_indice_motor(f_b, u_b, d_b)
        _, _, cor_b, icon_b = get_status_motor(p_b)
        st.markdown(f"<h1 style='color: white; margin-top: 15px;'>{p_b:.4e}</h1>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if p_a < p_b:
        st.success(f"🏆 O **{nome_a}** apresentou o melhor projeto de engenharia estrutural nestas condições (Menos propenso a falhas).")
    elif p_b < p_a:
        st.success(f"🏆 O **{nome_b}** apresentou o melhor projeto de engenharia estrutural nestas condições (Menos propenso a falhas).")
    else:
        st.info("⚖️ Empate técnico de fadiga nos rotores/pistões.")
