import streamlit as st
import streamlit.components.v1 as components

# Configuração da página para ocupar a tela toda
st.set_page_config(layout="wide", page_title="EngineRel Analytics")

# O código HTML/CSS/JS deve ficar dentro de uma variável de texto (triple quotes)
html_code = """
<!DOCTYPE html>
<html lang="pt-BR">
<style>
    /* O erro estava aqui, porque o Python tentava ler isso sem o componente HTML */
    background: linear-gradient(180deg, rgba(0, 180, 216, 0.1) 0%, var(--bg-dark) 100%);
</style>
<body>
    ...
</body>
</html>
"""

# Comando que faz o Streamlit renderizar o site corretamente
components.html(html_code, height=1200, scrolling=True)
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EngineRel | Índice de Confiabilidade de Motores</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    
    <style>
        /* =========================================
           VARIÁVEIS DE COR E ESTILO (DESIGN SYSTEM)
           ========================================= */
        :root {
            --bg-dark: #0a0c10;
            --bg-panel: #161b22;
            --bg-input: #010409;
            --accent-blue: #00b4d8;
            --accent-blue-glow: rgba(0, 180, 216, 0.4);
            --accent-green: #00ff87;
            --accent-green-glow: rgba(0, 255, 135, 0.3);
            --text-main: #c9d1d9;
            --text-muted: #8b949e;
            --border-color: #30363d;
            --font-ui: 'Inter', sans-serif;
            --font-code: 'JetBrains Mono', monospace;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: var(--font-ui);
            line-height: 1.6;
            overflow-x: hidden;
        }

        /* =========================================
           LAYOUT E ESTRUTURA
           ========================================= */
        header {
            background: linear-gradient(180deg, rgba(0, 180, 216, 0.1) 0%, var(--bg-dark) 100%);
            padding: 40px 20px;
            text-align: center;
            border-bottom: 1px solid var(--border-color);
        }

        header h1 {
            color: #ffffff;
            font-weight: 800;
            font-size: 2.5rem;
            letter-spacing: -1px;
            margin-bottom: 10px;
        }

        header h1 span.blue { color: var(--accent-blue); }
        header h1 span.green { color: var(--accent-green); }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
        }

        /* =========================================
           SEÇÃO DA FÓRMULA E EXPLICAÇÃO
           ========================================= */
        .formula-section {
            background-color: var(--bg-panel);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            position: relative;
            overflow: hidden;
        }

        .formula-section::before {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 4px;
            background: linear-gradient(90deg, var(--accent-blue), var(--accent-green));
        }

        .formula-display {
            background-color: var(--bg-input);
            padding: 20px;
            border-radius: 8px;
            font-size: 1.2rem;
            overflow-x: auto;
            margin: 20px 0;
            border: 1px solid var(--border-color);
            text-align: center;
        }

        .engine-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 8px;
            margin-top: 20px;
            opacity: 0.8;
            border: 1px solid var(--border-color);
        }

        /* =========================================
           FORMULÁRIO E INPUTS
           ========================================= */
        .calculator-panel {
            background-color: var(--bg-panel);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 0 20px var(--accent-blue-glow);
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-size: 0.9rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        input, select {
            width: 100%;
            background-color: var(--bg-input);
            border: 1px solid var(--border-color);
            color: #fff;
            padding: 14px;
            border-radius: 6px;
            font-family: var(--font-code);
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        input:focus, select:focus {
            outline: none;
            border-color: var(--accent-blue);
            box-shadow: 0 0 10px var(--accent-blue-glow);
        }

        button.btn-calc {
            width: 100%;
            background: transparent;
            color: var(--accent-green);
            border: 2px solid var(--accent-green);
            padding: 16px;
            font-size: 1.1rem;
            font-weight: 600;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-top: 10px;
        }

        button.btn-calc:hover {
            background: var(--accent-green);
            color: #000;
            box-shadow: 0 0 20px var(--accent-green-glow);
        }

        /* =========================================
           DASHBOARD DE RESULTADOS
           ========================================= */
        .result-dashboard {
            grid-column: 1 / -1;
            background-color: var(--bg-panel);
            border: 1px solid var(--accent-blue);
            border-radius: 12px;
            padding: 40px;
            display: none;
            animation: fadeIn 0.5s ease forwards;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .result-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .metric-card {
            background-color: var(--bg-input);
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid var(--accent-blue);
        }

        .metric-card.critical { border-left-color: #ff4444; }
        .metric-card.safe { border-left-color: var(--accent-green); }

        .metric-value {
            font-family: var(--font-code);
            font-size: 2rem;
            color: #fff;
            margin-top: 10px;
        }

        /* Responsividade */
        @media (max-width: 900px) {
            .container { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>

    <header>
        <h1>Engine<span class="blue">Rel</span> <span class="green">Analytics</span></h1>
        <p>Plataforma de Mensuração Dinâmica de Confiabilidade para Motores de Alta Performance</p>
    </header>

    <div class="container">
        <section class="formula-section">
            <h2>Modelo Matemático</h2>
            <p style="margin-top: 10px; color: var(--text-muted);">
                A fórmula avalia o estresse mecânico e o histórico de manutenções em minutos, catapultando o risco através da dupla aplicação logarítmica sobre a função Gamma.
            </p>
            
            <div class="formula-display">
                $$ R = \frac{\left(1 + \frac{1}{t_c}\right)^{t_c} \cdot \ln\left(\ln\left(\Gamma(\alpha + 2)^{t_c}\right)\right) \cdot e^{\alpha \cdot \lambda}}{u} $$
            </div>

            <ul style="color: var(--text-muted); margin-left: 20px; font-size: 0.9rem;">
                <li><strong>tc:</strong> Tempo desde o último conserto (em minutos).</li>
                <li><strong>u:</strong> Tempo de uso diário médio (em minutos).</li>
                <li><strong>λ (Lambda):</strong> Falhas/ano ÷ 365.</li>
                <li><strong>α (Alpha):</strong> Ajuste dinâmico com base no módulo |tc - u|/(tc+1).</li>
            </ul>

            <img src="https://images.unsplash.com/photo-1517976487492-5750f3195933?auto=format&fit=crop&q=80&w=800" alt="Turbina de Avião" class="engine-image">
        </section>

        <section class="calculator-panel">
            <h2 style="color: #fff; margin-bottom: 25px;">Parâmetros do Motor</h2>
            <form id="engineForm">
                
                <div class="form-group">
                    <label>Tipo de Motor</label>
                    <select id="engineType">
                        <option value="Carro">Motor de Combustão (Carro)</option>
                        <option value="Turbina">Turbina Aeronáutica</option>
                        <option value="Foguete">Motor de Foguete (Propulsão)</option>
                        <option value="Eletrico">Motor Elétrico Industrial</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Falhas nos últimos 365 dias</label>
                    <input type="number" id="breakdowns" value="2" min="0" step="1" required>
                </div>

                <div class="form-group">
                    <label>Tempo desde o último conserto (em DIAS)</label>
                    <input type="number" id="tc_days" value="90" min="0" step="0.1" required>
                    <small style="color: var(--text-muted); font-size: 0.8rem;">O sistema converterá para minutos (tc).</small>
                </div>

                <div class="form-group">
                    <label>Tempo de uso médio diário (em HORAS)</label>
                    <input type="number" id="u_hours" value="18" min="0" max="24" step="0.1" required>
                    <small style="color: var(--text-muted); font-size: 0.8rem;">O sistema converterá para minutos (u).</small>
                </div>

                <button type="submit" class="btn-calc">Processar Confiabilidade</button>
            </form>
        </section>

        <section class="result-dashboard" id="resultDashboard">
            <h2 style="color: var(--accent-blue);">Relatório de Telemetria Analítica</h2>
            <p id="systemMessage" style="color: var(--text-muted);"></p>
            
            <div class="result-grid">
                <div class="metric-card">
                    <label>Índice R (Perigo)</label>
                    <div class="metric-value" id="valR" style="color: var(--accent-blue);">0.000</div>
                </div>
                <div class="metric-card">
                    <label>Tempo Conserto (tc - min)</label>
                    <div class="metric-value" id="valTc">0</div>
                </div>
                <div class="metric-card">
                    <label>Tempo Uso (u - min)</label>
                    <div class="metric-value" id="valU">0</div>
                </div>
                <div class="metric-card">
                    <label>Fator Alfa (α)</label>
                    <div class="metric-value" id="valAlpha">0.000</div>
                </div>
            </div>
        </section>
    </div>

    <script>
        // Aproximação de Lanczos para a Função Gamma Γ(z)
        // Necessário pois JS não tem Math.gamma nativo
        function gamma(z) {
            const g = 7;
            const p = [
                0.99999999999980993,
                676.5203681218851,
                -1259.1392167224028,
                771.32342877765313,
                -176.61502916214059,
                12.507343278686905,
                -0.13857109526572012,
                9.9843695780195716e-6,
                1.5056327351493116e-7
            ];
            if (z < 0.5) return Math.PI / (Math.sin(Math.PI * z) * gamma(1 - z));
            z -= 1;
            let x = p[0];
            for (let i = 1; i < g + 2; i++) {
                x += p[i] / (z + i);
            }
            let t = z + g + 0.5;
            return Math.sqrt(2 * Math.PI) * Math.pow(t, z + 0.5) * Math.exp(-t) * x;
        }

        document.getElementById('engineForm').addEventListener('submit', function(e) {
            e.preventDefault();

            // 1. Captura de Dados
            const breakdowns = parseFloat(document.getElementById('breakdowns').value);
            const tc_days = parseFloat(document.getElementById('tc_days').value);
            const u_hours = parseFloat(document.getElementById('u_hours').value);
            const engineType = document.getElementById('engineType').value;

            // 2. Conversão Estrita para Minutos
            const tc = tc_days * 24 * 60; // Dias para minutos
            const u = u_hours * 60;       // Horas para minutos

            // Tratamento de divisão por zero caso u seja 0
            if (u === 0) {
                alert("O uso diário não pode ser zero absoluto para o denominador da fórmula.");
                return;
            }

            // 3. Cálculo do Lambda (λ)
            const lambda = breakdowns / 365.0;

            // 4. Cálculo rigoroso do Alfa (α) conforme regras de contorno
            let alpha = 0;
            if (tc === 0) {
                // Numerador vira ln(|u|)
                alpha = Math.log(Math.abs(u)) / 1; 
            } else if (u === tc) {
                // Numerador vira 1
                alpha = 1 / (tc + 1);
            } else {
                // Regra Geral: Módulo
                alpha = Math.abs(tc - u) / (tc + 1);
            }

            // 5. O Termo Logaritmo Duplo da Gama: ln(ln( Γ(α + 2)^tc ))
            // Usamos a propriedade logarítmica para evitar overflow no processador: ln(x^y) = y*ln(x)
            const gammaVal = gamma(alpha + 2);
            // Prevenção de logaritmo negativo caso a gamma seja 1 ou menor e dê problema no segundo ln
            let innerLog = Math.log(gammaVal);
            if (innerLog <= 0) innerLog = 0.0001; // Proteção matemática de software
            
            const outerLogTerm = Math.log(tc * innerLog);

            // 6. O Termo de Euler: (1 + 1/tc)^tc
            // Tratamento limite se tc for 0 para evitar Infinity/NaN
            const eulerTerm = (tc === 0) ? 1 : Math.pow((1 + (1 / tc)), tc);

            // 7. O Termo Exponencial: e^(α * λ)
            const expTerm = Math.exp(alpha * lambda);

            // 8. O Cálculo Final de R
            const R = (eulerTerm * outerLogTerm * expTerm) / u;

            // 9. Atualização da UI
            document.getElementById('resultDashboard').style.display = 'block';
            
            const rDisplay = document.getElementById('valR');
            rDisplay.innerText = R.toFixed(6);
            
            // Lógica de Cores baseada no risco
            if(R > 1.0) {
                rDisplay.style.color = "#ff4444"; // Vermelho Crítico
                document.getElementById('systemMessage').innerHTML = `ALERTA CRÍTICO: O ${engineType} ultrapassou o limite operacional seguro de confiabilidade.`;
            } else if (R > 0.5) {
                rDisplay.style.color = "#ffb86c"; // Amarelo Alerta
                document.getElementById('systemMessage').innerHTML = `ATENÇÃO: Fadiga moderada detectada no ${engineType}. Planejar manutenção.`;
            } else {
                rDisplay.style.color = var(--accent-green); // Verde Seguro
                document.getElementById('systemMessage').innerHTML = `OPERAÇÃO SEGURA: O ${engineType} opera dentro das margens toleráveis.`;
            }

            document.getElementById('valTc').innerText = tc.toLocaleString('pt-BR');
            document.getElementById('valU').innerText = u.toLocaleString('pt-BR');
            document.getElementById('valAlpha').innerText = alpha.toFixed(4);

            // Rola a tela suavemente até os resultados
            document.getElementById('resultDashboard').scrollIntoView({ behavior: 'smooth' });
        });
    </script>
</body>
</html>

