import streamlit as st
import math
import plotly.graph_objects as go
import numpy as np

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Reliability Engine Analytics",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILIZAÇÃO CSS (Tema Escuro + Azul Claro + Verde) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Fundo principal Escuro (Preto/Cinza Escuro) */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }

    /* Customização da Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #020617 100%) !important;
        border-right: 1px solid #1e293b;
    }
    
    /* Headers com Gradiente Azul e Verde */
    .hero-text {
        background: linear-gradient(90deg, #00d2ff 0%, #00ff87 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 3.5em;
        text-transform: uppercase;
        letter-spacing: -1px;
    }

    /* Cards Estilo Netflix/Microsoft */
    .tech-card {
        background: #111827;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #1f2937;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
        height: 100%;
        border-top: 4px solid #00d2ff;
    }
    .tech-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 210, 255, 0.15);
        border-top: 4px solid #00ff87;
    }

    /* Status Badges */
    .badge-safe {
        background: rgba(0, 255, 135, 0.1);
        color: #00ff87;
        border: 1px solid #00ff87;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: bold;
    }
    .badge-danger {
        background: rgba(255, 61, 0, 0.1);
        color: #ff3d00;
        border: 1px solid #ff3d00;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: bold;
    }

    hr { border-color: #1e293b; }
</style>
""", unsafe_allow_html=True)

# --- 3. MOTOR MATEMÁTICO DE CONFIABILIDADE ---
def calcular_indice_motor(falhas_ano: int, horas_uso_dia: float, dias_desde_conserto: float):
    """
    Fórmula de Confiabilidade de Motores:
    R = [ (1 + 1/tc)^tc * (ln(ln(Gamma(alpha + 2))))^tc * e^(alpha * lambda) ] / u
    """
    # Conversão obrigatória para MINUTOS
    u = max(horas_uso_dia * 60.0, 1.0) # Proteção mínima de 1 min para evitar div por 0
    tc_min = dias_desde_conserto * 1440.0
    tc = max(tc_min, 1.0) # Proteção para limites de euler e divisões
    
    # Lambda: Falhas normalizadas
    lambd = falhas_ano / 365.0
    
    # Cálculo do Numerador de Alpha com as regras de exceção
    if abs(u - tc_min) < 0.001:  # u igual a tc
        num_alpha = 1.0
    elif tc_min == 0.0:
        num_alpha = math.log(abs(u)) if abs(u) > 0 else 0.0
    else:
        num_alpha = abs(tc - u)
        
    alpha = num_alpha / (tc + 1.0)
    
    try:
        # Termo 1: (1 + 1/tc)^tc  --> Tende a Euler (e) quando tc é grande
        termo1 = math.pow((1.0 + 1.0 / tc), tc)
        
        # Termo 2: (ln(ln(Gamma(alpha + 2))))^tc
        # Necessita de salvaguardas rigorosas para evitar math domain error (ln de números <= 0)
        gama_val = math.gamma(alpha + 2.0)
        ln_1 = math.log(max(gama_val, 1.0001)) # Garante que o resultado seja > 0 para o próximo ln
        ln_2 = math.log(max(ln_1, 0.0001))
        
        # Como elevar à potência de milhares de minutos (tc) pode estourar a memória (Overflow):
        ln_2_safe = max(abs(ln_2), 0.000001) 
        termo2 = math.pow(ln_2_safe, min(tc, 10000.0)) # Limitamos o teto do expoente para evitar crash do Python
        
        # Termo 3: e^(alpha * lambda)
        termo3 = math.exp(alpha * lambd)
        
        # Equação Final
        indice = (termo1 * termo2 * termo3) / u
        
    except OverflowError:
        indice = 999999.0 # Teto de ruptura

    return indice, alpha, lambd, u, tc

def get_status(indice):
    if indice < 10.0:
        return "CONFIABILIDADE MÁXIMA", "badge-safe", "✔️"
    elif indice < 50.0:
        return "OPERAÇÃO ESTÁVEL", "badge-safe", "🔵"
    elif indice < 200.0:
        return "DESGASTE ACELERADO", "badge-danger", "⚠️"
    else:
        return "FALHA ESTRUTURAL EMINENTE", "badge-danger", "💥"

# --- 4. NAVEGAÇÃO LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='color: #00d2ff;'>⚙️ Engine<br>Analytics</h2>", unsafe_allow_html=True)
    st.markdown("Plataforma de Diagnóstico Matemático")
    st.divider()
    
    pagina = st.radio(
        "Módulos:",
        ["🌐 Visão Geral da Teoria", "🚀 Diagnóstico de Motor", "⚖️ Comparador de Turbinas"],
        label_visibility="collapsed"
    )

# --- 5. ROTEAMENTO DE PÁGINAS ---
if pagina == "🌐 Visão Geral da Teoria":
    st.markdown("<div style='text-align: center; padding: 40px 0;'><h1 class='hero-text'>A Matemática da Propulsão</h1></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("""
        <div class='tech-card'>
            <h3 style='color: #00ff87;'>A Fórmula de Degradação Exponencial Dupla</h3>
            <p style='color: #94a3b8; line-height: 1.8;'>
                Este sistema foi projetado para avaliar o estresse de materiais e a degradação mecânica em motores de alta performance. 
                A equação central modela o risco transformando o tempo de uso e a negligência de manutenção em minutos absolutos, criando uma curva de falha hiper-sensível.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.markdown("### 🧮 A Equação Fundamental")
        st.latex(r"I = \frac{\left(1 + \frac{1}{t_c}\right)^{t_c} \cdot \left[ \ln(\ln(\Gamma(\alpha + 2))) \right]^{t_c} \cdot e^{\alpha \cdot \lambda}}{U}")
        
        st.markdown("""
        * **$t_c$ (Tempo de Conserto):** Minutos desde a última intervenção.
        * **$U$ (Uso):** Minutos de trabalho diário.
        * **$\alpha$ (Alpha):** Coeficiente dinâmico baseado na diferença entre tempo parado e tempo de uso.
        * **$\lambda$ (Lambda):** Fator de falhas sistêmicas por ano.
        """)
        
    with col2:
        # Imagem contextual de turbina de avião
        pass
        
    st.markdown("---")
    st.markdown("<h3 style='text-align: center; color: #00d2ff;'>Aplicações Práticas</h3>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='tech-card' style='text-align: center;'><h4>Carros de Alta Performance</h4><p style='color:#64748b;'>Blocos V8, motores sobrealimentados e desgaste de bielas.</p></div>", unsafe_allow_html=True)
    c2.markdown("<div class='tech-card' style='text-align: center; border-top-color: #00ff87;'><h4>Turbinas Aeronáuticas</h4><p style='color:#64748b;'>Fadiga térmica em pás de titânio sob regime contínuo.</p></div>", unsafe_allow_html=True)
    c3.markdown("<div class='tech-card' style='text-align: center;'><h4>Propulsão Espacial</h4><p style='color:#64748b;'>Análise estocástica de bicos injetores e câmaras de combustão.</p></div>", unsafe_allow_html=True)

    # Imagem contextual de motor de foguete
    

elif pagina == "🚀 Diagnóstico de Motor":
    st.markdown("<h1 style='color: white; border-left: 6px solid #00d2ff; padding-left: 15px;'>Módulo de Diagnóstico</h1>", unsafe_allow_html=True)
    
    c_in, c_out = st.columns([1, 2])
    
    with c_in:
        st.markdown("<div class='tech-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #00ff87; margin-top: 0;'>Entrada de Telemetria</h4>", unsafe_allow_html=True)
        tipo_motor = st.selectbox("Categoria", ["Motor a Combustão (Carro)", "Turbofan (Avião)", "Motor Foguete (Espacial)"])
        falhas = st.number_input("Falhas (Últimos 365 dias)", 0, 50, 2)
        uso_h = st.slider("Uso Diário Médio (Horas)", 0.1, 24.0, 4.0)
        dias_manut = st.number_input("Tempo desde último conserto (Dias)", 0.0, 5000.0, 30.0)
        st.markdown("</div>", unsafe_allow_html=True)
        
    indice, alpha, lambd, u_min, tc_min = calcular_indice_motor(falhas, uso_h, dias_manut)
    txt, classe, icone = get_status(indice)
    
    with c_out:
        st.markdown(f"""
        <div style='background: #111827; border: 1px solid #1f2937; padding: 40px; border-radius: 12px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.4);'>
            <p style='color: #94a3b8; font-weight: bold; letter-spacing: 2px; margin: 0;'>ÍNDICE DE CONFIABILIDADE OBTIDO</p>
            <h1 style='font-size: 5em; color: white; margin: 10px 0;'>{indice:.4f}</h1>
            <span class='{classe}' style='font-size: 1.2em;'>{icone} {txt}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        k1, k2, k3 = st.columns(3)
        k1.markdown(f"<div class='tech-card' style='padding: 15px;'>Variável $\\alpha$<br><strong style='font-size: 1.5em; color:#00d2ff;'>{alpha:.4f}</strong></div>", unsafe_allow_html=True)
        k2.markdown(f"<div class='tech-card' style='padding: 15px;'>Tempo ($t_c$ min)<br><strong style='font-size: 1.5em; color:#00d2ff;'>{tc_min:.0f}</strong></div>", unsafe_allow_html=True)
        k3.markdown(f"<div class='tech-card' style='padding: 15px;'>Uso ($U$ min)<br><strong style='font-size: 1.5em; color:#00ff87;'>{u_min:.0f}</strong></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Projeção de Colapso")
    
    # Gráfico de Projeção
    dias_futuros = np.linspace(max(1, dias_manut), dias_manut + 90, 50)
    riscos = [calcular_indice_motor(falhas, uso_h, d)[0] for d in dias_futuros]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dias_futuros, y=riscos, 
        mode='lines', 
        line=dict(color='#00d2ff', width=3),
        fill='tozeroy', 
        fillcolor='rgba(0, 210, 255, 0.1)'
    ))
    fig.update_layout(
        plot_bgcolor='#0b0f19', paper_bgcolor='#0b0f19',
        font=dict(color='#e2e8f0'),
        xaxis=dict(title="Dias sem Manutenção", gridcolor='#1e293b'),
        yaxis=dict(title="Crescimento do Risco", gridcolor='#1e293b', type="log"),
        height=350, margin=dict(t=10, b=10, l=10, r=10)
    )
    st.plotly_chart(fig, use_container_width=True)

elif pagina == "⚖️ Comparador de Turbinas":
    st.markdown("<h2 style='color: white;'>Duelo de Especificações</h2>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("<div class='tech-card' style='border-top: 4px solid #00d2ff;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #00d2ff;'>Motor A</h3>", unsafe_allow_html=True)
        nome_a = st.text_input("Identificação", "Pratt & Whitney F135", key="nome_a")
        f_a = st.number_input("Falhas (Ano)", 0, 100, 1, key="fa")
        u_a = st.number_input("Uso Diário (H)", 1.0, 24.0, 6.0, key="ua")
        tc_a = st.number_input("Dias sem revisão", 0.0, 5000.0, 120.0, key="tca")
        
        ind_a, _, _, _, _ = calcular_indice_motor(f_a, u_a, tc_a)
        txt_a, class_a, icone_a = get_status(ind_a)
        st.markdown(f"<hr><h2 style='color:white;'>Índice: {ind_a:.4f}</h2><span class='{class_a}'>{icone_a} {txt_a}</span></div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("<div class='tech-card' style='border-top: 4px solid #00ff87;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #00ff87;'>Motor B</h3>", unsafe_allow_html=True)
        nome_b = st.text_input("Identificação", "Rolls-Royce Trent 900", key="nome_b")
        f_b = st.number_input("Falhas (Ano)", 0, 100, 3, key="fb")
        u_b = st.number_input("Uso Diário (H)", 1.0, 24.0, 14.0, key="ub")
        tc_b = st.number_input("Dias sem revisão", 0.0, 5000.0, 45.0, key="tcb")
        
        ind_b, _, _, _, _ = calcular_indice_motor(f_b, u_b, tc_b)
        txt_b, class_b, icone_b = get_status(ind_b)
        st.markdown(f"<hr><h2 style='color:white;'>Índice: {ind_b:.4f}</h2><span class='{class_b}'>{icone_b} {txt_b}</span></div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    if ind_a < ind_b:
        st.success(f"🏆 O motor **{nome_a}** possui um índice de falha menor, mostrando-se mais confiável nestas configurações.")
    elif ind_b < ind_a:
        st.success(f"🏆 O motor **{nome_b}** possui um índice de falha menor, mostrando-se mais confiável nestas configurações.")
