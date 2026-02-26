import streamlit as st
import math

# --- 1. CONFIGURAÇÃO E TEMA ESCURO (NETFLIX/AWS STYLE) ---
st.set_page_config(
    page_title="EngineReliability Pro",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;600&display=swap');
    
    /* Fundo Escuro Global */
    .stApp {
        background-color: #050505;
        color: #E0E0E0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Tecnológica */
    [data-testid="stSidebar"] {
        background-color: #0A0F14 !important;
        border-right: 1px solid #00E5FF;
    }
    
    /* Títulos Vibrantes */
    h1, h2, h3 {
        font-family: 'Rajdhani', sans-serif;
    }
    .title-blue { color: #00E5FF; font-weight: 700; text-transform: uppercase; letter-spacing: 2px;}
    .title-green { color: #00FF33; }
    
    /* Cards Estilo Dashboard */
    .metric-card {
        background: linear-gradient(145deg, #11151C, #0B0E14);
        border: 1px solid #1A2634;
        border-left: 4px solid #00E5FF;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 229, 255, 0.05);
    }
    
    /* Status Colors */
    .status-ok { color: #00FF33; font-weight: bold; font-size: 1.2em;}
    .status-warn { color: #00E5FF; font-weight: bold; font-size: 1.2em;}
    .status-danger { color: #FF0055; font-weight: bold; font-size: 1.2em;}
</style>
""", unsafe_allow_html=True)

# --- 2. O MOTOR MATEMÁTICO DE CONFIABILIDADE ---
def calcular_indice_motor(falhas_ano: int, uso_diario_min: float, dias_s_conserto: float):
    # Conversões: Transformando dias em minutos conforme solicitado
    tc = dias_s_conserto * 24.0 * 60.0
    u = uso_diario_min
    
    # Cálculo do Lambda
    lambd = falhas_ano / 365.0
    
    # Tratamento de Exceções do Numerador do Alfa
    if tc == 0:
        # Se tc for 0, numerador vira ln do módulo de u
        num_alpha = math.log(abs(u)) if u != 0 else 0.0
    elif u == tc:
        # Quando u for igual a tc, o numerador de alfa vira 1
        num_alpha = 1.0
    else:
        # Módulo do tempo desde o ultimo conserto menos uso diário
        num_alpha = abs(tc - u)
        
    # Alfa completo
    alpha = num_alpha / (tc + 1.0)
    
    try:
        # TERMO 1: (1 + 1/tc)^tc
        if tc == 0:
            termo1 = 1.0 # Limite de aproximação p/ evitar divisão por zero
        else:
            termo1 = (1.0 + (1.0 / tc)) ** tc
            
        # TERMO 2: ln(ln(Gamma(alpha + 2)^tc))
        # OTIMIZAÇÃO DE MEMÓRIA (Evita Overflow mantendo a fórmula exata):
        # Usamos math.lgamma que já calcula o ln(Gamma(x)) com segurança extrema.
        # Assim, ln(Gamma(alpha + 2)^tc) = tc * math.lgamma(alpha + 2)
        ln_gama = math.lgamma(alpha + 2.0)
        interior_do_log_externo = tc * ln_gama
        
        if interior_do_log_externo <= 0:
            termo2 = 0.0 # Proteção caso a base do logaritmo colapse
        else:
            termo2 = math.log(interior_do_log_externo)
            
        # TERMO 3: e^(alpha * lambda)
        termo3 = math.exp(alpha * lambd)
        
        # CÁLCULO FINAL DE P
        # Tudo isso dividido por u
        denominador = max(u, 1e-5) # Proteção mínima contra divisão por zero absoluto
        
        p_score = (termo1 * termo2 * termo3) / denominador
        
    except (ValueError, OverflowError, ZeroDivisionError):
        p_score = float('inf')
        
    return p_score, alpha, tc

# --- 3. INTERFACE VISUAL ---
st.markdown("<h1 class='title-blue'>EngineReliability Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #8892B0; font-size: 1.1em;'>Monitoramento Avançado de Falhas para Motores de Alta Performance</p>", unsafe_allow_html=True)

# Divisão de Colunas (Fórmula e Entradas)
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown("<h3 class='title-green'>A Matriz Matemática</h3>", unsafe_allow_html=True)
    st.write("O índice de confiabilidade ($P$) cruza a fadiga temporal com o estresse volumétrico do motor. A equação avalia o comportamento fatorial da degradação em minutos:")
    st.latex(r"P = \frac{\left(1 + \frac{1}{tc}\right)^{tc} \cdot \ln\left(\ln\left(\Gamma(\alpha + 2)^{tc}\right)\right) \cdot e^{\alpha \cdot \lambda}}{u}")
    st.markdown("""
    <ul style='color: #A0AABF; font-size: 0.9em;'>
        <li><b>tc:</b> Tempo desde o último reparo (convertido para minutos).</li>
        <li><b>u:</b> Uso diário em minutos.</li>
        <li><b>λ (Lambda):</b> Taxa de falha diária anualizada.</li>
        <li><b>α (Alpha):</b> Coeficiente de estresse modular.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='metric-card' style='border-left-color: #00FF33;'>", unsafe_allow_html=True)
    st.markdown("<h3>Parâmetros de Telemetria</h3>", unsafe_allow_html=True)
    
    tipo_motor = st.selectbox("Categoria do Motor", ["Automotivo (V8/V6)", "Turbofans Comerciais", "Motor de Foguete (Ciclo Fechado)"])
    falhas_in = st.number_input("Falhas nos últimos 365 dias", min_value=0, value=2)
    dias_in = st.number_input("Dias desde a última manutenção", min_value=0.0, value=45.0, step=1.0)
    uso_min_in = st.number_input("Uso Diário (Minutos)", min_value=0.0, value=120.0, step=10.0)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 4. PROCESSAMENTO E EXIBIÇÃO ---
st.divider()

p_score, alpha_calc, tc_minutos = calcular_indice_motor(falhas_in, uso_min_in, dias_in)

st.markdown("<h2 class='title-blue'>Diagnóstico do Sistema</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div class='metric-card'><p>Minutos sem Manutenção (tc)</p><h2 style='color: white;'>{tc_minutos:,.0f}</h2></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><p>Estresse do Motor (α)</p><h2 style='color: white;'>{alpha_calc:.4f}</h2></div>", unsafe_allow_html=True)
with col3:
    if p_score == float('inf'):
        status, color = "COLAPSO EMINENTE", "status-danger"
        val_display = "∞"
    elif p_score > 5.0:
        status, color = "RISCO CRÍTICO", "status-danger"
        val_display = f"{p_score:.4f}"
    elif p_score > 1.0:
        status, color = "INSPEÇÃO RECOMENDADA", "status-warn"
        val_display = f"{p_score:.4f}"
    else:
        status, color = "OPERAÇÃO NOMINAL", "status-ok"
        val_display = f"{p_score:.4f}"
        
    st.markdown(f"<div class='metric-card' style='border-left-color: transparent;'><p>Índice de Confiabilidade (P)</p><h2 class='{color}'>{val_display}</h2><p class='{color}'>{status}</p></div>", unsafe_allow_html=True)
