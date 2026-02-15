import streamlit as st
import math
import plotly.graph_objects as go
import numpy as np

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="NERO: Risk Observer Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILIZAÇÃO CSS (DESIGN SYSTEM PREMIUM) ---
st.markdown("""
<style>
    /* Containers de Métricas */
    div[data-testid="metric-container"] {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    /* Destaque para resultados positivos */
    .success-box {
        background-color: #dcfce7;
        color: #166534;
        padding: 20px;
        border-radius: 10px;
        border-left: 8px solid #166534;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Destaque para resultados negativos */
    .warning-box {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 20px;
        border-radius: 10px;
        border-left: 8px solid #991b1b;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Títulos */
    h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; color: #1e293b; }
    
    /* Cards da Home */
    .home-card {
        background: white;
        padding: 25px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        height: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CORE: MOTOR MATEMÁTICO NERO ---

def calcular_nero(falhas_ano: int, uso_min: float, t_conserto_min: float):
    """
    Calcula o score NERO (Euler Risk Observer).
    Fórmula base: P = (e^(lambda * alpha)) / U
    """
    # Proteção: Uso não pode ser zero absoluto para evitar divisão por zero
    if uso_min <= 0.1: 
        uso_min = 0.1 
    
    # 1. Lambda (Taxa de Falhas Anual Normalizada)
    lambd = falhas_ano / 365.0
    
    # 2. Alpha (Coeficiente de Estresse Sistêmico)
    # AJUSTE MATEMÁTICO: Limite Tc -> 0 (Suavização Logarítmica)
    if t_conserto_min <= 0.1: # Considerado limite tendendo a zero
        # Tira-se o ln do módulo de U para evitar explosão numérica e achatar a curva suavemente
        alpha = math.log(abs(uso_min)) 
    elif t_conserto_min == uso_min:
        alpha = abs(t_conserto_min + 1 - uso_min) / (t_conserto_min + 1)
    else:
        alpha = abs(t_conserto_min - uso_min) / (t_conserto_min + 1)
    
    # 3. Potencial de Risco (P)
    try:
        exponent = lambd * alpha
        # Proteção contra Overflow matemático (números astronômicos)
        if exponent > 700: 
            p_score = float('inf')
        else:
            p_score = math.exp(exponent) / uso_min
    except Exception:
        p_score = float('inf')
        
    return p_score, lambd, alpha

def get_status_visual(p_score):
    """Retorna metadados visuais baseados no risco NERO (Quanto mais perto de 0, melhor)."""
    if p_score == float('inf'):
        return "CRÍTICO EXTREMO", "#991b1b", "⛔"
    elif p_score > 0.01:
        return "CRÍTICO", "#dc2626", "🔴"
    elif p_score > 0.005:
        return "ALERTA", "#f59e0b", "🟠"
    elif p_score > 0.001:
        return "OPERACIONAL", "#3b82f6", "🔵"
    else:
        return "EXCELENTE", "#10b981", "🟢"


# --- 4. SIDEBAR: NAVEGAÇÃO E DADOS ---

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2091/2091665.png", width=60) # Ícone genérico de escudo/dados
    st.title("NERO Pro")
    st.caption("Euler Risk Observer")
    
    # Navegação entre páginas
    pagina = st.radio("Navegação", ["🏠 Página Inicial", "⚙️ Dashboard NERO"], label_visibility="collapsed")
    
    st.divider()

    if pagina == "⚙️ Dashboard NERO":
        st.subheader("🛠️ Parâmetros do Ativo")
        nome_ativo = st.text_input("Identificação", "Elevador de Alto Tráfego")
        
        col1, col2 = st.columns(2)
        with col1:
            falhas_in = st.number_input("Falhas/Ano", min_value=0, value=15, help="Soma total de panes no período de 365 dias.")
        with col2:
            dias_in = st.number_input("Dias s/ Conserto", min_value=0, value=20, help="Tempo desde a última manutenção corretiva.")
        
        uso_horas_in = st.slider("Uso Diário Médio (h)", 0.5, 24.0, 12.0, 0.5)
        
        st.markdown("---")
        st.info("💡 **Dica:** O modelo penaliza a inatividade. Mais uso contínuo ajuda na auto-validação do sistema.")


# --- 5. ROTEAMENTO DE PÁGINAS ---

if pagina == "🏠 Página Inicial":
    # --- PÁGINA INICIAL ---
    st.markdown("""
        <div style="text-align: center; padding: 40px 0;">
            <h1 style="font-size: 3.5em; margin-bottom: 0; color: #0f172a;">NERO Pro 🛡️</h1>
            <h3 style="color: #64748b; font-weight: 400; margin-top: 10px;">A evolução estocástica na Confiabilidade de Equipamentos</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### O paradigma da Inércia como Estresse")
    st.write("""
    Na engenharia de confiabilidade tradicional (como o MTBF), o risco de falha costuma ser tratado de forma estática e linear. O modelo **NERO (Euler Risk Observer)** subverte essa lógica baseando-se em uma premissa fundamental: **o equipamento ocioso não é um equipamento seguro**. A ausência de uso, na verdade, acumula incertezas e potencializa panes ocultas.
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Cards de Benefícios
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="home-card">
            <h3 style="margin-top:0;">⏳ Dinamismo Temporal</h3>
            <p style="color: #475569;">O tempo ocioso atua como um catalisador no coeficiente de estresse. O modelo calcula o risco de falha em tempo real baseado no desgaste pela ausência de validação operacional.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="home-card">
            <h3 style="margin-top:0;">🧮 Prevenção de Overflow</h3>
            <p style="color: #475569;">Através de <b>suavização logarítmica</b> e limites matemáticos controlados (como quando o tempo sem conserto tende a zero), a fórmula NERO previne explosões numéricas (assíntotas).</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="home-card">
            <h3 style="margin-top:0;">🔄 Simulador What-If</h3>
            <p style="color: #475569;">Permite aos engenheiros testar cenários hipotéticos de carga horária para entender matematicamente qual regime de uso mantém o maquinário na "zona de confiabilidade".</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    st.info("👈 **Comece a análise selecionando '⚙️ Dashboard NERO' no menu lateral esquerdo.**")

elif pagina == "⚙️ Dashboard NERO":
    # --- LÓGICA DE CÁLCULO DO DASHBOARD ---
    uso_min_atual = uso_horas_in * 60
    t_conserto_min_atual = dias_in * 1440

    p_atual, lambd_atual, alpha_atual = calcular_nero(falhas_in, uso_min_atual, t_conserto_min_atual)
    status_txt, status_cor, status_icon = get_status_visual(p_atual)

    # --- HEADER DO DASHBOARD ---
    col_kpi_main, col_kpi_desc = st.columns([1, 2])

    with col_kpi_main:
        st.markdown(f"""
        <div style="background-color: {status_cor}; padding: 25px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 6px 15px rgba(0,0,0,0.15);">
            <p style="margin:0; font-size: 1em; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">Status de Risco</p>
            <h2 style="margin:10px 0; font-size: 2.2em; color: white;">{status_icon} {status_txt}</h2>
            <div style="background: rgba(255,255,255,0.2); padding: 8px; border-radius: 8px; display: inline-block;">
                <p style="margin:0; font-weight:bold; font-size: 1.2em;">Índice P: {p_atual:.6f}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_kpi_desc:
        st.markdown(f"## Diagnóstico Ativo: {nome_ativo}")
        st.markdown(f"O modelo NERO avalia seu equipamento assumindo que a **inércia gera incerteza estocástica**. "
                    f"Neste instante, o coeficiente de estresse sistêmico ($\\alpha$) é de **{alpha_atual:.3f}**. "
                    f"Com um <i>uptime</i> diário de {uso_horas_in}h, a integridade operacional está classificada no status **{status_txt}**.")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Taxa de Falha Normalizada (λ)", f"{lambd_atual:.4f}")
        c2.metric("Estresse Sistêmico (α)", f"{alpha_atual:.3f}")
        c3.metric("Uso Diário (Minutos)", f"{uso_min_atual:.0f} min")

    st.markdown("---")

    # --- ABAS DE FERRAMENTAS ---
    tab_simulador, tab_grafico, tab_teoria = st.tabs([
        "🧪 Simulador de Cenários (What-If)", 
        "📈 Curva de Degradação (Gráfico Dinâmico)", 
        "📘 Entendendo a Fórmula NERO"
    ])

    # --- ABA 1: SIMULADOR ---
    with tab_simulador:
        st.markdown("### 🛠️ Estipulação de Nova Realidade Operacional")
        st.write("Teste se um novo regime de uso ou frequência de manutenção **aumenta ou diminui a confiabilidade** do sistema.")
        
        col_orig, col_arrow, col_sim = st.columns([4, 1, 4])
        
        with col_orig:
            st.info("🔒 **Cenário Atual (Baseline)**")
            st.text_input("Uso Diário Atual", f"{uso_horas_in} horas", disabled=True)
            st.text_input("Dias s/ Conserto Atual", f"{dias_in} dias", disabled=True)
            st.text_input("Falhas Anuais Atual", f"{falhas_in}", disabled=True)
            st.markdown(f"**Índice de Risco (P):** `{p_atual:.6f}`")

        with col_arrow:
            st.markdown("<div style='text-align: center; margin-top: 100px; font-size: 50px; color: #cbd5e1;'>➡️</div>", unsafe_allow_html=True)

        with col_sim:
            st.warning("✏️ **Novo Cenário (Alvo)**")
            novo_uso = st.number_input("Novo Uso Diário (Horas)", 0.5, 24.0, float(max(1.0, uso_horas_in - 5)), step=0.5)
            novos_dias = st.number_input("Novo Tempo s/ Conserto (Dias)", 0, 3650, int(max(0, dias_in - 10)))
            novas_falhas = st.number_input("Nova Taxa de Falhas (Ano)", 0, 1000, int(falhas_in))
            
            p_novo, lambd_novo, alpha_novo = calcular_nero(novas_falhas, novo_uso * 60, novos_dias * 1440)
            st.markdown(f"**Novo Índice (P):** `{p_novo:.6f}`")

        st.divider()

        if p_atual > 0:
            variacao_risco = ((p_novo - p_atual) / p_atual) * 100 
        else:
            variacao_risco = 0

        st.markdown("### 📊 Veredito NERO")
        
        if p_novo < p_atual:
            melhoria_seguranca = abs(variacao_risco)
            st.markdown(f"""
            <div class="success-box">
                <h3 style="margin-top:0;">📈 CONFIABILIDADE SUPERIOR</h3>
                <p>O novo cenário reduziu o Índice de Risco de <b>{p_atual:.6f}</b> para <b>{p_novo:.6f}</b>.</p>
                <p>O aparelho apresenta uma <b>melhoria de confiabilidade de aproximadamente {melhoria_seguranca:.1f}%</b>. O aumento do uso e/ou a redução do tempo ocioso permitem uma validação orgânica e mais firme da integridade do sistema.</p>
            </div>
            """, unsafe_allow_html=True)
        elif p_novo > p_atual:
            piora_seguranca = abs(variacao_risco)
            st.markdown(f"""
            <div class="warning-box">
                <h3 style="margin-top:0;">📉 CONFIABILIDADE INFERIOR</h3>
                <p>O novo cenário elevou o Índice de Risco de <b>{p_atual:.6f}</b> para <b>{p_novo:.6f}</b>.</p>
                <p>Cuidado: Este regime deixa o equipamento <b>{piora_seguranca:.1f}% mais perigoso</b>. A ociosidade alongada atua como um catalisador de falhas imprevistas.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("A alteração proposta mantém o equipamento no exato mesmo nível de risco estocástico.")

    # --- ABA 2: GRÁFICO (PLOTLY) ---
    with tab_grafico:
        st.markdown(f"### 📉 Evolução do Potencial de Risco (P)")
        st.write("Projeção de degradação: assume-se que as falhas e o uso diário se mantenham estáticos frente ao avanço dos dias sem conserto.")
        
        dias_projecao = max(dias_in + 60, 100)
        eixo_x = np.linspace(0, dias_projecao, 150)
        eixo_y_atual = []
        
        limite_visual = 0.02 
        
        for d in eixo_x:
            val, _, _ = calcular_nero(falhas_in, uso_min_atual, d * 1440)
            eixo_y_atual.append(min(val, limite_visual * 2))
            
        fig = go.Figure()

        # Zonas de Risco
        fig.add_hrect(y0=0, y1=0.005, fillcolor="#dcfce7", opacity=0.3, layer="below", line_width=0, annotation_text="Zona Operacional")
        fig.add_hrect(y0=0.005, y1=0.01, fillcolor="#fef08a", opacity=0.3, layer="below", line_width=0, annotation_text="Zona de Alerta")
        fig.add_hrect(y0=0.01, y1=limite_visual*2, fillcolor="#fee2e2", opacity=0.3, layer="below", line_width=0, annotation_text="Zona Crítica")

        # Curva
        fig.add_trace(go.Scatter(
            x=eixo_x, y=eixo_y_atual,
            mode='lines',
            name='Degradação Estocástica',
            line=dict(color='#1e293b', width=4),
            hovertemplate='Dias sem Conserto: %{x:.0f}<br>Índice NERO: %{y:.6f}<extra></extra>'
        ))

        # Ponto Atual
        fig.add_trace(go.Scatter(
            x=[dias_in], y=[p_atual],
            mode='markers+text',
            name='Situação Atual',
            marker=dict(color=status_cor, size=18, line=dict(color='white', width=3)),
            text=['VOCÊ ESTÁ AQUI'],
            textposition='top left',
            textfont=dict(size=14, color=status_cor, family="Arial Black")
        ))

        fig.update_layout(
            title=f"Risco vs. Dias de Ociosidade (Uso Fixo: {uso_horas_in}h/dia)",
            xaxis_title="Tempo desde a última manutenção (Dias)",
            yaxis_title="Índice de Risco NERO (P)",
            hovermode="x unified",
            height=500,
            margin=dict(l=20, r=20, t=50, b=20),
            plot_bgcolor="white"
        )
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)', range=[0, min(max(eixo_y_atual)*1.1, limite_visual)])

        st.plotly_chart(fig, use_container_width=True)

    # --- ABA 3: TEORIA DO MODELO NERO (CORRIGIDA) ---
    with tab_teoria:
        col_t1, col_t2 = st.columns([1.5, 1])
        
        with col_t1:
            st.markdown("### A Matemática da Dissipação por Uso")
            st.write("A gênese do modelo NERO inspira-se nos padrões naturais da constante de Euler e na lei de resfriamento de Newton, estabelecendo a premissa de que o risco de pane é um estado que se autoalimenta durante o repouso do maquinário.")
            
            st.markdown("#### Equação Fundamental:")
            # Renderização nativa do Streamlit para LaTeX (Display Mode)
            st.latex(r"P = \frac{e^{(\lambda \cdot \alpha)}}{U}")
            
            st.markdown("""
            **Composição Variável:**
            * **$P$**: Potencial de Risco Sistêmico (Quanto mais perto de zero, maior a segurança).
            * **$\lambda$** (Lambda): Taxa de falhas anuais normalizada ($\sum \text{Falhas} / 365$).
            * **$\alpha$** (Alpha): Coeficiente de Estresse Sistêmico. Definido ordinariamente por $\\frac{|T-U|}{T+1}$.
              * **⚠️ Regra de Suavização Logarítmica:** No limite em que $T$ tende a 0, $\\alpha$ tenderia irrestritamente ao módulo de $U$. Para evitar explosões numéricas (assíntotas) e aproveitar a capacidade matemática do logaritmo de estabilizar funções agressivas, **o algoritmo calcula $\\alpha = \ln(|U|)$ se, e somente se, $T \\to 0$.**
              * Além disso, caso haja simetria total ($T = U$), a base temporal é reajustada para $T+1$.
            * **$U$**: Tempo contínuo de uso diário em minutos (A variável que "conquista" a confiabilidade).
            * **$T$**: Tempo desde o último conserto em minutos (A variável que "catalisa" a incerteza).
            """)

        with col_t2:
            st.info("""
            💡 **O Trunfo do Modelo NERO**
            
            Um sistema eletromecânico, mesmo em repouso, avança rumo à entropia. A genialidade da fórmula está em mostrar que **um conserto recente não é sinônimo imutável de segurança**. 
            
            A máquina precisa "provar" sua higidez mecânica através da atividade (denominador $U$). Um equipamento que apresentou mais falhas históricas, porém opera 12 horas diárias sob intensa validação contínua, muitas vezes demonstra maior estabilidade do que aquele que girou os motores por meros minutos após sair da oficina na mesma semana.
            """)


