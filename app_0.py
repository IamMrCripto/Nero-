import streamlit as st
import math
import plotly.graph_objects as go
import numpy as np
from scipy.special import gamma
from pathlib import Path

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="NERO Pro: Risk Observer (Log Scale) - Atualizado",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILIZAÇÃO CSS (mantida) ---
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
        denominador = math.log(math.log(max(fatorial_resistencia, 1.1)))

        # Numerador Exponencial (Fadiga)
        exponent = lambd * alpha

        # Cálculo do P original (linear)
        if exponent > 700:  # Proteção contra overflow
            raw_p = float('inf')
        else:
            raw_p = math.exp(exponent) / denominador

        # Aplicação de ln no resultado
        if raw_p <= 0:
            p_score = -5.0  # Piso logarítmico para risco nulo
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
        ["🏠 Visão Geral", "⚙️ Dashboard de Ativos", "🚀 Sistemas Complexos", "⚖️ Comparador de Marcas", "📘 Exemplos de Aplicação"]
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
        st.markdown("Onde o resultado final não é mais uma taxa bruta, mas sim o **expoente de risco** acumulado no sistema.")

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
    st.markdown("<h2 class='gradient-text'>Média Logarítmica Ponderada por Coeficiente de Confiabilidade</h2>", unsafe_allow_html=True)
    st.write("Aqui calculamos a média dos **coeficientes de confiabilidade** \(C_i\) ponderada por \(\\alpha_i\). Usamos:")
    st.latex(r"C_{global} = \frac{\sum_i C_i \cdot \alpha_i}{\sum_i \alpha_i} \quad\text{onde}\quad C_i = e^{-P_i}")

    # Simulação com imagens de motores
    sists = ["Eletrônica", "Mecânica", "Refrigeração"]
    p_list = []
    a_list = []
    c_list = []

    cols = st.columns(3)
    # Paths de exemplo para imagens (substitua pelos caminhos reais)
    image_paths = ["motors/motor_electronics.png", "motors/motor_mechanical.png", "motors/motor_refrigeration.png"]

    for i, s in enumerate(sists):
        with cols[i]:
            st.subheader(s)
            f = st.number_input(f"Falhas/Ano ({s})", 0, 50, 2+i, key=f"f{i}")
            # parâmetros fixos de uso e manutenção para comparação
            uso_min = 8 * 60
            dias_min = 60 * 1440
            p, _, a, _ = calcular_nero(f, uso_min, dias_min)
            # Coeficiente de confiabilidade derivado de P (mapa decrescente)
            if p == float('inf'):
                C = 0.0
            else:
                C = math.exp(-p)  # confiabilidade entre 0 e >0 (quanto maior P, menor C)
            p_list.append(p)
            a_list.append(a)
            c_list.append(C)
            st.caption(f"Magnitude P: {p:.3f}")
            st.caption(f"Coef. Confiab. C = e^(-P): {C:.4f}")

            # Exibir imagem do motor (placeholder). Substitua pelos arquivos reais.
            img_path = Path(image_paths[i])
            if img_path.exists():
                st.image(str(img_path), use_column_width=True, caption=f"Motor - {s}")
            else:
                st.image("https://via.placeholder.com/300x180.png?text=Motor+" + s, use_column_width=True, caption=f"Motor - {s} (placeholder)")

    # Cálculo da média ponderada por alpha
    sum_alpha = sum(a_list) if sum(a_list) != 0 else 1.0
    c_global = sum(ci * ai for ci, ai in zip(c_list, a_list)) / sum_alpha

    stat_g, cor_g, _ = get_status_visual(-math.log(c_global) if c_global>0 else float('inf'))

    st.markdown(f"""
    <div style="text-align: center; padding: 24px; background: {cor_g}10; border: 2px solid {cor_g}; border-radius: 12px;">
        <h3 style="margin:0;">Coeficiente Global de Confiabilidade</h3>
        <h1 style="font-size: 3em; color: {cor_g};">{c_global:.4f}</h1>
        <p style="font-weight:bold; color: {cor_g}; text-transform:uppercase;">{stat_g}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Interpretação:** calculamos primeiro os coeficientes de confiabilidade individuais \(C_i = e^{-P_i}\). Em seguida, ponderamos cada \(C_i\) por seu respectivo estresse/tempo \(\\alpha_i\) e dividimos pela soma total de \(\\alpha_i\), obtendo a média ponderada em relação aos sistemas totais.")

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

elif pagina == "📘 Exemplos de Aplicação":
    st.markdown("<h2 class='gradient-text'>Exemplos de Aplicação da Fórmula NERO</h2>", unsafe_allow_html=True)
    st.write("Abaixo há exemplos numéricos que mostram passo a passo como aplicar a equação e como obter a média ponderada de confiabilidade.")

    st.markdown("### Exemplo 1 — Três subsistemas (simples)")
    st.write("Parâmetros de entrada (Falhas/Ano): [2, 4, 6]; uso diário 8h; dias sem manutenção fixos para comparação.")
    falhas_ex = [2, 4, 6]
    uso_min_ex = 8 * 60
    dias_min_ex = 60 * 1440

    P_vals = []
    alpha_vals = []
    C_vals = []
    for f in falhas_ex:
        p, _, a, _ = calcular_nero(f, uso_min_ex, dias_min_ex)
        P_vals.append(p)
        alpha_vals.append(a)
        C_vals.append(math.exp(-p) if p != float('inf') else 0.0)

    st.write("Magnitudes P:", [round(v, 4) if v != float('inf') else "∞" for v in P_vals])
    st.write("Alfas (α):", [round(a, 4) for a in alpha_vals])
    st.write("Coeficientes de Confiabilidade C = e^{-P}:", [round(c, 6) for c in C_vals])

    c_global_ex = sum(ci * ai for ci, ai in zip(C_vals, alpha_vals)) / (sum(alpha_vals) if sum(alpha_vals)!=0 else 1.0)
    st.markdown(f"**C_global = (Σ C_i · α_i) / (Σ α_i) = {c_global_ex:.6f}**")

    st.markdown("### Exemplo 2 — Interpretação prática")
    st.write("Se C_global = 0.85, isso indica que, em média ponderada pelo estresse (α), o sistema tem 85% de confiabilidade relativa segundo a métrica NERO. Valores menores indicam maior risco agregado.")

    st.info("Substitua os exemplos por dados reais do seu parque para obter diagnósticos práticos. As imagens de motores na aba de sistemas complexos são placeholders; troque pelos arquivos reais em 'motors/'.")

# --- FIM ---



