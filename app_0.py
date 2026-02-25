import streamlit as st
import math
import plotly.graph_objects as go
import numpy as np

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="NERO Pro: Risk Observer V6",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILIZAÇÃO CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background: linear-gradient(135deg, #FF3D00 0%, #FF9100 50%, #FFC400 100%) !important; }
    [data-testid="stSidebar"] * { color: #ffffff !important; text-shadow: 0px 1px 2px rgba(0,0,0,0.2); }
    .gradient-text { background: linear-gradient(90deg, #00C853 0%, #00B0FF 33%, #9C27B0 66%, #FF3D00 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; }
    .modern-card { background: linear-gradient(145deg, #ffffff, #f8fafc); padding: 24px; border-radius: 16px; border: 1px solid #e2e8f0; box-shadow: 0 10px 20px rgba(0,0,0,0.08); transition: all 0.3s ease; height: 100%; }
    .modern-card:hover { transform: translateY(-8px); box-shadow: 0 15px 30px rgba(0,0,0,0.12); border-color: #00B0FF; }
    .status-badge { display: inline-block; padding: 8px 16px; border-radius: 9999px; font-weight: 800; font-size: 0.9rem; letter-spacing: 0.08em; text-transform: uppercase; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. MOTOR MATEMÁTICO NERO V6 ---
def calcular_nero(falhas_ano: int, uso_diario_min: float, t_conserto_min: float):
    # Proteção do uso diário para evitar divisão por 0 e log de <=0
    u = max(uso_diario_min, 0.1) 
    tc = t_conserto_min 

    # 1. Lambda
    lambd = falhas_ano / 365.0

    # 2. Alpha com ponderações exatas
    if tc == u:
        num_alpha = tc + 1.0
    elif tc == 0:
        num_alpha = math.log(u)
    else:
        num_alpha = abs(tc - u)
        
    alpha = num_alpha / (tc + 1.0)

    # 3. Equação Principal
    try:
        # Fator (1 + 1/tc)^tc. Trata o limite notável se tc == 0
        if tc == 0:
            termo_1 = 1.0 
        else:
            termo_1 = (1.0 + 1.0 / tc) ** tc
            
        termo_2 = math.exp(alpha * lambd)
        termo_3 = math.gamma(alpha + 1.0)
        
        numerador = termo_1 * termo_2 * termo_3
        p_score = numerador / u
        
    except Exception:
        p_score = float('inf')

    return p_score, lambd, alpha, u

# --- NOVOS PARÂMETROS DE RISCO (Desescalados de volta para notação pequena) ---
def get_status_visual(p_score):
    if p_score < 0.010:
        return "EXCELENTE", "#00c853", "🟢"
    elif p_score < 0.025:
        return "OPERACIONAL", "#00b0ff", "🔵"
    elif p_score < 0.050:
        return "ALERTA", "#ffc400", "🟠"
    elif p_score < 0.100:
        return "RISCO CRÍTICO", "#ff3d00", "🔴"
    else:
        return "COLAPSO IMINENTE", "#d50000", "⛔"

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 3em;'>🛡️</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; margin-bottom: 0;'>NERO Pro V6</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1em; font-weight: bold;'>Risk Observer Protocol</p>", unsafe_allow_html=True)
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
            dias_in = st.number_input("Dias s/ Conserto", min_value=0, value=2)
        uso_horas_in = st.slider("Uso Diário Médio (h)", 0.5, 24.0, 8.0, 0.5)

# --- 5. ROTEAMENTO DE PÁGINAS ---
if pagina == "🏠 Visão Geral":
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px;">
        <h1 class="gradient-text" style="font-size: 4em; margin-bottom: 10px;">O Protocolo Euler-Gama</h1>
        <h3 style="color: #475569; font-weight: 400; font-size: 1.5em; max-width: 800px; margin: 0 auto;">
            O NERO V6 retorna à precisão absoluta da engenharia: <b>Quanto MENOR o valor, mais blindado e seguro</b> está o seu sistema contra falhas estocásticas.
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col_img, col_txt = st.columns([1, 1.2], gap="large")
    with col_img:
        st.markdown("""
        <div class="modern-card" style="background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); border-top: 6px solid #00B0FF; color: white;">
            <h2 style="color: #00B0FF; margin-top: 0;">Fadiga por Juros Compostos</h2>
            <p style="font-size: 1.1em; color: #e2e8f0; line-height: 1.6;">
                O abandono não soma defeitos, ele os multiplica. O NERO V6 introduz o limite matemático do Número de Euler integrado à Função Gama criando um gatilho para ativos não mantidos.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_txt:
        st.markdown("### A Equação Definitiva de Degradação")
        
        st.latex(r"\lambda = \frac{\text{Falhas no Ano}}{365}")
        st.latex(r"\alpha = \frac{|t_c - u|}{t_c + 1}")
        st.latex(r"Index = \frac{\left(1 + \frac{1}{t_c}\right)^{t_c} \cdot e^{\alpha \cdot \lambda} \cdot \Gamma(\alpha + 1)}{u}")
        
        st.markdown("""
        * **$Index$:** O Placar de Ameaça padronizado (Baixos = Seguro).
        * **$\left(1 + \frac{1}{t_c}\right)^{t_c}$:** Fator de Euler para desgaste base.
        * **$e^{\alpha \cdot \lambda}$:** Fator estocástico de incidência.
        * **$\Gamma(\alpha + 1)$:** O Abismo Fatorial cruzando o limite do estresse.
        * **$u$:** Amortecedor de Uso Operacional Diário.
        """)

elif pagina == "🚀 Sistemas Complexos (Aeronaves/Veículos)":
    st.markdown("<h2 class='gradient-text'>Risco Global de Sistemas Eletromecânicos</h2>", unsafe_allow_html=True)
    st.write("Avalie o risco de ruptura global ponderando o risco de cada subsistema.")
    
    sistemas = ["Motor Principal", "Sistema Hidráulico", "Aviônicos / Sensores"]
    resultados = []
    
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    
    for i, sys_name in enumerate(sistemas):
        with cols[i]:
            cores_topo = ["#00B0FF", "#FF3D00", "#9C27B0"]
            st.markdown(f"<div class='modern-card' style='border-top: 6px solid {cores_topo[i]};'>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='color:{cores_topo[i]};'>{sys_name}</h4>", unsafe_allow_html=True)
            f_ano = st.number_input(f"Falhas/Ano", 0, 50, 1 + i, key=f"f_{i}")
            d_conserto = st.number_input(f"Dias s/ Manut.", 0, 7000, 2 + i*5, key=f"d_{i}")
            u_diario_h = st.slider(f"Uso/Dia (h)", 0.5, 24.0, 6.0, key=f"u_{i}")
            
            p, l, a, u_efetivo = calcular_nero(f_ano, u_diario_h * 60, d_conserto * 1440)
            resultados.append({'p': p, 'alpha': a})
            
            status, cor, icon = get_status_visual(p)
            st.markdown(f"<p style='color:{cor}; font-weight:800; font-size: 1.2em;'>Risco: {p:.2e}</p>", unsafe_allow_html=True)
            st.markdown(f"<span class='status-badge' style='background:{cor}; color:white; font-size: 0.7rem;'>{icon} {status}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
    soma_p_alpha = sum(r['p'] * r['alpha'] for r in resultados)
    soma_alpha = sum(r['alpha'] for r in resultados)
    p_global = soma_p_alpha / soma_alpha if soma_alpha > 0 else float('inf')
    
    st.divider()
    stat_g, cor_g, icon_g = get_status_visual(p_global)
    st.markdown(f"""
    <div style="text-align: center; padding: 40px; background: linear-gradient(145deg, #ffffff, {cor_g}15); border-radius: 20px; border: 3px solid {cor_g}; box-shadow: 0 10px 30px {cor_g}30;">
        <h3 style="margin:0; color: #1e293b; font-weight: 800;">RISCO ESTRUTURAL DA AERONAVE</h3>
        <h1 style="font-size: 5em; color: {cor_g}; margin: 10px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">{p_global:.2e}</h1>
        <span class="status-badge" style="background: {cor_g}; color: white; font-size: 1.2em;">{icon_g} STATUS: {stat_g}</span>
    </div>
    """, unsafe_allow_html=True)

elif pagina == "⚙️ Dashboard de Ativos":
    uso_diario_min_atual = uso_horas_in * 60
    t_conserto_min_atual = dias_in * 1440
    p_atual, lambd_atual, alpha_atual, uso_efetivo_atual = calcular_nero(falhas_in, uso_diario_min_atual, t_conserto_min_atual)
    status_txt, status_cor, status_icon = get_status_visual(p_atual)

    st.markdown(f"<h2 style='color: #1e293b;'>Monitoramento de Risco: <span style='color: #00B0FF;'>{nome_ativo}</span></h2>", unsafe_allow_html=True)
    col_kpi, col_info = st.columns([1, 2.5])
    
    with col_kpi:
        st.markdown(f"""
        <div class="modern-card" style="background: {status_cor}; text-align: center; color: white;">
            <p style="color: rgba(255,255,255,0.8); font-size: 1em; font-weight: 800; text-transform: uppercase; margin: 0;">Índice NERO V6</p>
            <h2 style="font-size: 3em; color: white; margin: 10px 0; text-shadow: 0px 4px 10px rgba(0,0,0,0.3);">{p_atual:.2e}</h2>
            <div style="background: rgba(255,255,255,0.2); color: white; border: 1px solid white;" class="status-badge">
                {status_icon} {status_txt}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_info:
        st.markdown("<div class='modern-card'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Taxa Normalizada (λ)", f"{lambd_atual:.4f}")
        c2.metric("Coeficiente de Estresse (α)", f"{alpha_atual:.3f}")
        c3.metric("Uso Diário Real", f"{uso_diario_min_atual:.0f} m/dia")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab_grafico, tab_simulador = st.tabs(["📈 Curva de Fadiga Euler-Gama", "🧪 Simulador de Regime Operacional"])

    with tab_grafico:
        st.write("A linha abaixo mostra como o risco avança conforme os dias sem manutenção acumulam.")
        dias_projecao = max(dias_in + 150, 200)
        eixo_x = np.linspace(1, dias_projecao, 200)
        eixo_y = [calcular_nero(falhas_in, uso_diario_min_atual, d * 1440)[0] for d in eixo_x]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=eixo_x, y=eixo_y, mode='lines', name='Risco NERO',
            line=dict(color='#ff3d00', width=5, shape='spline'),
            fill='tozeroy', fillcolor='rgba(255, 61, 0, 0.15)',
            hovertemplate='Dias s/ Manutenção: %{x:.0f}<br>Risco: %{y:.2e}<extra></extra>'
        ))
        fig.add_trace(go.Scatter(
            x=[max(dias_in, 1)], y=[p_atual], mode='markers+text', name='Estado Atual',
            marker=dict(color=status_cor, size=18, line=dict(color='white', width=4)),
            text=['📍 MARCA ATUAL'], textposition='top left', textfont=dict(color=status_cor, size=14, weight='bold')
        ))
        fig.update_layout(
            hovermode="x unified", height=500, margin=dict(l=0, r=0, t=30, b=0),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="Dias Acumulados sem Manutenção", showgrid=True, gridcolor='#e2e8f0'),
            yaxis=dict(title="Índice de Risco", tickformat=".1e", showgrid=True, gridcolor='#e2e8f0')
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab_simulador:
        st.markdown("### Teste de Impacto: Mudança de Comportamento")
        col_s1, col_s2, col_s3 = st.columns([1, 0.2, 1])
        with col_s1:
            st.info(f"**Cenário Atual:**\n\nUso: {uso_horas_in}h/dia | Manut.: {dias_in} dias atrás\nRisco Base: **{p_atual:.2e}**")
        with col_s2:
            st.markdown("<h1 style='text-align: center; color: #ff3d00; margin-top: 10px;'>⚡</h1>", unsafe_allow_html=True)
        with col_s3:
            default_uso = round(max(1.0, uso_horas_in - 2.0) * 2) / 2
            novo_uso_h = st.slider("Testar Novo Uso (h/dia)", 0.5, 24.0, default_uso, 0.5, key="sim_uso")
            novos_dias = st.number_input("Testar Dias sem Manutenção", 0, 7000, int(max(1, dias_in - 1)), key="sim_dias")
            
        p_novo, _, _, _ = calcular_nero(falhas_in, novo_uso_h * 60, novos_dias * 1440)
        st.divider()
        if p_novo < p_atual:
            melhoria = (p_atual / p_novo) if p_novo > 0 else float('inf')
            st.markdown(f"""<div class="modern-card" style="border-left: 8px solid #00C853;">
                <h3 style="color:#00C853; margin:0;">📉 MELHORIA DE SEGURANÇA</h3>
                <p>O Risco caiu para <b>{p_novo:.2e}</b> (Ficou {melhoria:.1f}x mais SEGURO).</p>
            </div>""", unsafe_allow_html=True)
        elif p_novo > p_atual:
            piora = (p_novo / p_atual) if p_atual > 0 else float('inf')
            st.markdown(f"""<div class="modern-card" style="border-left: 8px solid #FF3D00;">
                <h3 style="color:#FF3D00; margin:0;">📈 ALARME DE PERIGO</h3>
                <p>O Risco subiu para <b>{p_novo:.2e}</b> (Ficou {piora:.1f}x mais PERIGOSO).</p>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="modern-card" style="border-left: 8px solid #00b0ff;">
                <h3 style="color:#00b0ff; margin:0;">⚖️ RISCO ESTÁVEL</h3>
                <p>O nível de risco se manteve inalterado com esses parâmetros.</p>
            </div>""", unsafe_allow_html=True)

elif pagina == "⚖️ Comparador de Marcas":
    st.markdown("## ⚖️ Duelo de Tolerância à Negligência")
    st.write("O **menor Índice de Risco** ganha.")
    
    col_marca_a, col_vs, col_marca_b = st.columns([1, 0.2, 1])
    
    with col_marca_a:
        st.markdown("<div class='modern-card' style='border-top: 8px solid #00B0FF;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #00B0FF;'>Máquina A</h3>", unsafe_allow_html=True)
        nome_a = st.text_input("Nome", "TechCorp", key="nome_a")
        falhas_a = st.number_input("Falhas/Ano", 0, 100, 2, key="falhas_a")
        dias_a = st.number_input("Dias s/ Conserto", 0, 7000, 30, key="dias_a")
        uso_a_h = st.number_input("Horas Uso/Dia", 1.0, 24.0, 12.0, key="uso_a")
        p_a, _, _, _ = calcular_nero(falhas_a, uso_a_h * 60, dias_a * 1440)
        status_txt_a, color_a, icon_a = get_status_visual(p_a)
        st.markdown(f"<br><h5 style='color: #64748b; margin:0;'>Risco Ponderado</h5><h1 style='color: {color_a}; margin:0;'>{p_a:.2e}</h1>", unsafe_allow_html=True)
        st.markdown(f"<span class='status-badge' style='background:{color_a}; color:white; margin-top:10px;'>{icon_a} {status_txt_a}</span></div>", unsafe_allow_html=True)

    with col_vs:
        st.markdown("<h1 style='text-align: center; font-size: 4em; color: #cbd5e1; margin-top: 100px;'>⚔️</h1>", unsafe_allow_html=True)

    with col_marca_b:
        st.markdown("<div class='modern-card' style='border-top: 8px solid #9C27B0;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #9C27B0;'>Máquina B</h3>", unsafe_allow_html=True)
        nome_b = st.text_input("Nome", "ElectroMax", key="nome_b")
        falhas_b = st.number_input("Falhas/Ano", 0, 100, 8, key="falhas_b")
        dias_b = st.number_input("Dias s/ Conserto", 0, 7000, 15, key="dias_b")
        uso_b_h = st.number_input("Horas Uso/Dia", 1.0, 24.0, 12.0, key="uso_b")
        p_b, _, _, _ = calcular_nero(falhas_b, uso_b_h * 60, dias_b * 1440)
        status_txt_b, color_b, icon_b = get_status_visual(p_b)
        st.markdown(f"<br><h5 style='color: #64748b; margin:0;'>Risco Ponderado</h5><h1 style='color: {color_b}; margin:0;'>{p_b:.2e}</h1>", unsafe_allow_html=True)
        st.markdown(f"<span class='status-badge' style='background:{color_b}; color:white; margin-top:10px;'>{icon_b} {status_txt_b}</span></div>", unsafe_allow_html=True)

    st.divider()
    if p_a < p_b:
        st.success(f"🏆 A máquina **{nome_a}** provou ser estruturalmente mais segura e resistente.")
    elif p_b < p_a:
        st.success(f"🏆 A máquina **{nome_b}** provou ser estruturalmente mais segura e resistente.")
    else:
        st.info("⚖️ Empate técnico.")


