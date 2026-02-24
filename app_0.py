import streamlit as st
import math
import plotly.graph_objects as go
import numpy as np

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="NERO Pro: Risk Observer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILIZAÇÃO CSS (DESIGN VIBRANTE E SIDEBAR LARANJA) ---
st.markdown("""
<style>
    /* Tipografia e Fundo Geral */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Customização da Sidebar para Laranja */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FF6B00 0%, #FF9500 100%) !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Headers com Gradiente Multicolorido */
    .gradient-text {
        background: linear-gradient(90deg, #FF6B00 0%, #9C27B0 50%, #FF1493 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    /* Cards Modernos e Coloridos */
    .modern-card {
        background: #ffffff;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
    }
    .modern-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    /* Containers de Status (Sucesso/Aviso/Crítico) */
    .status-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    
    /* Ocultar elementos padrão do Streamlit para visual mais limpo */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. MOTOR MATEMÁTICO NERO V6 (NOTAÇÃO DE PUREZA SINGULAR) ---
def calcular_nero(falhas_ano: int, uso_min: float, t_conserto_min: float):
    """Calcula o score NERO com a ponderação de estresse sobre o uso e função Gamma."""
    uso_min = max(uso_min, 0.1)

    # 1. Lambda (Taxa de Falhas Anual Normalizada)
    lambd = falhas_ano / 365.0

    # 2. Alpha (Coeficiente de Estresse Sistêmico)
    # Calculada como a razão normalizada para tender a 1 no limite crítico
    alpha = t_conserto_min / (t_conserto_min + uso_min)

    # Mantemos a variável de uso_efetivo para os dashboards
    uso_efetivo = uso_min / (alpha + 1)

    # 3. Potencial de Risco (P) - Motor Atualizado
    try:
        exponent = lambd * alpha
        if exponent > 700:
            p_score = float('inf')
        else:
            # Numerador: e^(lambda * alpha)
            # Denominador: U * Gamma(alpha + 1)^-1  => o mesmo que multiplicar por Gamma(alpha + 1)
            p_score = (math.exp(exponent) * math.gamma(alpha + 1)) / uso_min
    except Exception:
        p_score = float('inf')

    return p_score, lambd, alpha, uso_efetivo

def get_status_visual(p_score):
    if p_score == float('inf'):
        return "CRÍTICO EXTREMO", "#7f1d1d", "⛔"
    elif p_score >= 0.1:
        return "CRÍTICO (Início do Colapso)", "#dc2626", "🔴"
    elif p_score >= 0.01:
        return "ALERTA", "#FF9500", "🟠"
    elif p_score >= 0.001:
        return "OPERACIONAL", "#9C27B0", "🟣"
    else:
        return "EXCELENTE", "#00C853", "🟢"

# --- 4. SIDEBAR: NAVEGAÇÃO E DADOS ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 2.5em;'>🛡️</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; margin-bottom: 0;'>NERO Pro</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.9em; opacity: 0.8;'>Euler Risk Observer</p>", unsafe_allow_html=True)
    st.divider()
    
    pagina = st.radio(
        "Navegação",
        ["🏠 Visão Geral", "⚙️ Dashboard de Ativos", "🚀 Sistemas Complexos (Aeronaves/Veículos)", "⚖️ Comparador de Marcas"],
        label_visibility="collapsed"
    )

    if pagina == "⚙️ Dashboard de Ativos":
        st.divider()
        st.subheader("🛠️ Parâmetros do Ativo")
        nome_ativo = st.text_input("Identificação", "Motor VW EA111 (1.6)")
        col1, col2 = st.columns(2)
        with col1:
            falhas_in = st.number_input("Falhas/Ano", min_value=0, value=3)
        with col2:
            dias_in = st.number_input("Dias s/ Conserto", min_value=0, value=180)
        uso_horas_in = st.slider("Uso Diário Médio (h)", 0.5, 24.0, 0.5, 0.5)

# --- 5. ROTEAMENTO DE PÁGINAS ---
if pagina == "🏠 Visão Geral":
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px;">
        <h1 class="gradient-text" style="font-size: 4em; margin-bottom: 10px;">A Matemática da Confiabilidade</h1>
        <h3 style="color: #475569; font-weight: 400; font-size: 1.5em; max-width: 800px; margin: 0 auto;">
            O NERO Pro modela o risco de falhas através da lente dos <b>Sistemas Dinâmicos</b>. A integridade do seu maquinário não é baseada em histórico, mas em estresse em tempo real.
        </h3>
    </div>
    """, unsafe_allow_html=True)

    col_img, col_txt = st.columns([1, 1.2], gap="large")
    with col_img:
        st.markdown("""
        <div class="modern-card" style="background: linear-gradient(145deg, #1e1e1e, #2d2d2d); border-left: 4px solid #FF6B00; color: white;">
            <h2 style="color: white; margin-top: 0;">O Paradigma NERO</h2>
            <p style="font-size: 1.1em; color: #cbd5e1; line-height: 1.6;">
                Na engenharia clássica, o uso constante é sempre visto como desgaste. No modelo NERO original, o uso é validação. Mas a vida real exige uma ponderação perfeita:<br><br>
                <b style="color: #FF6B00; font-size: 1.2em;">"O estresse devora a validação."</b><br><br>
                Se uma máquina está com manutenção atrasada, o tempo de uso deixa de ser um certificado de saúde e passa a acelerar a degradação sistêmica.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_txt:
        st.markdown("### Como o Algoritmo Funciona?")
        st.write("A nossa equação exclusiva pondera o benefício do uso pela Notação de Pureza Singular:")
        st.latex(r"P = \frac{e^{(\lambda \cdot \alpha)}}{U \cdot \Gamma(\alpha + 1)^{-1}}")
        st.markdown("""
        * **$P$ (Potencial de Risco):** O placar de segurança. Próximo a zero é ideal.
        * **$\lambda$ (Lambda):** Taxa normalizada de falhas anuais.
        * **$\alpha$ (Alpha):** Coeficiente de Estresse Sistêmico (Razão normalizada de fadiga).
        * **$\Gamma(\alpha + 1)$:** O ajuste de fadiga gama avaliando a estabilidade da máquina.
        """)

elif pagina == "🚀 Sistemas Complexos (Aeronaves/Veículos)":
    st.markdown("<h2 class='gradient-text'>Confiabilidade Global de Sistemas Eletromecânicos</h2>", unsafe_allow_html=True)
    st.write("""
    Para sistemas compostos, a falha global ($P_{total}$) é a **média ponderada** dos riscos individuais ($P_i$), utilizando o estresse sistêmico ($\\alpha_i$) como peso. O subsistema mais estressado domina a saúde geral da máquina.
    """)
    
    st.latex(r"P_{total} = \frac{\sum_{i=1}^{n} (P_i \cdot \alpha_i)}{\sum_{i=1}^{n} \alpha_i}")
    
    st.markdown("### Simulador de Veículos / Frotas")
    
    sistemas = ["Motor Principal (Ex: Bloco/Turbina)", "Sistema de Lubrificação/Hidráulico", "Sistemas Elétricos / Sensores"]
    resultados = []
    
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    
    for i, sys_name in enumerate(sistemas):
        with cols[i]:
            st.markdown(f"<div class='modern-card' style='border-top: 4px solid #FF1493;'>", unsafe_allow_html=True)
            st.markdown(f"#### {sys_name}")
            f_ano = st.number_input(f"Falhas/Ano", 0, 50, 1 + i*2, key=f"f_{i}")
            d_conserto = st.number_input(f"Dias s/ Manut.", 0, 365, 45 + i*45, key=f"d_{i}")
            u_diario = st.slider(f"Uso/Dia (h)", 0.5, 24.0, 8.0, key=f"u_{i}")
            
            p, l, a, u_efetivo = calcular_nero(f_ano, u_diario * 60, d_conserto * 1440)
            resultados.append({'p': p, 'alpha': a, 'nome': sys_name})
            
            status, cor, icon = get_status_visual(p)
            st.markdown(f"<p style='color:{cor}; font-weight:bold;'>Score P: {p:.5f}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#64748b;'>Peso (α): {a:.3f}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
    soma_p_alpha = sum(r['p'] * r['alpha'] for r in resultados)
    soma_alpha = sum(r['alpha'] for r in resultados)
    p_global = soma_p_alpha / soma_alpha if soma_alpha > 0 else 0
    
    st.divider()
    stat_g, cor_g, icon_g = get_status_visual(p_global)
    st.markdown(f"""
    <div style="text-align: center; padding: 30px; background: {cor_g}15; border-radius: 16px; border: 2px solid {cor_g};">
        <h3 style="margin:0; color: #1e293b;">Risco Global do Sistema Ponderado por Estresse (α)</h3>
        <h1 style="font-size: 4em; color: {cor_g}; margin: 10px 0;">{p_global:.5f}</h1>
        <span class="status-badge" style="background: {cor_g}; color: white;">{icon_g} STATUS GLOBAL: {stat_g}</span>
    </div>
    """, unsafe_allow_html=True)

elif pagina == "⚙️ Dashboard de Ativos":
    # --- LÓGICA DE CÁLCULO ---
    uso_min_atual = uso_horas_in * 60
    t_conserto_min_atual = dias_in * 1440
    p_atual, lambd_atual, alpha_atual, uso_efetivo_atual = calcular_nero(falhas_in, uso_min_atual, t_conserto_min_atual)
    status_txt, status_cor, status_icon = get_status_visual(p_atual)

    # --- HEADER DO DASHBOARD ---
    st.markdown(f"## Análise em Tempo Real: **{nome_ativo}**")
    col_kpi, col_info = st.columns([1, 2.5])
    
    with col_kpi:
        st.markdown(f"""
        <div class="modern-card" style="border-top: 6px solid {status_cor}; text-align: center;">
            <p style="color: #64748b; font-size: 0.9em; font-weight: 600; text-transform: uppercase; margin: 0;">Índice NERO (P)</p>
            <h2 style="font-size: 2.5em; color: #1e293b; margin: 10px 0;">{p_atual:.5f}</h2>
            <div style="background: {status_cor}20; color: {status_cor};" class="status-badge">
                {status_icon} {status_txt}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_info:
        st.markdown("<div class='modern-card'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Taxa Normalizada (λ)", f"{lambd_atual:.4f}")
        c2.metric("Estresse Sistêmico (α)", f"{alpha_atual:.3f}")
        c3.metric("Uso Efetivo (Ponderado)", f"{uso_efetivo_atual:.0f} min/dia", help="O uso real mitigando o risco, descontado o estresse α.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab_grafico, tab_simulador = st.tabs(["📉 Curva de Degradação", "🧪 Simulador What-If"])

    with tab_grafico:
        st.write("Visualização da degradação estocástica: o que acontece se o equipamento continuar operando sem manutenção nos próximos dias?")
        dias_projecao = max(dias_in + 90, 100)
        eixo_x = np.linspace(0, dias_projecao, 200)
        # Ajustado para visualizar a nova escala mais precisa do P
        eixo_y = [min(calcular_nero(falhas_in, uso_min_atual, d * 1440)[0], 0.15) for d in eixo_x]
        
        fig = go.Figure()
        fig.add_hrect(y0=0, y1=0.001, fillcolor="#00C853", opacity=0.1, line_width=0, annotation_text="Excelente")
        fig.add_hrect(y0=0.001, y1=0.01, fillcolor="#9C27B0", opacity=0.1, line_width=0, annotation_text="Operacional")
        fig.add_hrect(y0=0.01, y1=0.1, fillcolor="#FF9500", opacity=0.1, line_width=0, annotation_text="Alerta")
        fig.add_hrect(y0=0.1, y1=0.15, fillcolor="#dc2626", opacity=0.1, line_width=0, annotation_text="Crítico")

        fig.add_trace(go.Scatter(
            x=eixo_x, y=eixo_y, mode='lines', name='Trajetória de Risco',
            line=dict(color='#FF6B00', width=4, shape='spline'),
            fill='tozeroy', fillcolor='rgba(255, 107, 0, 0.1)',
            hovertemplate='Dias s/ Manutenção: %{x:.0f}<br>Risco NERO: %{y:.5f}<extra></extra>'
        ))

        fig.add_trace(go.Scatter(
            x=[dias_in], y=[p_atual], mode='markers+text', name='Status Atual',
            marker=dict(color=status_cor, size=16, line=dict(color='white', width=3)),
            text=['VOCÊ ESTÁ AQUI'], textposition='top left', textfont=dict(color=status_cor, size=12)
        ))

        fig.update_layout(
            hovermode="x unified", height=450, margin=dict(l=0, r=0, t=30, b=0),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="Dias desde a última manutenção", showgrid=True, gridcolor='#f1f5f9'),
            yaxis=dict(title="Índice de Risco (P)", showgrid=True, gridcolor='#f1f5f9', range=[0, 0.15])
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab_simulador:
        st.markdown("### Teste de Regime Operacional")
        col_s1, col_s2, col_s3 = st.columns([1, 0.2, 1])
        with col_s1:
            st.info(f"**Cenário Atual:**\n\nUso: {uso_horas_in}h | Manut.: {dias_in} dias atrás\nRisco: **{p_atual:.5f}**")
        with col_s2:
            st.markdown("<h2 style='text-align: center; color: #cbd5e1; margin-top: 10px;'>→</h2>", unsafe_allow_html=True)
        with col_s3:
            novo_uso = st.slider("Novo Uso (h/dia)", 0.5, 24.0, float(max(1.0, uso_horas_in - 2)), 0.5, key="sim_uso")
            novos_dias = st.number_input("Novos Dias s/ Conserto", 0, 365, int(max(0, dias_in - 10)), key="sim_dias")
            
        p_novo, _, _, _ = calcular_nero(falhas_in, novo_uso * 60, novos_dias * 1440)
        st.divider()
        if p_novo < p_atual:
            melhoria = abs(((p_novo - p_atual) / p_atual) * 100)
            st.markdown(f"""<div class="success-box"><b>📈 CONFIABILIDADE OTIMIZADA:</b> Risco caiu para <b>{p_novo:.5f}</b> (Melhoria de {melhoria:.1f}%).</div>""", unsafe_allow_html=True)
        elif p_novo > p_atual:
            piora = abs(((p_novo - p_atual) / p_atual) * 100)
            st.markdown(f"""<div class="warning-box"><b>📉 CUIDADO:</b> Risco subiu para <b>{p_novo:.5f}</b> (Piora de {piora:.1f}%). Como o estresse penaliza o uso efetivo, o regime escolhido prejudica a máquina.</div>""", unsafe_allow_html=True)

elif pagina == "⚖️ Comparador de Marcas":
    st.markdown("## ⚖️ Comparador Estocástico de Marcas")
    st.write("Insira os dados de duas marcas submetidas ao mesmo cenário. A ponderação avançada do NERO mostrará qual delas resiste melhor à fadiga e perda de lubrificação.")
    
    col_marca_a, col_vs, col_marca_b = st.columns([1, 0.1, 1])
    
    with col_marca_a:
        st.markdown("<div class='modern-card' style='border-top: 4px solid #FF6B00;'>", unsafe_allow_html=True)
        st.markdown("### Marca A")
        nome_a = st.text_input("Nome", "TechCorp Premium", key="nome_a")
        falhas_a = st.number_input("Média de Falhas/Ano", 0, 100, 3, key="falhas_a")
        dias_a = st.number_input("Tempo Típico p/ Falhar (Dias)", 0, 1000, 120, key="dias_a")
        uso_a = st.number_input("Horas de Uso/Dia", 1.0, 24.0, 10.0, key="uso_a")
        p_a, _, _, _ = calcular_nero(falhas_a, uso_a * 60, dias_a * 1440)
        status_txt_a, color_a, _ = get_status_visual(p_a)
        st.markdown(f"<br><h4 style='color: #64748b;'>Score NERO</h4><h2 style='color: {color_a};'>{p_a:.5f}</h2></div>", unsafe_allow_html=True)

    with col_vs:
        st.markdown("<h2 style='text-align: center; color: #cbd5e1; margin-top: 150px;'>VS</h2>", unsafe_allow_html=True)

    with col_marca_b:
        st.markdown("<div class='modern-card' style='border-top: 4px solid #9C27B0;'>", unsafe_allow_html=True)
        st.markdown("### Marca B")
        nome_b = st.text_input("Nome", "ElectroMax Genérica", key="nome_b")
        falhas_b = st.number_input("Média de Falhas/Ano", 0, 100, 12, key="falhas_b")
        dias_b = st.number_input("Tempo Típico p/ Falhar (Dias)", 0, 1000, 45, key="dias_b")
        uso_b = st.number_input("Horas de Uso/Dia", 1.0, 24.0, 10.0, key="uso_b")
        p_b, _, _, _ = calcular_nero(falhas_b, uso_b * 60, dias_b * 1440)
        status_txt_b, color_b, _ = get_status_visual(p_b)
        st.markdown(f"<br><h4 style='color: #64748b;'>Score NERO</h4><h2 style='color: {color_b};'>{p_b:.5f}</h2></div>", unsafe_allow_html=True)

    st.divider()
    if p_a < p_b:
        st.success(f"🏆 A marca **{nome_a}** lida melhor com o estresse (α).")
    elif p_b < p_a:
        st.success(f"🏆 A marca **{nome_b}** lida melhor com o estresse (α).")
    else:
        st.info("⚖️ Empate técnico.")
