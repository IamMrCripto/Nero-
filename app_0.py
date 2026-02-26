import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# CONFIGURAÇÃO DO STREAMLIT
# ==========================================
st.set_page_config(
    page_title="EngineRel | Reliability Analytics",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ocultar os menus padrões do Streamlit para dar aspecto de site real
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# ==========================================
# CÓDIGO FONTE DO SISTEMA (HTML + CSS + JS)
# (Usando 'r' antes da string para evitar que o Python quebre as barras do LaTeX)
# ==========================================
html_code = r"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EngineRel - Monitoramento Dinâmico</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800;900&family=JetBrains+Mono:wght@400;700;800&display=swap" rel="stylesheet">
    
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    
    <style>
        /* =========================================
           SISTEMA DE CORES E VARIÁVEIS (DARK THEME)
           ========================================= */
        :root {
            --bg-base: #0d1117;         /* Fundo estilo GitHub Dark / AWS */
            --bg-panel: #161b22;        /* Fundo dos cartões */
            --bg-input: #010409;        /* Fundo das caixas de texto */
            --blue-primary: #00b4d8;    /* Azul Claro Vivo */
            --blue-glow: rgba(0, 180, 216, 0.2);
            --green-primary: #00ff87;   /* Verde Fluorescente */
            --green-glow: rgba(0, 255, 135, 0.2);
            --text-main: #c9d1d9;
            --text-muted: #8b949e;
            --border-color: #30363d;
            --font-ui: 'Inter', sans-serif;
            --font-code: 'JetBrains Mono', monospace;
        }

        /* RESET BÁSICO */
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            background-color: var(--bg-base);
            color: var(--text-main);
            font-family: var(--font-ui);
            line-height: 1.6;
            padding: 20px;
            overflow-x: hidden;
        }

        /* SCROLLBAR CUSTOMIZADA */
        ::-webkit-scrollbar { width: 10px; }
        ::-webkit-scrollbar-track { background: var(--bg-base); }
        ::-webkit-scrollbar-thumb { background: var(--border-color); border-radius: 5px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--blue-primary); }

        /* =========================================
           CABEÇALHO (HERO SECTION)
           ========================================= */
        .hero {
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(180deg, rgba(0, 180, 216, 0.05) 0%, var(--bg-base) 100%);
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 40px;
            border-radius: 16px;
        }

        .hero h1 {
            font-size: 4rem;
            font-weight: 900;
            letter-spacing: -2px;
            margin-bottom: 10px;
            color: #ffffff;
        }

        .hero h1 span.blue { color: var(--blue-primary); text-shadow: 0 0 20px var(--blue-glow); }
        .hero h1 span.green { color: var(--green-primary); text-shadow: 0 0 20px var(--green-glow); }

        .hero p {
            font-size: 1.2rem;
            color: var(--text-muted);
            max-width: 600px;
            margin: 0 auto;
        }

        /* =========================================
           GRID PRINCIPAL
           ========================================= */
        .dashboard-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            max-width: 1400px;
            margin: 0 auto;
        }

        .panel {
            background-color: var(--bg-panel);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.6);
            transition: transform 0.3s ease;
        }

        .panel:hover {
            border-color: #4b5563;
        }

        /* =========================================
           IMAGENS E FÓRMULA (LADO ESQUERDO)
           ========================================= */
        .image-gallery {
            display: grid;
            grid-template-columns: repeat(2, 1fr); /* Ajustado para as 2 imagens em anexo */
            gap: 15px;
            margin-bottom: 25px;
        }

        .image-gallery img {
            width: 100%;
            height: 250px; /* Ajuste de altura para melhor visualização das imagens verticais */
            object-fit: cover;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            filter: grayscale(40%);
            transition: filter 0.3s ease;
        }

        .image-gallery img:hover {
            filter: grayscale(0%);
            border-color: var(--blue-primary);
        }

        .math-container {
            background-color: var(--bg-input);
            padding: 25px;
            border-radius: 12px;
            border: 1px solid var(--blue-primary);
            box-shadow: inset 0 0 20px var(--blue-glow);
            margin: 20px 0;
            overflow-x: auto;
            text-align: center;
            font-size: 1.3rem;
        }

        .theory-list {
            list-style: none;
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-top: 20px;
        }

        .theory-list li {
            margin-bottom: 10px;
            padding-left: 20px;
            position: relative;
        }

        .theory-list li::before {
            content: '>';
            position: absolute;
            left: 0;
            color: var(--blue-primary);
            font-weight: 900;
        }

        /* =========================================
           FORMULÁRIO E INPUTS (LADO DIREITO)
           ========================================= */
        .form-title {
            color: #fff;
            font-size: 1.5rem;
            font-weight: 800;
            margin-bottom: 25px;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 10px;
        }

        .input-group {
            margin-bottom: 25px;
        }

        .input-group label {
            display: block;
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--blue-primary);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }

        .input-group input, .input-group select {
            width: 100%;
            background-color: var(--bg-input);
            border: 1px solid var(--border-color);
            color: #ffffff;
            padding: 16px;
            border-radius: 8px;
            font-family: var(--font-code);
            font-size: 1.1rem;
            transition: all 0.3s ease;
        }

        .input-group input:focus, .input-group select:focus {
            outline: none;
            border-color: var(--green-primary);
            box-shadow: 0 0 15px var(--green-glow);
        }

        .btn-process {
            width: 100%;
            background: transparent;
            color: var(--green-primary);
            border: 2px solid var(--green-primary);
            padding: 18px;
            font-family: var(--font-ui);
            font-size: 1.2rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 2px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 10px;
        }

        .btn-process:hover {
            background: var(--green-primary);
            color: #000000;
            box-shadow: 0 0 30px var(--green-glow);
        }

        /* =========================================
           PAINEL DE RESULTADOS TELEMÉTRICOS
           ========================================= */
        .telemetry-results {
            display: none;
            margin-top: 30px;
            padding: 30px;
            background-color: var(--bg-input);
            border-radius: 12px;
            border-left: 5px solid var(--blue-primary);
            animation: slideDown 0.5s ease forwards;
        }

        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .result-header {
            font-size: 1rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }

        .result-r {
            font-family: var(--font-code);
            font-size: 4rem;
            font-weight: 900;
            line-height: 1;
            margin-bottom: 20px;
            color: var(--green-primary);
        }

        .result-status {
            font-weight: 800;
            font-size: 1.2rem;
            padding: 10px 15px;
            border-radius: 6px;
            display: inline-block;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 25px;
            border-top: 1px solid var(--border-color);
            padding-top: 25px;
        }

        .stat-box {
            background: var(--bg-panel);
            padding: 15px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }

        .stat-label { font-size: 0.8rem; color: var(--text-muted); }
        .stat-val { font-family: var(--font-code); font-size: 1.2rem; color: #fff; margin-top: 5px; }

        @media (max-width: 1000px) {
            .dashboard-container { grid-template-columns: 1fr; }
            .hero h1 { font-size: 2.5rem; }
        }
    </style>
</head>
<body>

    <header class="hero">
        <h1>Engine<span class="blue">Rel</span> <span class="green">Analytics</span></h1>
        <p>Modelo de Inteligência de Confiabilidade Baseado em Fadiga Logarítmica e Uso Dinâmico</p>
    </header>

    <main class="dashboard-container">
        
        <section class="panel left-panel">
            <h2 style="color: #fff; margin-bottom: 20px; font-weight: 800;">Alvos de Propulsão</h2>
            
            <div class="image-gallery">
                <img src="BCO.46320da6-8731-4951-83d9-c2b5fd96709e.jpg" alt="Motor de Combustão em Chamas">
                <img src="BCO.ad96e715-3f80-4890-8452-c916d844511e.jpg" alt="Propulsor Foguete em Ignição">
            </div>

            <h3 style="color: var(--blue-primary); margin-top: 30px;">Algoritmo Estrutural</h3>
            
            <div class="math-container">
                $$ R = \frac{\left(1 + \frac{1}{t_c}\right)^{t_c} \cdot \left(\ln\left(\ln\left(\Gamma(\alpha + 2)^{t_c}\right)\right)\right)^2 \cdot e^{\alpha \cdot \lambda}}{u} $$
            </div>

            <ul class="theory-list">
                <li>O sistema processa todas as variáveis de tempo estritamente em <strong>minutos</strong>.</li>
                <li><strong>Gama (Γ):</strong> Catapulta o estresse acumulado. Processado como logaritmo duplo ao quadrado para amplificação exponencial controlada.</li>
                <li><strong>Alpha (α):</strong> Dinâmico. Se <i>tc = 0</i>, α = ln(|u|). Se <i>tc = u</i>, o numerador vira 1. Regra geral: módulo de tc menos u.</li>
                <li><strong>Euler (e):</strong> Fator de maturação limitante sobre as falhas anuais.</li>
            </ul>
        </section>

        <section class="panel right-panel">
            <h2 class="form-title">Console de Telemetria</h2>
            
            <form id="engineForm">
                <div class="input-group">
                    <label>Categoria do Equipamento</label>
                    <select id="engineType">
                        <option value="Combustão">Motor V8 / V6 (Automotivo)</option>
                        <option value="Aeroespacial">Turbofã (Aeroespacial)</option>
                        <option value="Propulsor">Propulsor Foguete (Espacial)</option>
                        <option value="Elétrico">Motor Elétrico Industrial</option>
                    </select>
                </div>

                <div class="input-group">
                    <label>Número de falhas nos últimos 365 dias (Gera o λ)</label>
                    <input type="number" id="failures" value="2" min="0" step="1" required>
                </div>

                <div class="input-group">
                    <label>Tempo desde o último conserto (Em Dias)</label>
                    <input type="number" id="tc_days" value="90" min="0" step="0.1" required>
                </div>

                <div class="input-group">
                    <label>Uso médio diário (Em Horas)</label>
                    <input type="number" id="u_hours" value="18" min="0.1" max="24" step="0.1" required>
                </div>

                <button type="submit" class="btn-process">Processar Confiabilidade</button>
            </form>

            <div class="telemetry-results" id="telemetryPanel">
                <div class="result-header">Índice Dinâmico R (Risco)</div>
                <div class="result-r" id="valR">0.000000</div>
                <div class="result-status" id="statusMessage">Aguardando...</div>

                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-label">TC Analisado (Minutos)</div>
                        <div class="stat-val" id="valTcMin">0</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Uso Diário (Minutos)</div>
                        <div class="stat-val" id="valUMin">0</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Fator de Distância (α)</div>
                        <div class="stat-val" id="valAlpha">0.000</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Taxa de Falha (λ)</div>
                        <div class="stat-val" id="valLambda">0.000</div>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <script>
        // ==========================================
        // 1. APROXIMAÇÃO DE LANCZOS (FUNÇÃO GAMMA)
        // ==========================================
        function gamma(z) {
            const p = [
                0.99999999999980993, 676.5203681218851, -1259.1392167224028,
                771.32342877765313, -176.61502916214059, 12.507343278686905,
                -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7
            ];
            const g = 7;
            if (z < 0.5) return Math.PI / (Math.sin(Math.PI * z) * gamma(1 - z));
            z -= 1;
            let x = p[0];
            for (let i = 1; i < g + 2; i++) {
                x += p[i] / (z + i);
            }
            let t = z + g + 0.5;
            return Math.sqrt(2 * Math.PI) * Math.pow(t, z + 0.5) * Math.exp(-t) * x;
        }

        // ==========================================
        // 2. MOTOR DE CÁLCULO E INTERFACE
        // ==========================================
        document.getElementById('engineForm').addEventListener('submit', function(e) {
            e.preventDefault();

            // Captura
            const failures = parseFloat(document.getElementById('failures').value);
            const tc_days = parseFloat(document.getElementById('tc_days').value);
            const u_hours = parseFloat(document.getElementById('u_hours').value);

            // Conversão Obrigatória para Minutos
            const tc = tc_days * 24 * 60;
            const u = u_hours * 60;

            // Variável Lambda (λ)
            const lambda = failures / 365.0;

            // Regras Estritas do Fator Alfa (α)
            let alpha = 0;
            if (tc === 0) {
                alpha = Math.log(Math.abs(u)) / 1; // tc é 0, denominador seria 1
            } else if (u === tc) {
                alpha = 1 / (tc + 1); // Numerador vira 1
            } else {
                alpha = Math.abs(tc - u) / (tc + 1); // Regra Geral
            }

            // ==========================================
            // IMPLEMENTAÇÃO RIGOROSA DA FÓRMULA
            // ==========================================
            
            // Termo 1: Euler: (1 + 1/tc)^tc
            let eulerTerm = 1; // Padrão se tc = 0
            if (tc > 0) {
                eulerTerm = Math.pow((1 + (1 / tc)), tc);
            }

            // Termo 2: Logaritmo Duplo da Gama ao Quadrado: (ln(ln(Γ(α + 2)^tc)))^2
            // Propriedade algoritmica para evitar travamento: ln(tc * ln(Γ))
            const gammaVal = gamma(alpha + 2);
            let innerLog = Math.log(gammaVal);
            
            // Proteção contra logaritmo de número negativo/zero
            if (innerLog <= 0) innerLog = 0.000001; 
            
            let logLogTerm = 0;
            if (tc > 0) {
                const multiLog = tc * innerLog;
                // Aplicação da elevação ao quadrado inserida aqui:
                logLogTerm = multiLog > 0 ? Math.pow(Math.log(multiLog), 2) : 0;
            } else {
                logLogTerm = 0; // Se tc=0, não há acumulo temporal para catapulta
            }

            // Termo 3: Exponencial: e^(α * λ)
            const expTerm = Math.exp(alpha * lambda);

            // FÓRMULA FINAL R
            let R = 0;
            if (u > 0) {
                R = (eulerTerm * logLogTerm * expTerm) / u;
            }

            // ==========================================
            // ATUALIZAÇÃO DO DASHBOARD FRONT-END
            // ==========================================
            const panel = document.getElementById('telemetryPanel');
            const displayR = document.getElementById('valR');
            const statusMsg = document.getElementById('statusMessage');

            panel.style.display = 'block';
            displayR.innerText = R.toFixed(6);

            // Lógica de Cores e Alertas
            if (R > 1.0) {
                displayR.style.color = "#ff4444"; // Vermelho
                panel.style.borderLeftColor = "#ff4444";
                statusMsg.innerText = "PERIGO: LIMITE ESTRUTURAL ULTRAPASSADO";
                statusMsg.style.backgroundColor = "rgba(255, 68, 68, 0.2)";
                statusMsg.style.color = "#ff4444";
            } else if (R > 0.5) {
                displayR.style.color = "#ffb86c"; // Laranja
                panel.style.borderLeftColor = "#ffb86c";
                statusMsg.innerText = "ALERTA: FADIGA MODERADA / ALTA";
                statusMsg.style.backgroundColor = "rgba(255, 184, 108, 0.2)";
                statusMsg.style.color = "#ffb86c";
            } else {
                displayR.style.color = "var(--green-primary)"; // Verde
                panel.style.borderLeftColor = "var(--green-primary)";
                statusMsg.innerText = "NOMINAL: OPERAÇÃO SEGURA";
                statusMsg.style.backgroundColor = "var(--green-glow)";
                statusMsg.style.color = "var(--green-primary)";
            }

            // Preenchimento das métricas menores
            document.getElementById('valTcMin').innerText = tc.toLocaleString('pt-BR');
            document.getElementById('valUMin').innerText = u.toLocaleString('pt-BR');
            document.getElementById('valAlpha').innerText = alpha.toFixed(5);
            document.getElementById('valLambda').innerText = lambda.toFixed(5);
        });
    </script>
</body>
</html>
"""

# Renderiza o HTML dentro do Streamlit ocupando a tela de forma harmoniosa
components.html(html_code, height=1100, scrolling=True)
