import streamlit as st
import math
import plotly.graph_objects as go
import numpy as np
import pandas as pd

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
</style>
""", unsafe_allow_html=True)

# --- 3. CORE: MOTOR MATEMÁTICO NERO ---

def calcular_nero(falhas_ano: int, uso_min: float, t_conserto_min: float):
    """
    Calcula o score NERO (Nikollas-Euler Risk Observer).
    Fórmula: P = (e^(lambda * alpha)) / U
    """
    # Proteção: Uso não pode ser zero absoluto para evitar divisão por zero
    if uso_min <= 0.1: 
        uso_min = 0.1 
    
    # 1. Lambda (Taxa de Falhas Anual Normalizada)
    lambd = falhas_ano / 365.0
    
    # 2. Alpha (Coeficiente de Estresse Sistêmico)
    # Regra baseada no artigo: se T = U, aplica-se uma fórmula alternativa
    if t_conserto_min == uso_min:
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
        return "CRÍTICO EXTREMO", "#991b1b", "⛔ Falha Iminente"
    elif p_score > 0.01:
        return "CRÍTICO", "#dc2626", "🔴 Risco Alto"
    elif p_score > 0.005:
        return "ALERTA", "#f59e0b", "🟠 Atenção Necessária"
    elif p_score > 0.001:
        return "OPERACIONAL", "#3b82f6", "🔵 Operação Padrão"
    else:
        return "EXCELENTE", "#10b981", "🟢 Alta Confiabilidade"

# --- 4. SIDEBAR: DADOS DO ATIVO ---

with st.sidebar:
    st.title("🛡️ NERO Pro")
    st.caption("Fórmula de NERO: Medição Exponencial-Dinâmica")
    st.divider()

    st.subheader("⚙️ Dados do Equipamento")
    nome_ativo = st.text_input("Identificação", "Elevador de Alto Tráfego")
    
    col1, col2 = st.columns(2)
    with col1:
        falhas_in = st.number_input("Falhas (Últ. Ano)", min_value=0, value=15, help="Soma total de panes no período de 365 dias.")
    with col2:
        dias_in = st.number_input("Dias s/ Conserto", min_value=0, value=20, help="Tempo decorrido desde a última manutenção corretiva.")
    
    uso_horas_in = st.slider("Uso Diário Médio (Horas)", 0.5, 24.0, 12.0, 0.5)
    
    st.markdown("---")
    st.info("💡 **Dica:** O modelo NERO penaliza equipamentos inativos e recompensa o uso contínuo (validação operacional).")

# --- 5. LÓGICA DE APRESENTAÇÃO ---

# --- CÁLCULO DO ESTADO ATUAL ---
# Conversão imperativa para minutos (base da fórmula NERO)
uso_min_atual = uso_horas_in * 60
t_conserto_min_atual = dias_in * 1440

p_atual, lambd_atual, alpha_atual = calcular_nero(falhas_in, uso_min_atual, t_conserto_min_atual)
status_txt, status_cor, status_icon = get_status_visual(p_atual)

# --- DASHBOARD PRINCIPAL ---

# Header com Status Grande
col_kpi_main, col_kpi_desc = st.columns([1, 2])

with col_kpi_main:
    st.markdown(f"""
    <div style="background-color: {status_cor}; padding: 25px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 6px 15px rgba(0,0,0,0.15);">
        <p style="margin:0; font-size: 1em; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">Status de Risco</p>
        <h2 style="margin:10px 0; font-size: 2.2em; color: white;">{status_txt}</h2>
        <div style="background: rgba(255,255,255,0.2); padding: 8px; border-radius: 8px; display: inline-block;">
            <p style="margin:0; font-weight:bold; font-size: 1.2em;">Índice P: {p_atual:.6f}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
with col_kpi_desc:
    st.markdown(f"## Análise Diagnóstica: {nome_ativo}")
    st.markdown(f"O modelo NERO avalia o equipamento sob o paradigma de que **a inércia gera estresse sistêmico**. "
                f"Atualmente, seu equipamento possui um coeficiente de estresse ($\\alpha$) de **{alpha_atual:.3f}**. "
                f"Com um tempo de funcionamento diário de {uso_horas_in}h, sua capacidade de autocertificação operacional o enquadra no status **{status_txt}**.")
    
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

# --- ABA 1: SIMULADOR COMPARATIVO ---
with tab_simulador:
    st.markdown("### 🛠️ Estipulação de Nova Realidade Operacional")
    st.write("Insira parâmetros imaginários de um novo cenário para avaliar se a mudança **aumenta ou diminui a confiabilidade** do sistema, provando que mais tempo de funcionamento pode gerar maior segurança.")
    
    col_orig, col_arrow, col_sim = st.columns([4, 1, 4])
    
    # LADO ESQUERDO: ORIGINAL
    with col_orig:
        st.info("🔒 **Cenário Atual (Baseline)**")
        st.text_input("Uso Diário", f"{uso_horas_in} horas", disabled=True, key="orig_uso")
        st.text_input("Dias s/ Conserto", f"{dias_in} dias", disabled=True, key="orig_dias")
        st.text_input("Falhas Anuais", f"{falhas_in}", disabled=True, key="orig_falhas")
        st.markdown(f"**Índice de Risco (P):** `{p_atual:.6f}`")

    # CENTRO: SETA
    with col_arrow:
        st.markdown("<div style='text-align: center; margin-top: 100px; font-size: 50px; color: #cbd5e1;'>➡️</div>", unsafe_allow_html=True)

    # LADO DIREITO: SIMULAÇÃO
    with col_sim:
        st.warning("✏️ **Novo Cenário (Alvo)**")
        novo_uso = st.number_input("Novo Uso Diário (Horas)", 0.5, 24.0, float(max(1.0, uso_horas_in - 5)), step=0.5)
        novos_dias = st.number_input("Novo Tempo s/ Conserto (Dias)", 0, 3650, int(max(0, dias_in - 10)))
        novas_falhas = st.number_input("Nova Taxa de Falhas (Ano)", 0, 1000, int(falhas_in))
        
        # CÁLCULO DA SIMULAÇÃO
        p_novo, lambd_novo, alpha_novo = calcular_nero(novas_falhas, novo_uso * 60, novos_dias * 1440)
        st.markdown(f"**Novo Índice (P):** `{p_novo:.6f}`")

    st.divider()

    # RESULTADO COMPARATIVO E CONCLUSÃO
    if p_atual > 0:
        # A conta do delta: Se o risco NOVO for MENOR, a segurança é MAIOR.
        # Risco caiu em X% = Segurança subiu em X%
        variacao_risco = ((p_novo - p_atual) / p_atual) * 100 
    else:
        variacao_risco = 0

    st.markdown("### 📊 Veredito NERO")
    
    if p_novo < p_atual:
        melhoria_seguranca = abs(variacao_risco)
        st.markdown(f"""
        <div class="success-box">
            <h3>📈 CONFIABILIDADE SUPERIOR</h3>
            <p style="font-size: 16px;">O novo cenário reduziu o Índice de Risco de <b>{p_atual:.6f}</b> para <b>{p_novo:.6f}</b>.</p>
            <p style="font-size: 16px;">Ao adotar este novo regime operacional, o aparelho apresenta uma <b>melhoria de confiabilidade de aproximadamente {melhoria_seguranca:.1f}%</b>. 
            O aumento do uso e/ou a redução do tempo de ociosidade permitiram uma maior validação da integridade mecânica do sistema.</p>
        </div>
        """, unsafe_allow_html=True)
    elif p_novo > p_atual:
        piora_seguranca = abs(variacao_risco)
        st.markdown(f"""
        <div class="warning-box">
            <h3>📉 CONFIABILIDADE INFERIOR</h3>
            <p style="font-size: 16px;">O novo cenário elevou o Índice de Risco de <b>{p_atual:.6f}</b> para <b>{p_novo:.6f}</b>.</p>
            <p style="font-size: 16px;">Cuidado: Este cenário deixa o equipamento <b>{piora_seguranca:.1f}% mais perigoso</b>. 
            Isso ocorre porque a ociosidade atua como catalisador de incerteza, ou o tempo de uso diário não é suficiente para certificar a eficiência operacional frente ao tempo decorrido do último conserto.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("A alteração proposta mantém o equipamento no mesmo nível exato de risco estocástico.")

# --- ABA 2: GRÁFICO DINÂMICO (PLOTLY) ---
with tab_grafico:
    st.markdown(f"### 📉 Evolução do Potencial de Risco (P)")
    st.write("Acompanhe como a ausência prolongada de manutenção acelera a degradação e expõe o sistema a panes, assumindo que a taxa de falhas e o uso diário se mantenham estáticos.")
    
    # Preparação dos dados para o gráfico
    dias_projecao = max(dias_in + 60, 100) # Projeta 60 dias além do atual
    eixo_x = np.linspace(0, dias_projecao, 150)
    eixo_y_atual = []
    
    limite_visual = 0.02 # Limite Y para o gráfico não quebrar com exponenciais gigantes
    
    for d in eixo_x:
        val, _, _ = calcular_nero(falhas_in, uso_min_atual, d * 1440)
        eixo_y_atual.append(min(val, limite_visual * 2)) # Clip para manter visibilidade
        
    # Construção do Gráfico Interativo com Plotly
    fig = go.Figure()

    # Zonas de Risco (Background)
    fig.add_hrect(y0=0, y1=0.005, fillcolor="#dcfce7", opacity=0.3, layer="below", line_width=0, annotation_text="Zona de Confiabilidade")
    fig.add_hrect(y0=0.005, y1=0.01, fillcolor="#fef08a", opacity=0.3, layer="below", line_width=0, annotation_text="Zona de Alerta")
    fig.add_hrect(y0=0.01, y1=limite_visual*2, fillcolor="#fee2e2", opacity=0.3, layer="below", line_width=0, annotation_text="Zona Crítica")

    # Linha de Projeção
    fig.add_trace(go.Scatter(
        x=eixo_x, y=eixo_y_atual,
        mode='lines',
        name='Curva de Risco',
        line=dict(color='#1e293b', width=4),
        hovertemplate='Dias sem Conserto: %{x:.0f}<br>Índice NERO: %{y:.6f}<extra></extra>'
    ))

    # Ponto do Estado Atual
    fig.add_trace(go.Scatter(
        x=[dias_in], y=[p_atual],
        mode='markers+text',
        name='Situação Atual',
        marker=dict(color=status_cor, size=18, line=dict(color='white', width=3)),
        text=['VOCÊ ESTÁ AQUI'],
        textposition='top left',
        textfont=dict(size=14, color=status_cor, family="Arial Black")
    ))

    # Configuração de Layout
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

# --- ABA 3: TEORIA DO MODELO NERO ---
with tab_teoria:
    col_t1, col_t2 = st.columns([1.5, 1])
    
    with col_t1:
        st.markdown("### Fundamentação Teórica")
        st.write("""
        Diferente de modelos estáticos convencionais como o MTBF (Mean Time Between Failures), a Fórmula de NERO introduz o dinamismo na mensuração de falhas através do conceito de **dissipação por uso**.
        """)
        
        st.markdown("A gênese do modelo inspira-se nos padrões naturais da constante de Euler e na lei de resfriamento de Newton, estabelecendo uma premissa ousada: **O risco de pane não é linear, e sim um estado que se autoalimenta durante o repouso.**")
        
        st.markdown("""
        #### A Equação Fundamental:
        """)
        st.latex(r"P = \frac{e^{(\lambda \cdot \alpha)}}{U}")
        
        st.markdown("""
        **Composição:**
        * $P$: Potencial de Risco Sistêmico (Quanto mais perto de zero, mais seguro).
        * $\lambda$ (Lambda): Taxa de falhas diárias ($\sum \text{Falhas} / 365$).
        * $ (Alpha): Coeficiente de Estresse Sistêmico, definido por {|T-U|}{T+1} Para T igual a U, T se torna T+1$.
        * $U$: Tempo contínuo de uso diário em minutos (A exposição monitorada que conquista a confiabilidade).
        * $T$: Tempo desde o último conserto em minutos (A ociosidade que catalisa a incerteza).
        """)

    with col_t2:
        st.info("""
        💡 **O Trunfo do Modelo NERO**
        
        Um sistema eletromecânico, mesmo em repouso, tende ao acúmulo de energia e falha. A genialidade da fórmula está em mostrar que **um conserto recente não é sinônimo absoluto de segurança**. 
        
        O aparelho precisa "provar" sua segurança através da atividade (denominador $U$). Um equipamento como um elevador que estraga mais vezes, mas trabalha 12 horas por dia de forma consistente, estatisticamente demonstra muito mais estabilidade operacional através da sua "sobrevivência" diária do que um elevador que rodou apenas 1 hora após um conserto recente.
        """)
         