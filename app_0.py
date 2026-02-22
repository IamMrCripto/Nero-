import streamlit as st
import math
import plotly.graph_objects as go
import numpy as np
from scipy.special import gamma

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="NERO Pro: Risk Observer (Log Scale)",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILIZAÇÃO CSS (DESIGN VIBRANTE E SIDEBAR LARANJA) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FF6B00 0%, #FF9500 100%) !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    .gradient-text {
        background: linear-gradient(90deg, #FF6B00 0%, #9C27B0 50%, #FF1493 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    .modern-card {
        background: #ffffff;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease;
        height: 100%;
    }
    
    .status-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
    }

    .success-box { padding: 15px; background-color: #f0fdf4; border-left: 5px solid #22c55e; border-radius: 4px; margin: 10px 0; }
    .warning-box { padding: 15px; background-color: #fef2f2; border-left: 5px solid #ef4444; border-radius: 4px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. MOTOR MATEMÁTICO NERO V6.1 (ESCALA LOGARÍTMICA) ---
def calcular_nero(falhas_ano: int, uso_min: float, t_conserto_min: float):
    """Calcula o score NERO aplicando o Logaritmo Natural no resultado final."""
    
    lambd = falhas_ano / 365.0
    alpha = t_conserto_min / (uso_min + 1)

    try:
        # Fator de uso (Garante que u > 1 para o log interno)
        u_val = max(uso_min, 1.1)
        log_base = math.log(u_val)
        
        # Resiliência Fatorial (Gama)
        fatorial_resistencia = gamma(log_base)
        
        # Denominador (Fator de amortecimento elástico)
        # Proteção para evitar log de números <= 0
        denominador = math.log(math.log(max(fatorial_resistencia, 1.1)))
        
        # Numerador Exponencial (Fadiga)
        exponent = lambd * alpha
        
        # Cálculo do P original (linear)
        if exponent > 700: # Proteção contra overflow
            raw_p = float('inf')
        else:
            raw_p = math.exp(exponent) / denominador
            
        # --- MODIFICAÇÃO SOLICITADA: Aplicação de ln no resultado ---
        if raw_p <= 0:
            p_score = -5.0 # Piso logarítmico para risco nulo
        elif raw_p == float('inf'):
            p_score = float('inf')
        else:
            p_score = math.log(raw_p)

    except (ValueError, OverflowError, ZeroDivisionError):
        p_score = float('inf')
        denominador = 1.0

    return p_score, lambd, alpha, denominador

def get_status_visual(p_score):
    """Thresholds ajustados para a nova escala logarítmica (Magnitude)"""
    if p_score == float('inf') or p_score > 6.0:
        return "CRÍTICO EXTREMO", "#7f1d1d", "⛔"
    elif p_score > 3.5:
        return "CRÍTICO", "#dc2626", "🔴"
    elif p_score > 1.5:
        return "ALERTA", "#FF9500", "🟠"
    elif p_score > -0.5:
        return "OPERACIONAL", "#9C27B0", "🟣"
    else:
        return "EXCELENTE", "#00C853", "🟢"

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 2.5em;'>🛡️</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>NERO Pro</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.8;'>Magnitude de Risco (Log Scale)</p>", unsafe_allow_html=True)
    st.divider()
    
    pagina = st.radio(
        "Navegação",
        ["🏠 Visão Geral", "⚙️ Dashboard de Ativos", "🚀 Sistemas Complexos", "⚖️ Comparador de Marcas"]
    )

    if pagina == "⚙️ Dashboard de Ativos":
        st.divider()
        st.subheader("🛠️ Parâmetros do Ativo")
        nome_ativo = st.text_input("Identificação", "Unidade Hidráulica H1")
        falhas_in = st.number_input("Falhas/Ano", 0, 100, 4)
        dias_in = st.number_input("Dias s/ Manutenção", 0, 365, 120)
        uso_horas_in = st.slider("Uso Diário (h)", 0.5, 24.0, 8.0)

# --- 5. PÁGINAS ---
if pagina == "🏠 Visão Geral":
    st.markdown("<h1 class='gradient-text' style='font-size: 3.5em;'>Escala de Magnitude NERO</h1>", unsafe_allow_html=True)
    
    col_img, col_txt = st.columns([1, 1.2], gap="large")
    with col_img:
        st.markdown("""
        <div class="modern-card" style="background: #1e1e1e; color: white; border-left: 4px solid #FF6B00;">
            <h3>Por que logaritmo natural (ln)?</h3>
            <p>Sistemas mecânicos tendem a falhar de forma exponencial sob estresse. Ao inserirmos o <b>ln</b> no resultado, transformamos essa curva explosiva em uma métrica de magnitude linear.</p>
            <ul>
                <li><b>P < 0:</b> Alta resiliência sistêmica.</li>
                <li><b>P > 3:</b> Zona de fadiga acelerada.</li>
                <li><b>P > 6:</b> Ponto de ruptura iminente.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_txt:
        st.markdown("### Nova Equação Fenomenológica")
        st.latex(r"P = \ln \left( \frac{e^{(\lambda \cdot \alpha)}}{\ln(\ln(\Gamma(\ln(u))))} \right)")
        st.markdown("""
        Onde o resultado final não é mais uma taxa bruta, mas sim o **expoente de risco** acumulado no sistema. Isso permite comparar ativos de naturezas diferentes sob a mesma régua logarítmica.
        """)

elif pagina == "⚙️ Dashboard de Ativos":
    p_atual, lambd_atual, alpha_atual, denom_atual = calcular_nero(falhas_in, uso_horas_in * 60, dias_in * 1440)
    status_txt, status_cor, status_icon = get_status_visual(p_atual)
    
    p_display = "∞ (Singularidade)" if p_atual == float('inf') else f"{p_atual:.4f}"
    
    st.markdown(f"## Análise em Tempo Real: **{nome_ativo}**")
    
    col_kpi, col_info = st.columns([1, 2.5])
    with col_kpi:
        st.markdown(f"""
        <div class="modern-card" style="border-top: 6px solid {status_cor}; text-align: center;">
            <p style="color: #64748b; font-size: 0.9em; font-weight: 600; text-transform: uppercase;">Magnitude NERO (P)</p>
            <h2 style="font-size: 3em; color: #1e293b; margin: 10px 0;">{p_display}</h2>
            <div style="background: {status_cor}20; color: {status_cor};" class="status-badge">
                {status_icon} {status_txt}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_info:
        st.markdown("<div class='modern-card'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Fadiga (λ)", f"{lambd_atual:.4f}")
        c2.metric("Estresse (α)", f"{alpha_atual:.2f}")
        c3.metric("Resiliência (Denom)", f"{denom_atual:.3f}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Gráfico de Projeção
    st.markdown("### Projeção de Magnitude de Risco")
    dias_proj = np.linspace(0, dias_in + 90, 100)
    y_proj = [calcular_nero(falhas_in, uso_horas_in * 60, d * 1440)[0] for d in dias_proj]
    y_plot = [min(max(v, -2), 8) if v != float('inf') else 8 for v in y_proj]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dias_proj, y=y_plot, line=dict(color='#FF6B00', width=4)))
    fig.update_layout(height=400, xaxis_title="Dias s/ Manutenção", yaxis_title="Magnitude ln(P)",
                      plot_bgcolor="white", yaxis=dict(range=[-2, 8]))
    st.plotly_chart(fig, use_container_width=True)

elif pagina == "🚀 Sistemas Complexos":
    st.markdown("<h2 class='gradient-text'>Média Logarítmica Ponderada</h2>", unsafe_allow_html=True)
    st.write("Em sistemas complexos, as magnitudes individuais são ponderadas pelo estresse sistêmico.")
    
    # Simulação Simplificada
    sists = ["Eletrônica", "Mecânica", "Refrigeração"]
    p_list = []
    a_list = []
    
    cols = st.columns(3)
    for i, s in enumerate(sists):
        with cols[i]:
            st.subheader(s)
            f = st.number_input(f"Falhas/Ano ({s})", 0, 50, 2+i, key=f"f{i}")
            p, _, a, _ = calcular_nero(f, 8*60, 60*1440)
            p_list.append(p)
            a_list.append(a)
            st.caption(f"Magnitude: {p:.3f}")

    p_global = sum(p * a for p, a in zip(p_list, a_list)) / sum(a_list)
    stat_g, cor_g, _ = get_status_visual(p_global)
    
    st.markdown(f"""
    <div style="text-align: center; padding: 40px; background: {cor_g}15; border: 2px solid {cor_g}; border-radius: 20px;">
        <h2 style="margin:0;">Magnitude Global do Sistema</h2>
        <h1 style="font-size: 5em; color: {cor_g};">{p_global:.4f}</h1>
        <p style="font-weight:bold; color: {cor_g}; uppercase">{stat_g}</p>
    </div>
    """, unsafe_allow_html=True)

elif pagina == "⚖️ Comparador de Marcas":
    st.markdown("## ⚖️ Comparação de Resiliência Logarítmica")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Marca A")
        fa = st.number_input("Falhas/Ano (A)", 0, 50, 2)
        da = st.number_input("Dias sem Falha (A)", 0, 500, 200)
        pa, _, _, _ = calcular_nero(fa, 10*60, da*1440)
        st.metric("Magnitude P (A)", f"{pa:.4f}")
    with c2:
        st.markdown("### Marca B")
        fb = st.number_input("Falhas/Ano (B)", 0, 50, 8)
        db = st.number_input("Dias sem Falha (B)", 0, 500, 90)
        pb, _, _, _ = calcular_nero(fb, 10*60, db*1440)
        st.metric("Magnitude P (B)", f"{pb:.4f}")

    st.divider()
    if pa < pb:
        st.success(f"🏆 A **Marca A** possui uma magnitude de risco menor (Melhor resiliência).")
    else:
        st.warning(f"🏆 A **Marca B** possui uma magnitude de risco menor.")



