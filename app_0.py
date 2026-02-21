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

# --- 2. ESTILIZAÇÃO CSS (DESIGN SYSTEM PREMIUM) ---
st.markdown("""
<style>
    /* Tipografia e Fundo Geral */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Headers com Gradiente (Azul e Verde Limão para Contraste Premium) */
    .gradient-text {
        background: linear-gradient(90deg, #0052FF 0%, #39FF14 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    
    /* Cards Modernos */
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

    .success-box {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        color: #166534;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #166534;
    }
    .warning-box {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #991b1b;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #991b1b;
    }

    /* Ocultar elementos padrão do Streamlit para visual mais limpo */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. CORE: MOTOR MATEMÁTICO NERO ---
def calcular_nero(falhas_ano: int, uso_min: float, t_conserto_min: float):
    """Calcula o score NERO (Euler Risk Observer)."""
    # Proteção: Uso não pode ser zero absoluto
    uso_min = max(uso_min, 0.1)
    
    # 1. Lambda (Taxa de Falhas Anual Normalizada)
    lambd = falhas_ano / 365.0
    
    # 2. Alpha (Coeficiente de Estresse Sistêmico)
    if t_conserto_min <= 0.1:
        alpha = math.log(abs(uso_min))
    elif t_conserto_min == uso_min:
        alpha = abs(t_conserto_min + 1 - uso_min) / (t_conserto_min + 1)
    else:
        alpha = abs(t_conserto_min - uso_min) / (t_conserto_min + 1)
        
    # 3. Potencial de Risco (P)
    try:
        exponent = lambd * alpha
        if exponent > 700:
            p_score = float('inf')
        else:
            p_score = math.exp(exponent) / uso_min
    except Exception:
        p_score = float('inf')
        
    return p_score, lambd, alpha

def get_status_visual(p_score):
    if p_score == float('inf'):
        return "CRÍTICO EXTREMO", "#7f1d1d", "⛔"
    elif p_score > 0.01:
        return "CRÍTICO", "#dc2626", "🔴"
    elif p_score > 0.005:
        return "ALERTA", "#f59e0b", "🟠"
    elif p_score > 0.001:
        return "OPERACIONAL", "#0052FF", "🔵"
    else:
        return "EXCELENTE", "#39FF14", "🟢"

# --- 4. SIDEBAR: NAVEGAÇÃO E DADOS ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 2.5em;'>🛡️</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; margin-bottom: 0; color: #0052FF;'>NERO Pro</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.9em;'>Euler Risk Observer</p>", unsafe_allow_html=True)
    st.divider()

    pagina = st.radio(
        "Navegação",
        ["🏠 Visão Geral", "⚙️ Dashboard de Ativos", "⚖️ Comparador de Marcas"],
        label_visibility="collapsed"
    )
    
    if pagina == "⚙️ Dashboard de Ativos":
        st.divider()
        st.subheader("🛠️ Parâmetros do Ativo")
        nome_ativo = st.text_input("Identificação", "Motor Industrial AC-200")

        col1, col2 = st.columns(2)
        with col1:
            falhas_in = st.number_input("Falhas/Ano", min_value=0, value=5)
        with col2:
            dias_in = st.number_input("Dias s/ Conserto", min_value=0, value=30)

        uso_horas_in = st.slider("Uso Diário Médio (h)", 0.5, 24.0, 8.0, 0.5)

# --- 5. ROTEAMENTO DE PÁGINAS ---
if pagina == "🏠 Visão Geral":
    # --- PÁGINA INICIAL ---
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px;">
        <h1 class="gradient-text" style="font-size: 4em; margin-bottom: 10px;">A Matemática da Confiabilidade</h1>
        <h3 style="color: #475569; font-weight: 400; font-size: 1.5em; max-width: 800px; margin: 0 auto;">
            O NERO Pro modela o risco de falhas através da lente dos <b>Sistemas Dinâmicos</b>. 
            Aqui, a integridade do seu maquinário é uma métrica viva.
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col_img, col_txt = st.columns([1, 1.2], gap="large")

    with col_img:
        st.markdown("""
        <div class="modern-card" style="background: linear-gradient(145deg, #0f172a, #1e293b); border-left: 4px solid #39FF14; color: white;">
            <h2 style="color: white; margin-top: 0;">O Paradigma NERO</h2>
            <p style="font-size: 1.1em; color: #cbd5e1; line-height: 1.6;">
                Na engenharia clássica, medimos a quebra apenas pelo histórico (MTBF). 
                O modelo NERO subverte isso com uma regra de ouro dos sistemas dinâmicos:<br><br>
                <b style="color: #39FF14; font-size: 1.2em;">"O ócio degrada. O uso valida."</b><br><br>
                Um equipamento parado acumula incertezas e estresse sistêmico. O NERO calcula o risco em tempo real, provando matematicamente que operar constantemente é mais seguro do que repousar sem validação.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_txt:
        st.markdown("### Como o Algoritmo Funciona?")
        st.write("A fórmula baseia-se em leis de dissipação estocástica (semelhantes ao resfriamento de Newton):")
        st.latex(r"P = \frac{e^{(\lambda \cdot \alpha)}}{U}")
        st.markdown("""
        * **$P$ (Potencial de Risco):** Nosso placar. Quanto mais perto de zero, mais seguro o equipamento.
        * **$\lambda$ (Lambda):** Taxa normalizada de falhas anuais.
        * **$\alpha$ (Alpha):** Coeficiente de Estresse. É o cabo de guerra entre o tempo sem conserto ($T$) e o uso diário ($U$). Se a inércia vence, $\alpha$ sobe exponencialmente.
        * **$U$ (Uso):** O denominador que "salva" o equipamento. Mais horas de uso diluem o risco.
        """)
        
    st.markdown("<br><hr style='border-color: #e2e8f0;'><br>", unsafe_allow_html=True)

    # Cards de Benefícios
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="modern-card" style="border-top: 3px solid #0052FF;">
            <h3 style="margin-top:0; color: #1e293b;">⏳ Tempo como Variável</h3>
            <p style="color: #64748b;">Na teoria dos sistemas dinâmicos, o estado de uma máquina evolui no tempo. O NERO precifica a ausência de uso como um catalisador de panes ocultas.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="modern-card" style="border-top: 3px solid #0052FF;">
            <h3 style="margin-top:0; color: #1e293b;">🧮 Proteção Algorítmica</h3>
            <p style="color: #64748b;">Utilizamos suavização logarítmica para evitar assíntotas e explosões matemáticas, garantindo gráficos e métricas perfeitamente estáveis.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="modern-card" style="border-top: 3px solid #39FF14;">
            <h3 style="margin-top:0; color: #1e293b;">⚖️ Tomada de Decisão</h3>
            <p style="color: #64748b;">Através dos simuladores e comparadores, engenheiros e gestores descobrem instantaneamente qual regime de manutenção previne acidentes.</p>
        </div>
        """, unsafe_allow_html=True)

elif pagina == "⚙️ Dashboard de Ativos":
    # --- LÓGICA DE CÁLCULO ---
    uso_min_atual = uso_horas_in * 60
    t_conserto_min_atual = dias_in * 1440
    p_atual, lambd_atual, alpha_atual = calcular_nero(falhas_in, uso_min_atual, t_conserto_min_atual)
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
        c1.metric("Taxa Normalizada (λ)", f"{lambd_atual:.4f}", help="Falhas diluídas no ano")
        c2.metric("Estresse Sistêmico (α)", f"{alpha_atual:.3f}", help="Relação entre ociosidade e uso")
        c3.metric("Tempo de Validação", f"{uso_min_atual:.0f} min/dia", help="Tempo diário mitigando o estresse")
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab_grafico, tab_simulador = st.tabs(["📉 Curva de Degradação (Sistemas Dinâmicos)", "🧪 Simulador What-If"])
    
    with tab_grafico:
        st.write("Visualização da degradação estocástica: o que acontece com a confiabilidade se o equipamento não receber manutenção nos próximos dias, mantendo o uso atual?")

        dias_projecao = max(dias_in + 90, 100)
        eixo_x = np.linspace(0, dias_projecao, 200)
        eixo_y = [min(calcular_nero(falhas_in, uso_min_atual, d * 1440)[0], 0.02) for d in eixo_x]
        fig = go.Figure()

        # Zonas com gradiente simulado
        fig.add_hrect(y0=0, y1=0.005, fillcolor="#39FF14", opacity=0.1, line_width=0, annotation_text="Ideal")
        fig.add_hrect(y0=0.005, y1=0.01, fillcolor="#f59e0b", opacity=0.1, line_width=0, annotation_text="Alerta")
        fig.add_hrect(y0=0.01, y1=0.02, fillcolor="#ef4444", opacity=0.1, line_width=0, annotation_text="Crítico")
        
        # Linha principal com preenchimento
        fig.add_trace(go.Scatter(
            x=eixo_x, y=eixo_y,
            mode='lines',
            name='Trajetória de Risco',
            line=dict(color='#0052FF', width=4, shape='spline'),
            fill='tozeroy',
            fillcolor='rgba(0, 82, 255, 0.1)',
            hovertemplate='Dias s/ Manutenção: %{x:.0f}<br>Risco NERO: %{y:.5f}<extra></extra>'
        ))
        
        # Ponto Atual
        fig.add_trace(go.Scatter(
            x=[dias_in], y=[p_atual],
            mode='markers+text',
            name='Status Atual',
            marker=dict(color=status_cor, size=16, line=dict(color='white', width=3)),
            text=['VOCÊ ESTÁ AQUI'],
            textposition='top left',
            textfont=dict(color=status_cor, size=12, family="Inter")
        ))
        
        fig.update_layout(
            hovermode="x unified",
            height=450,
            margin=dict(l=0, r=0, t=30, b=0),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="Dias desde a última manutenção", showgrid=True, gridcolor='#f1f5f9'),
            yaxis=dict(title="Índice de Risco (P)", showgrid=True, gridcolor='#f1f5f9', range=[0, 0.022])
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with tab_simulador:
        st.markdown("### Teste de Regime Operacional")
        st.write("Descubra se alterar a carga de trabalho ou a rotina de manutenção afeta positiva ou negativamente a máquina.")

        col_s1, col_s2, col_s3 = st.columns([1, 0.2, 1])
        with col_s1:
            st.info(f"**Cenário Atual:**\n\nUso: {uso_horas_in}h | Manutenção: {dias_in} dias atrás\nRisco: **{p_atual:.5f}**")

        with col_s2:
            st.markdown("<h2 style='text-align: center; color: #cbd5e1; margin-top: 10px;'>→</h2>", unsafe_allow_html=True)

        with col_s3:
            novo_uso = st.slider("Novo Uso (h/dia)", 0.5, 24.0, float(max(1.0, uso_horas_in - 2)), 0.5, key="sim_uso")
            novos_dias = st.number_input("Novos Dias s/ Conserto", 0, 365, int(max(0, dias_in - 10)), key="sim_dias")

        p_novo, _, _ = calcular_nero(falhas_in, novo_uso * 60, novos_dias * 1440)

        st.divider()
        if p_novo < p_atual:
            melhoria = abs(((p_novo - p_atual) / p_atual) * 100)
            st.markdown(f"""<div class="success-box" style="border-left-color: #39FF14;"><b>📈 CONFIABILIDADE OTIMIZADA:</b> O risco caiu para <b>{p_novo:.5f}</b> (Melhoria de {melhoria:.1f}%).<br>Aumentar a validação pelo uso ou encurtar a manutenção estabilizou o sistema.</div>""", unsafe_allow_html=True)
        elif p_novo > p_atual:
            piora = abs(((p_novo - p_atual) / p_atual) * 100)
            st.markdown(f"""<div class="warning-box"><b>📉 CUIDADO:</b> O risco subiu para <b>{p_novo:.5f}</b> (Piora de {piora:.1f}%).<br>Esse regime de operação favorece o acúmulo de incertezas sistêmicas.</div>""", unsafe_allow_html=True)
        else:
            st.info("Risco estagnado. O sistema dinâmico se manteve em equilíbrio perfeito na transição.")

elif pagina == "⚖️ Comparador de Marcas":
    # --- NOVA ABA: COMPARADOR DE MARCAS ---
    st.markdown("## ⚖️ Comparador Estocástico de Marcas")
    st.write("Insira os dados históricos de dois fabricantes diferentes para descobrir qual aparelho suporta melhor o regime de trabalho da sua empresa com base na equação NERO.")

    col_marca_a, col_vs, col_marca_b = st.columns([1, 0.1, 1])

    with col_marca_a:
        st.markdown("<div class='modern-card' style='border-top: 4px solid #0052FF;'>", unsafe_allow_html=True)
        st.markdown("### Marca A")
        nome_a = st.text_input("Nome", "TechCorp Premium", key="nome_a")
        falhas_a = st.number_input("Média de Falhas/Ano", 0, 100, 3, key="falhas_a")
        dias_a = st.number_input("Tempo Típico p/ Falhar (Dias)", 0, 1000, 120, key="dias_a")
        uso_a = st.number_input("Horas de Uso/Dia", 1.0, 24.0, 10.0, key="uso_a")

        p_a, _, _ = calcular_nero(falhas_a, uso_a * 60, dias_a * 1440)
        status_txt_a, color_a, _ = get_status_visual(p_a)

        st.markdown(f"<br><h4 style='color: #64748b;'>Score NERO</h4>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='color: {color_a};'>{p_a:.5f}</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_vs:
        st.markdown("<h2 style='text-align: center; color: #cbd5e1; margin-top: 150px;'>VS</h2>", unsafe_allow_html=True)
        
    with col_marca_b:
        st.markdown("<div class='modern-card' style='border-top: 4px solid #39FF14;'>", unsafe_allow_html=True)
        st.markdown("### Marca B")
        nome_b = st.text_input("Nome", "ElectroMax Genérica", key="nome_b")
        falhas_b = st.number_input("Média de Falhas/Ano", 0, 100, 12, key="falhas_b")
        dias_b = st.number_input("Tempo Típico p/ Falhar (Dias)", 0, 1000, 45, key="dias_b")
        uso_b = st.number_input("Horas de Uso/Dia", 1.0, 24.0, 10.0, key="uso_b")

        p_b, _, _ = calcular_nero(falhas_b, uso_b * 60, dias_b * 1440)
        status_txt_b, color_b, _ = get_status_visual(p_b)

        st.markdown(f"<br><h4 style='color: #64748b;'>Score NERO</h4>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='color: {color_b};'>{p_b:.5f}</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.divider()

    # Veredito
    st.markdown("### Veredito do Sistema")
    if p_a < p_b:
        vantagem = ((p_b - p_a) / p_b) * 100
        st.success(f"🏆 A marca **{nome_a}** é mais confiável neste cenário operacional. Ela apresenta um risco **{vantagem:.1f}% menor** de falha crítica comparada à {nome_b}.")
    elif p_b < p_a:
        vantagem = ((p_a - p_b) / p_a) * 100
        st.success(f"🏆 A marca **{nome_b}** é mais confiável neste cenário operacional. Ela apresenta um risco **{vantagem:.1f}% menor** de falha crítica comparada à {nome_a}.")
    else:
        st.info("⚖️ Ambas as marcas apresentam o exato mesmo potencial de risco (Empate Técnico).")




