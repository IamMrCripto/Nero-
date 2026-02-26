import streamlit as st
import streamlit.components.v1 as components

# =====================================================================
# CONFIGURAÇÃO GLOBAL DO STREAMLIT
# Configurações iniciais da página para garantir que o layout use
# toda a largura disponível e oculte os elementos nativos do framework.
# =====================================================================
st.set_page_config(
    page_title="EngineRel | Reliability Analytics",
    page_icon=" ⚙️ ",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Injeção de CSS nativo no Streamlit para ocultar cabeçalho, rodapé e menu
hide_st_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
    }
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# =====================================================================
# CÓDIGO FONTE DA APLICAÇÃO (SINGLE PAGE APPLICATION)
# Contém HTML semântico, CSS (Dark/Neon Theme) e JavaScript (Lógica).
# Utilizamos 'r' antes da string para preservar as barras do LaTeX.
# =====================================================================
html_code = r"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Sistema de análise de confiabilidade de propulsores baseado na Equação Quimera.">
    <title>EngineRel - Dashboard Telemétrico</title>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800;900&family=JetBrains+Mono:wght@400;700;800&display=swap" rel="stylesheet">

    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

    <style>
        /* =====================================================================
           SISTEMA DE DESIGN: VARIÁVEIS GLOBAIS
           Definição de paleta de cores, tipografia e espaçamentos.
        ===================================================================== */
        :root {
            /* Paleta de Cores de Fundo */
            --bg-base: #09090b;
            --bg-panel: #18181b;
            --bg-input: #000000;

            /* Paleta de Cores de Destaque (Neon) */
            --blue-primary: #00d2ff;
            --blue-glow: rgba(0, 210, 255, 0.3);
            
            --green-primary: #39ff14;
            --green-glow: rgba(57, 255, 20, 0.2);
            
            --red-primary: #ff2a2a;
            --red-glow: rgba(255, 42, 42, 0.3);
            
            --purple-primary: #b026ff;
            --purple-glow: rgba(176, 38, 255, 0.2);
            
            --orange-primary: #ffb86c;
            --orange-glow: rgba(255, 184, 108, 0.2);

            /* Tipografia e Bordas */
            --text-main: #e4e4e7;
            --text-muted: #a1a1aa;
            --border-color: #27272a;

            --font-ui: 'Inter', sans-serif;
            --font-code: 'JetBrains Mono', monospace;

            /* Sombras Padrão */
            --shadow-panel: 0 10px 30px rgba(0, 0, 0, 0.8);
        }

        /* =====================================================================
           RESET E CONFIGURAÇÕES BÁSICAS
        ===================================================================== */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-base);
            color: var(--text-main);
            font-family: var(--font-ui);
            line-height: 1.6;
            padding: 20px;
            overflow-x: hidden;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* Customização da Barra de Rolagem */
        ::-webkit-scrollbar {
            width: 10px;
        }
        ::-webkit-scrollbar-track {
            background: var(--bg-base);
        }
        ::-webkit-scrollbar-thumb {
            background: var(--border-color);
            border-radius: 5px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--blue-primary);
        }

        /* =====================================================================
           CABEÇALHO E NAVEGAÇÃO (TABS)
        ===================================================================== */
        .app-header {
            text-align: center;
            margin-bottom: 30px;
            padding-top: 20px;
        }

        .nav-tabs {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 40px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 10px;
        }

        .tab-btn {
            background: transparent;
            color: var(--text-muted);
            border: none;
            font-size: 1.2rem;
            font-weight: 800;
            cursor: pointer;
            padding: 10px 20px;
            text-transform: uppercase;
            letter-spacing: 2px;
            transition: all 0.3s ease;
            position: relative;
        }

        .tab-btn:hover {
            color: var(--text-main);
        }

        .tab-btn.active {
            color: var(--blue-primary);
            text-shadow: 0 0 10px var(--blue-glow);
        }

        .tab-btn.active::after {
            content: '';
            position: absolute;
            bottom: -11px;
            left: 0;
            width: 100%;
            height: 3px;
            background: var(--blue-primary);
            box-shadow: 0 0 10px var(--blue-glow);
        }

        /* Transições de Conteúdo das Abas */
        .tab-content {
            display: none;
            animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
            flex-grow: 1;
        }

        .tab-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* =====================================================================
           ESTRUTURA DE GRIDS E PAINÉIS
        ===================================================================== */
        .grid-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            max-width: 1400px;
            margin: 0 auto;
        }

        .single-container {
            max-width: 1000px;
            margin: 0 auto;
        }

        .panel {
            background-color: var(--bg-panel);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 40px;
            box-shadow: var(--shadow-panel);
            position: relative;
            overflow: hidden;
        }

        .panel::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, var(--blue-primary), var(--purple-primary));
            opacity: 0.5;
        }

        .panel-title {
            color: #ffffff;
            font-size: 1.8rem;
            font-weight: 900;
            margin-bottom: 25px;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        /* =====================================================================
           ABA 1: TEORIA E SISTEMAS DINÂMICOS
        ===================================================================== */
        .theory-text {
            font-size: 1.1rem;
            color: var(--text-muted);
            margin-bottom: 20px;
            text-align: justify;
            line-height: 1.8;
        }

        .theory-highlight {
            color: var(--purple-primary);
            font-weight: 800;
            text-shadow: 0 0 10px var(--purple-glow);
        }

        .math-box {
            background-color: var(--bg-input);
            padding: 30px;
            border-radius: 12px;
            border: 1px solid var(--purple-primary);
            box-shadow: inset 0 0 30px var(--purple-glow);
            text-align: center;
            font-size: 1.5rem;
            margin: 30px 0;
            overflow-x: auto;
        }

        .feature-list {
            list-style-type: none;
            margin-top: 20px;
        }

        .feature-list li {
            position: relative;
            padding-left: 25px;
            margin-bottom: 15px;
            color: var(--text-muted);
            font-size: 1.1rem;
        }

        .feature-list li::before {
            content: ' ⊳ ';
            position: absolute;
            left: 0;
            color: var(--blue-primary);
            font-weight: bold;
        }

        /* =====================================================================
           ABA 2: DASHBOARD (GALERIA E FORMULÁRIOS)
        ===================================================================== */
        .image-gallery {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-bottom: 30px;
        }

        .image-gallery img {
            width: 100%;
            height: 220px;
            object-fit: cover;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            transition: all 0.4s ease;
            filter: grayscale(60%) opacity(0.8);
        }

        .image-gallery img:hover {
            filter: grayscale(0%) opacity(1);
            border-color: var(--blue-primary);
            box-shadow: 0 0 20px var(--blue-glow);
            transform: scale(1.02);
        }
        
        .alert-box {
            background: var(--bg-input);
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid var(--blue-primary);
            margin-top: 20px;
        }

        .alert-box p {
            color: var(--text-muted);
            font-size: 0.95rem;
            line-height: 1.5;
        }

        /* Campos de Formulário */
        .input-group {
            margin-bottom: 25px;
            position: relative;
        }

        .input-group label {
            display: block;
            font-size: 0.85rem;
            font-weight: 800;
            color: var(--blue-primary);
            text-transform: uppercase;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }

        .input-group input,
        .input-group select {
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

        .input-group input:focus,
        .input-group select:focus {
            outline: none;
            border-color: var(--blue-primary);
            box-shadow: 0 0 15px var(--blue-glow);
        }

        /* Botão de Processamento */
        .btn-process {
            width: 100%;
            background: transparent;
            color: var(--blue-primary);
            border: 2px solid var(--blue-primary);
            padding: 18px;
            font-family: var(--font-ui);
            font-size: 1.2rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 2px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            margin-top: 10px;
        }

        .btn-process:hover {
            background: var(--blue-primary);
            color: #000000;
            box-shadow: 0 0 30px var(--blue-glow);
        }

        .btn-process:disabled {
            border-color: var(--border-color);
            color: var(--border-color);
            cursor: not-allowed;
            background: transparent;
            box-shadow: none;
        }

        /* =====================================================================
           RESULTADOS TELEMÉTRICOS
        ===================================================================== */
        .telemetry-results {
            display: none;
            margin-top: 30px;
            padding: 30px;
            background-color: var(--bg-input);
            border-radius: 12px;
            border-left: 5px solid var(--border-color);
            transition: all 0.5s ease;
        }

        .result-r {
            font-family: var(--font-code);
            font-size: 4.5rem;
            font-weight: 900;
            line-height: 1;
            margin: 15px 0;
            text-shadow: 0 0 20px rgba(0,0,0,0.5);
        }

        .result-status {
            font-weight: 900;
            font-size: 1.2rem;
            padding: 12px 20px;
            border-radius: 6px;
            display: inline-block;
            text-transform: uppercase;
            letter-spacing: 1px;
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

        .stat-label {
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 800;
        }

        .stat-val {
            font-family: var(--font-code);
            font-size: 1.3rem;
            color: #ffffff;
            margin-top: 5px;
            font-weight: 700;
        }

        /* =====================================================================
           RODAPÉ E LOADING SIMULATION
        ===================================================================== */
        .loading-spinner {
            display: none;
            text-align: center;
            margin-top: 20px;
            color: var(--blue-primary);
            font-family: var(--font-code);
            font-weight: bold;
            animation: pulse 1s infinite;
        }

        @keyframes pulse {
            0% { opacity: 0.5; }
            50% { opacity: 1; }
            100% { opacity: 0.5; }
        }

        footer {
            text-align: center;
            padding: 40px 20px;
            color: var(--border-color);
            font-size: 0.9rem;
            margin-top: auto;
        }

        /* =====================================================================
           MEDIA QUERIES (RESPONSIVIDADE)
        ===================================================================== */
        @media (max-width: 1200px) {
            .grid-container {
                gap: 20px;
            }
            .panel {
                padding: 30px;
            }
        }

        @media (max-width: 992px) {
            .grid-container {
                grid-template-columns: 1fr;
            }
            .result-r {
                font-size: 3.5rem;
            }
        }

        @media (max-width: 576px) {
            .nav-tabs {
                flex-direction: column;
                align-items: center;
            }
            .tab-btn {
                width: 100%;
                text-align: center;
            }
            .stats-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>

    <header class="app-header">
        <h1 style="font-size: 2.5rem; font-weight: 900; color: #fff;">
            Engine<span style="color: var(--blue-primary)">Rel</span>
        </h1>
    </header>

    <nav class="nav-tabs" aria-label="Navegação Principal">
        <button class="tab-btn active" onclick="openTab('tab-theory')" id="btn-theory">
            Visão & Teoria
        </button>
        <button class="tab-btn" onclick="openTab('tab-dashboard')" id="btn-dashboard">
            Dashboard Telemétrico
        </button>
    </nav>

    <main id="tab-theory" class="tab-content active" role="tabpanel">
        <div class="single-container panel">
            <div class="panel-title">
                Modelagem Quimera (Multi-Fator)
                <span style="font-size: 0.9rem; color: var(--text-muted); font-weight: 400;">v4.0.0</span>
            </div>
            
            <p class="theory-text">
                A fórmula do <strong>EngineRel</strong> transcende a simples métrica de falhas pontuais. 
                Ela é uma abstração matemática projetada para descrever o comportamento de um 
                <span class="theory-highlight">Sistema Dinâmico Não-Linear</span>.
                Sistemas mecânicos de alta complexidade operam em um estado de equilíbrio tênue, 
                onde o tempo absoluto, o desgaste físico e a consistência de uso interagem de forma caótica.
            </p>

            <div class="math-box">
                $$ R = \frac{e^{\alpha \lambda} \cdot \ln(\ln(\Gamma(\alpha + 2))) \cdot \sqrt{t_{cd}} \cdot \left(1 + \frac{1}{t_c}\right)^{t_c}}{u} $$
            </div>

            <h3 style="color: #ffffff; margin: 40px 0 20px 0; font-weight: 800;">Análise Vetorial do Sistema</h3>
            
            <ul class="feature-list">
                <li>
                    <strong>O Atrator de Euler:</strong> O termo \( (1 + 1/t_c)^{t_c} \) atua como um atrator de 
                    estabilidade no espaço de fase. À medida que o tempo (\( t_c \)) passa sem interrupções, 
                    o sistema converge assintoticamente para a constante de Euler (\( e \)), sugerindo matematicamente 
                    que as falhas prematuras (mortalidade infantil de engenharia) foram superadas.
                </li>
                <li>
                    <strong>A Raiz de Desgaste (\( \sqrt{t_{cd}} \)):</strong> Introduzida para modelar a fadiga de material a longo prazo, converte os dias corridos (\( t_{cd} \)) num fator de escalada geométrica, suavizando a curva de risco nas fases iniciais.
                </li>
                <li>
                    <strong>Micro-Falhas e Função Gama:</strong> O bloco logarítmico duplo de Gama garante que a taxa de estragos (\( \lambda \)) ponderada pelas condições limítrofes operacionais (\( \alpha \)) amorteça números infinitos sem perder o rasto do estado microscópico da mecânica.
                </li>
            </ul>
        </div>
    </main>

    <main id="tab-dashboard" class="tab-content" role="tabpanel">
        <div class="grid-container">
            
            <section class="panel">
                <div class="panel-title">
                    Alvos de Propulsão 
                    <span style="font-size: 1.2rem;"> 🚀 </span>
                </div>
                
                <div class="image-gallery">
                    <img src="https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?auto=format&fit=crop&q=80" alt="Motor de Combustão V8 em operação com alta temperatura">
                    <img src="https://images.unsplash.com/photo-1541185933-ef5d8ed016c2?auto=format&fit=crop&q=80" alt="Exaustão de um propulsor de foguete espacial durante lançamento">
                </div>

                <div class="alert-box">
                    <p>
                        <strong> ⚠️  Aviso de Restrição do Sistema:</strong><br>
                        O núcleo algorítmico do índice \( R \) foi atualizado para a arquitetura Quimera. 
                        A complexidade analítica integra micro-falhas (\( \alpha \) e \( \lambda \)) com a elegância da degradação estrutural em dias (\( \sqrt{t_{cd}} \)). Valide rigorosamente os inputs para evitar cálculos assintóticos imprevistos.
                    </p>
                </div>
            </section>

            <section class="panel">
                <div class="panel-title">
                    Console de Telemetria 
                    <span style="font-size: 1.2rem;"> ⏱️ </span>
                </div>

                <form id="engineForm" novalidate>
                    <div class="input-group">
                        <label for="engineType">Perfil Estrutural do Equipamento</label>
                        <select id="engineType" name="engineType">
                            <option value="Combustão">Motor V8 / V6 (Automotivo Pesado)</option>
                            <option value="Aeroespacial">Turbofã (Aeroespacial Comercial)</option>
                            <option value="Propulsor">Propulsor Criogênico (Espacial)</option>
                            <option value="Gerador">Gerador a Diesel (Uso Contínuo)</option>
                        </select>
                    </div>

                    <div class="input-group">
                        <label for="failures">Eventos de Falha (Histórico 365 dias)</label>
                        <input type="number" id="failures" name="failures" value="3" min="0" step="1" required 
                               placeholder="Ex: 2">
                    </div>

                    <div class="input-group">
                        <label for="tc_days">Ciclo desde o último reparo (Em Dias)</label>
                        <input type="number" id="tc_days" name="tc_days" value="7000" min="0" step="0.1" required 
                               placeholder="Ex: 365">
                    </div>

                    <div class="input-group">
                        <label for="u_hours">Carga Operacional Diária Média (Em Horas)</label>
                        <input type="number" id="u_hours" name="u_hours" value="18" min="0.1" max="24" step="0.1" required 
                               placeholder="Ex: 12.5">
                    </div>

                    <button type="submit" class="btn-process" id="btnSubmit">
                        Processar Vetor de Risco (R)
                    </button>

                    <div class="loading-spinner" id="loadingState">
                        [ CALIBRANDO MATRIZ DE DADOS... AGUARDE ]
                    </div>
                </form>

                <div class="telemetry-results" id="telemetryPanel">
                    <div style="font-size: 0.9rem; color: var(--text-muted); font-weight: 800; letter-spacing: 2px;">
                        ÍNDICE GLOBAL DE RISCO ESTRUTURAL
                    </div>
                    
                    <div class="result-r" id="valR">0.000000</div>
                    <div class="result-status" id="statusMessage">Aguardando telemetria...</div>

                    <div class="stats-grid">
                        <div class="stat-box">
                            <div class="stat-label">Minutos Acumulados (tc)</div>
                            <div class="stat-val" id="valTcMin">0</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-label">Minutos Uso Diário (u)</div>
                            <div class="stat-val" id="valUMin">0</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-label">Fator de Desvio (α)</div>
                            <div class="stat-val" id="valAlpha">0.000000</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-label">Taxa Lambda Anual (λ)</div>
                            <div class="stat-val" id="valLambda">0.000000</div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    </main>

    <footer>
        EngineRel Analytics System &copy; 2026. Desenvolvido para modelagem de ambientes extremos.
    </footer>

    <script>
        /**
         * FUNÇÃO DE CONTROLE DE INTERFACE (SPA ROUTING)
         * Alterna entre as abas alterando as classes CSS ativas.
         * @param {string} tabId - O ID do elemento <main> a ser exibido.
         */
        function openTab(tabId) {
            try {
                // Esconde todas as abas de conteúdo
                const contents = document.querySelectorAll('.tab-content');
                contents.forEach(tab => {
                    tab.classList.remove('active');
                });

                // Remove o estilo ativo de todos os botões
                const buttons = document.querySelectorAll('.tab-btn');
                buttons.forEach(btn => {
                    btn.classList.remove('active');
                });

                // Ativa a aba solicitada e o botão correspondente
                document.getElementById(tabId).classList.add('active');
                event.currentTarget.classList.add('active');
            } catch (error) {
                console.error("Erro na navegação de abas: ", error);
            }
        }

        /**
         * APROXIMAÇÃO DE LANCZOS PARA A FUNÇÃO GAMA
         * A Função Gama estende o fatorial para números complexos e reais.
         * Essa implementação utiliza coeficientes pré-calculados para alta precisão.
         * @param {number} z - O valor de entrada.
         * @returns {number} O valor aproximado de Gama(z).
         */
        function gamma(z) {
            // Constantes de Lanczos para g = 7
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

            const g = 7;

            // Fórmula de reflexão se z < 0.5
            if (z < 0.5) {
                return Math.PI / (Math.sin(Math.PI * z) * gamma(1 - z));
            }

            z -= 1;
            let x = p[0];

            for (let i = 1; i < g + 2; i++) {
                x += p[i] / (z + i);
            }

            let t = z + g + 0.5;

            // Equação final de Lanczos
            return Math.sqrt(2 * Math.PI) * Math.pow(t, z + 0.5) * Math.exp(-t) * x;
        }

        /**
         * MOTOR DE CÁLCULO E MANIPULAÇÃO DO DOM
         * Intercepta o envio do formulário, processa os dados matemáticos,
         * simula o carregamento e atualiza a interface com as cores apropriadas.
         */
        document.getElementById('engineForm').addEventListener('submit', function(e) {
            // Impede o recarregamento da página padrão do form HTML
            e.preventDefault();

            // 1. CAPTURA E VALIDAÇÃO DOS DADOS DE ENTRADA
            const inputFailures = document.getElementById('failures').value;
            const inputTcDays = document.getElementById('tc_days').value;
            const inputUHours = document.getElementById('u_hours').value;

            // Verificação de inputs vazios ou inválidos
            if (!inputFailures || !inputTcDays || !inputUHours) {
                alert("Erro de Validação: Todos os parâmetros telemétricos são obrigatórios.");
                return;
            }

            const failures = parseFloat(inputFailures);
            const tcDays = parseFloat(inputTcDays);
            const uHours = parseFloat(inputUHours);

            if (uHours <= 0 || uHours > 24) {
                alert("Aviso: O uso diário deve ser estritamente maior que 0 e máximo de 24 horas.");
                return;
            }

            // Manipulação de UI para iniciar a simulação de processamento
            const btnSubmit = document.getElementById('btnSubmit');
            const loadingState = document.getElementById('loadingState');
            const panel = document.getElementById('telemetryPanel');

            btnSubmit.style.display = 'none';
            loadingState.style.display = 'block';
            panel.style.display = 'none';

            // Simulação assíncrona para efeito de processamento de dados (1.5 segundos)
            setTimeout(() => {

                try {
                    // 2. CONVERSÃO DE UNIDADES PARA A BASE MATEMÁTICA (MINUTOS E DIAS)
                    const tc = tcDays * 24 * 60; // Dias transformados em minutos
                    const u = uHours * 60;       // Horas transformadas em minutos

                    // Cálculo da taxa histórica de falha ao ano (λ)
                    const lambda = failures / 365.0;

                    // 3. DEFINIÇÃO RIGOROSA DO FATOR ALFA (α) [SEGUNDO AS ESPECIFICAÇÕES DO MODELO]
                    let numAlpha = 0;
                    if (tc === 0) {
                        numAlpha = Math.log(Math.abs(u));
                    } else if (tc === u) {
                        numAlpha = 1;
                    } else {
                        numAlpha = Math.abs(tc - u);
                    }
                    const alpha = numAlpha / (tc + 1);

                    // 4. RESOLUÇÃO DA EQUAÇÃO DE RISCO (R) - MODELO QUIMERA
                    
                    // 4.1. Termo de Fadiga Temporal (Raiz de tcd)
                    const rootTcd = Math.sqrt(tcDays);

                    // 4.2. Termo Estabilizador de Euler
                    let eulerTerm = 1;
                    if (tc > 0) {
                        eulerTerm = Math.pow((1 + (1 / tc)), tc);
                    }

                    // 4.3. Termo de Micro-Fadiga (Logaritmo Duplo da Função Gama)
                    const gammaVal = gamma(alpha + 2);
                    let innerLog = Math.log(gammaVal);

                    // Proteção de domínio para evitar NaN em logaritmos naturais
                    if (innerLog <= 0) {
                        innerLog = 0.000001; 
                    }

                    let logLogTerm = Math.log(innerLog);
                    if (logLogTerm < 0 && tc === 0) { logLogTerm = 0; } // Trava de segurança no ponto zero

                    // 4.4. Termo Exponencial de Maturação de Falhas
                    const expTerm = Math.exp(alpha * lambda);

                    // 4.5. Síntese Final do Índice R
                    let R = 0;
                    if (u > 0) {
                        R = (expTerm * logLogTerm * rootTcd * eulerTerm) / u;
                    }

                    // 5. ATUALIZAÇÃO DO FRONT-END E LÓGICA DE CORES
                    const displayR = document.getElementById('valR');
                    const statusMsg = document.getElementById('statusMessage');

                    // Formatação do número usando notação científica se o número for ínfimo, ou com 4 casas decimais 
                    displayR.innerText = R < 0.001 ? R.toExponential(4) : R.toFixed(4);

                    // Lógica Condicional de Alertas Visuais
                    if (R > 1.0) {
                        // ESTADO: PERIGO (VERMELHO NEON)
                        displayR.style.color = "var(--red-primary)";
                        displayR.style.textShadow = "0 0 20px var(--red-glow)";
                        panel.style.borderLeftColor = "var(--red-primary)";
                        statusMsg.innerText = "CRÍTICO: COLAPSO ESTRUTURAL IMINENTE";
                        statusMsg.style.backgroundColor = "var(--red-glow)";
                        statusMsg.style.color = "var(--red-primary)";
                        statusMsg.style.border = "1px solid var(--red-primary)";
                    }
                    else if (R > 0.5) {
                        // ESTADO: ALERTA (LARANJA NEON)
                        displayR.style.color = "var(--orange-primary)";
                        displayR.style.textShadow = "0 0 20px var(--orange-glow)";
                        panel.style.borderLeftColor = "var(--orange-primary)";
                        statusMsg.innerText = "ALERTA: FADIGA DE MATERIAL DETECTADA";
                        statusMsg.style.backgroundColor = "var(--orange-glow)";
                        statusMsg.style.color = "var(--orange-primary)";
                        statusMsg.style.border = "1px solid var(--orange-primary)";
                    }
                    else {
                        // ESTADO: NOMINAL (VERDE NEON)
                        displayR.style.color = "var(--green-primary)";
                        displayR.style.textShadow = "0 0 20px var(--green-glow)";
                        panel.style.borderLeftColor = "var(--green-primary)";
                        statusMsg.innerText = "NOMINAL: INTEGRIDADE CONFIRMADA";
                        statusMsg.style.backgroundColor = "var(--green-glow)";
                        statusMsg.style.color = "var(--green-primary)";
                        statusMsg.style.border = "1px solid var(--green-primary)";
                    }

                    // Alimentando a grade inferior de estatísticas isoladas 
                    document.getElementById('valTcMin').innerText = tc.toLocaleString('pt-BR'); 
                    document.getElementById('valUMin').innerText = u.toLocaleString('pt-BR'); 
                    document.getElementById('valAlpha').innerText = alpha.toFixed(6); 
                    document.getElementById('valLambda').innerText = lambda.toFixed(6); 

                } catch (error) {
                    console.error("Falha Crítica no Processador Matemático:", error);
                    alert("Ocorreu um erro no cálculo do vetor. Verifique o console.");
                } finally {
                    // Retorna a UI ao estado interativo, revelando os resultados
                    loadingState.style.display = 'none';
                    btnSubmit.style.display = 'block';
                    panel.style.display = 'block';
                }

            }, 1500); // Fim do setTimeout (1.5s)
        });
    </script>
</body>
</html>
"""

# Renderização do Componente no Streamlit com altura dinâmica generosa
components.html(html_code, height=1300, scrolling=True)
