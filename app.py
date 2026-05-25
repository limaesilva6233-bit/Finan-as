import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf

# 1. Configuração da página (modo amplo e título do sistema)
st.set_page_config(page_title="QUANTUM | Wealth OS", layout="wide", page_icon="⚡")

# 2. Injeção de CSS Avançado para correspondência exata do Layout HUD Futurista
BACKGROUND_IMAGE_URL = "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=1200&auto=format&fit=crop"

st.markdown(f"""
    <style>
        /* Importação da fonte Inter */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        /* Reset e Fundo Escuro Absoluto */
        .stApp {{
            background-color: #03070c !important;
            color: #e2e8f0 !important;
            font-family: 'Inter', sans-serif !important;
        }}
        
        /* Imagem de Fundo de Alta Tecnologia (HUD Glow) */
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background-image: url('{BACKGROUND_IMAGE_URL}');
            background-size: cover;
            background-position: center;
            opacity: 0.12;
            z-index: -1;
            pointer-events: none;
        }}
        
        /* Forçar todos os textos normais, parágrafos e marcações para Branco/Cinza Claro */
        .stApp p, .stApp span, .stApp label, .stApp div {{
            color: #e2e8f0 !important;
        }}
        
        /* Correção Crítica: Legibilidade total dos Inputs na Sidebar e Painel */
        div[data-testid="stSidebar"] {{
            background-color: #070c14 !important;
            border-right: 1px solid #1e293b !important;
        }}
        
        div[data-testid="stSidebar"] p, div[data-testid="stSidebar"] label {{
            color: #94a3b8 !important;
            font-weight: 600 !important;
        }}
        
        /* Estilização das caixas de entrada de número e seletores (Inputs legíveis e bonitos) */
        .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
            background-color: #0d1527 !important;
            color: #ffffff !important;
            border: 1px solid #334155 !important;
            border-radius: 6px !important;
        }}
        
        /* Estilização dos Containers Translucidos (Glassmorphism de Alta Fidelidade) */
        div[data-testid="stContainer"] {{
            background: rgba(10, 17, 30, 0.75) !important;
            border: 1px solid rgba(51, 65, 85, 0.5) !important;
            border-radius: 12px !important;
            padding: 20px !important;
            backdrop-filter: blur(8px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        }}
        
        /* Títulos Prateados e brilhantes */
        h1, h2, h3, h4 {{
            color: #ffffff !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }}
        
        /* Estilização das Abas (Tabs) para combinarem com o menu superior */
        div[data-testid="stTabBar"] button {{
            color: #94a3b8 !important;
            font-weight: 600 !important;
            background: transparent !important;
            border: none !important;
        }}
        div[data-testid="stTabBar"] button[aria-selected="true"] {{
            color: #00E676 !important;
            border-bottom: 2px solid #00E676 !important;
        }}
        
        /* Customização dos Tickers de Mercado (Faixa do topo) */
        .ticker-bar {{
            background: #070b12;
            padding: 8px 15px;
            border-radius: 6px;
            border: 1px solid #1e293b;
            display: flex;
            gap: 20px;
            overflow-x: auto;
            margin-bottom: 15px;
        }}
        .ticker-item {{
            font-size: 0.85rem;
            white-space: nowrap;
        }}
        .ticker-green {{ color: #00E676 !important; font-weight: bold; }}
        .ticker-red {{ color: #ff5252 !important; font-weight: bold; }}
    </style>
""", unsafe_allowed_html=True)

# --- COLETA DE DADOS REAIS (YFINANCE) ---
@st.cache_data(ttl=1800)
def fetch_market_data():
    data = {"dolar": 5.25, "ouro_g": 395.0, "cdi": 10.50, "sp500": 8.5, "ipca": 4.20, "fiis": 1.5}
    try:
        # Dólar
        df_usd = yf.Ticker("BRL=X").history(period="1d")
        if not df_usd.empty: data["dolar"] = df_usd['Close'].iloc[-1]
        # Ouro Oz -> convertido para grama
        df_gold = yf.Ticker("GC=F").history(period="1d")
        if not df_gold.empty:
            data["ouro_g"] = (df_gold['Close'].iloc[-1] * data["dolar"]) / 31.1035
        # S&P 500 YTD
        df_sp = yf.Ticker("^GSPC").history(period="ytd")
        if len(df_sp) > 1: data["sp500"] = ((df_sp['Close'].iloc[-1] / df_sp['Close'].iloc[0]) - 1) * 100
    except:
        pass
    return data

m_data = fetch_market_data()

# --- 3. BARRA DE TICKERS EM TEMPO REAL (IGUAL AO TOPO DA IMAGEM) ---
st.html(f"""
    <div class="ticker-bar">
        <span class="ticker-item">📊 Real time Market data</span>
        <span class="ticker-item">🟢 IPCA+ <span class="ticker-green">+{m_data['ipca']:.2f}%</span></span>
        <span class="ticker-item">💵 USD/BRL <span class="ticker-green">R$ {m_data['dolar']:.2f}</span></span>
        <span class="ticker-item">🏢 FIIs (IFIX) <span class="ticker-green">+1.50%</span></span>
        <span class="ticker-item">🏦 CDI <span class="ticker-green">{m_data['cdi']:.2f}%</span></span>
        <span class="ticker-item">🏆 Gold <span class="ticker-red">R$ {m_data['ouro_g']:.2f}/g</span></span>
        <span class="ticker-item">🌎 S&P 500 <span class="ticker-green">+{m_data['sp500']:.2f}%</span></span>
    </div>
""")

# --- CABEÇALHO DO SISTEMA ---
st.title("⚡ Quantum Wealth System // Wealth Intelligence Engine")
st.caption("SISTEMA DE ANÁLISE MATRICIAL DE ATIVOS E PROJEÇÃO PATRIMONIAL")
st.markdown("<br>", unsafe_allowed_html=True)

# --- CONFIGURAÇÃO DA BARRA LATERAL (SIDEBAR TERMINAL) ---
with st.sidebar:
    st.markdown("### 🎛️ TERMINAL DE ENTRADA")
    st.markdown("---")
    v_inicial = st.number_input("Aporte Inicial Semente (R$)", min_value=0.0, value=30000.0, step=5000.0)
    aporte_mensal = st.number_input("Fluxo Mensal de Aporte (R$)", min_value=0.0, value=500.0, step=100.0)
    anos = st.slider("Horizonte Temporal (Anos)", min_value=1, max_value=40, value=15)
    taxa_alvo = st.number_input("Taxa Alvo Estratégica (% a.a.)", min_value=0.0, value=13.0, step=0.5)
    
    st.markdown("---")
    st.markdown("### 🛡️ RISK MANAGEMENT")
    perfil = st.selectbox("Perfil de Alocação", ["Conservador Defensivo", "Moderado Balanceado", "Agressivo Quantitativo"])
    custo_vida = st.number_input("Custo de Vida Alvo Atual (R$)", value=7000.0)

# --- SISTEMA DE ABAS DO MONITOR ---
aba_painel, aba_carteira, aba_stress, aba_roadmap = st.tabs([
    "📈 TERMINAL DE PROJEÇÃO", 
    "💼 MATRIX ASSET ALLOCATION", 
    "🚨 STRESS TEST CRITICAL SCENARIOS",
    "🗓️ ROADMAP METAS 2040"
])

# Lógica matemática de base para os gráficos e painéis
meses = anos * 12
r_meta = (1 + taxa_alvo/100)**(1/12) - 1
r_cdi = (1 + m_data['cdi']/100)**(1/12) - 1

data_points = []
s_meta, s_cdi = v_inicial, v_inicial
c_proprio = v_inicial

for m in range(1, meses + 1):
    if m > 1:
        c_proprio += aporte_mensal
        s_meta = (s_meta + aporte_mensal) * (1 + r_meta)
        s_cdi = (s_cdi + aporte_mensal) * (1 + r_cdi)
    else:
        s_meta *= (1 + r_meta)
        s_cdi *= (1 + r_cdi)
        
    data_points.append({
        "Ano": round(m / 12, 2),
        "Apenas Aportes": c_proprio,
        "Quantum Algo": s_meta,
        "Benchmark CDI": s_cdi
    })
    
df_projeccao = pd.DataFrame(data_points)
res_final = df_projeccao.iloc[-1]

# ==========================================
# ABA 1: TERMINAL DE PROJEÇÃO (GRID DA IMAGEM)
# ==========================================
with aba_painel:
    
    # Grid Principal: Bloco superior dividido em Simulador e Alocação
    grid_superior_esq, grid_superior_dir = st.columns([1, 1])
    
    with grid_superior_esq:
        with st.container():
            st.markdown("#### ⚙️ Compound Interest Simulator")
            # Apresentação Limpa estilo HUD
            c1, c2 = st.columns(2)
            c1.markdown(f"**Initial Investment:**<br><span style='font-size:1.3rem; color:#00E676; font-weight:bold;'>R$ {v_inicial:,.2f}</span>", unsafe_allowed_html=True)
            c2.markdown(f"**Duration:**<br><span style='font-size:1.3rem; color:#ffffff; font-weight:bold;'>{anos} Anos</span>", unsafe_allowed_html=True)
            
            st.markdown("<br>", unsafe_allowed_html=True)
            c3, c4 = st.columns(2)
            c3.markdown(f"**Monthly Contribution:**<br><span style='font-size:1.3rem; color:#ffffff; font-weight:bold;'>R$ {aporte_mensal:,.2f}</span>", unsafe_allowed_html=True)
            c4.markdown(f"**Target Yield (% a.a.):**<br><span style='font-size:1.3rem; color:#00B0FF; font-weight:bold;'>{taxa_alvo}%</span>", unsafe_allowed_html=True)

    with grid_superior_dir:
        with st.container():
            st.markdown("#### 📊 Portfolio Allocation Matrix")
            col_tab, col_graph = st.columns([1.2, 1])
            
            with col_tab:
                # Simulando a tabela compacta do mockup
                st.html("""
                    <table style='width:100%; border-collapse: collapse; font-size:0.85rem;'>
                        <tr style='border-bottom: 1px solid #334155; text-align:left; color:#94a3b8;'><th>Asset</th><th>Current</th><th>Target</th></tr>
                        <tr style='border-bottom: 1px solid #1e293b;'><td><b>IPCA+</b></td><td>35%</td><td>30%</td></tr>
                        <tr style='border-bottom: 1px solid #1e293b;'><td><b>FIIs</b></td><td>25%</td><td>20%</td></tr>
                        <tr style='border-bottom: 1px solid #1e293b;'><td><b>Nacionais Ações</b></td><td>20%</td><td>30%</td></tr>
                        <tr style='border-bottom: 1px solid #1e293b;'><td><b>International</b></td><td>20%</td><td>20%</td></tr>
                    </table>
                """)
            with col_graph:
                fig_mini_pie = px.pie(
                    values=[35, 25, 20, 20], 
                    names=["IPCA+", "FIIs", "Ações", "Inter"],
                    hole=0.6,
                    color_discrete_sequence=["#22c55e", "#3b82f6", "#a855f7", "#f97316"]
                )
                fig_mini_pie.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_mini_pie, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<br>", unsafe_allowed_html=True)

    # Bloco Inferior: Monitores Macroeconômicos na esquerda e Gráfico estendido na direita
    col_macro, col_timeline = st.columns([1, 2.2])
    
    with col_macro:
        with st.container():
            st.markdown("🌐 **Dollar Comercial (USD/BRL)**")
            st.markdown(f"<span style='font-size: 2.2rem; font-weight: 700; color: #00E676;'>R$ {m_data['dolar']:.3f}</span>", unsafe_allowed_html=True)
            st.markdown("<span style='color: #64748b; font-size:0.8rem;'>USD / BRL FX RATE</span>", unsafe_allowed_html=True)
            
        st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allowed_html=True)
        
        with st.container():
            st.markdown("🏆 **Gold (GC=F per gram)**")
            st.markdown(f"<span style='font-size: 2.2rem; font-weight: 700; color: #00E676;'>R$ {m_data['ouro_g']:.2f}</span>", unsafe_allowed_html=True)
            st.markdown("<span style='color: #64748b; font-size:0.8rem;'>GC=F REAL TIME PER GRAM</span>", unsafe_allowed_html=True)
            
        st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allowed_html=True)
        
        with st.container():
            st.markdown("🏦 **CDI Atual**")
            st.markdown(f"<span style='font-size: 2.2rem; font-weight: 700; color: #38bdf8;'>{m_data['cdi']:.2f}% a.a.</span>", unsafe_allowed_html=True)
            st.markdown("<span style='color: #64748b; font-size:0.8rem;'>REF: TAXA SELIC MATRIZ</span>", unsafe_allowed_html=True)

    with col_timeline:
        with st.container():
            st.markdown("#### 📊 Portfolio Performance Timeline")
            
            fig_neon = go.Figure()
            fig_neon.add_trace(go.Scatter(
                x=df_projeccao['Ano'], y=df_projeccao['Quantum Algo'], 
                name='Quantum Algo', line=dict(color='#00E676', width=3.5)
            ))
            fig_neon.add_trace(go.Scatter(
                x=df_projeccao['Ano'], y=df_projeccao['Benchmark CDI'], 
                name='Benchmark CDI', line=dict(color='#38bdf8', width=2, dash='dash')
            ))
            fig_neon.add_trace(go.Scatter(
                x=df_projeccao['Ano'], y=df_projeccao['Apenas Aportes'], 
                name='Apenas Aportes', line=dict(color='#ef4444', width=1.5)
            ))
            
            fig_neon.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(gridcolor='#1e293b', title="ANOS DE EVOLUÇÃO"),
                yaxis=dict(gridcolor='#1e293b', title="PATRIMÔNIO (R$)"),
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_neon, use_container_width=True)

# ==========================================
# ABAS ADICIONAIS RECONFIGURADAS E LEGÍVEIS
# ==========================================
with aba_carteira:
    st.subheader("💼 Engenharia Estratégica de Alocação")
    with st.container():
        st.markdown("Gerencie os pesos ativos do algoritmo de inteligência.")
        # Editor de dados com cores agora 100% visíveis
        df_edit = pd.DataFrame([
            {"Classe Ativo": "IPCA+", "Alocação (%)": 30.0},
            {"Classe Ativo": "FIIs", "Alocação (%)": 20.0},
            {"Classe Ativo": "Ações Nacionais", "Alocação (%)": 30.0},
            {"Classe Ativo": "Ativos Internacionais", "Alocação (%)": 20.0}
        ])
        st.data_editor(df_edit, use_container_width=True)

with aba_stress:
    st.subheader("🚨 Painel de Simulação de Crises Críticas")
    with st.container():
        st.markdown(f"**Patrimônio Alvo Projetado:** R$ {res_final['Quantum Algo']:,.2f}")
        st.markdown("---")
        st.markdown("📉 **Cenário de Estresse (Crash de Renda Variável - Estilo 2008):**")
        st.markdown(f"<h3 style='color:#ef4444;'>R$ {res_final['Quantum Algo']*0.75:,.2f} (-25%)</h3>", unsafe_allowed_html=True)

with aba_roadmap:
    st.subheader("🗓️ Planejamento de Metas de Longo Prazo")
    with st.container():
        v_meta1 = 100000.0
        t_meta1 = df_projeccao[df_projeccao["Quantum Algo"] >= v_meta1]["Ano"].min()
        st.markdown(f"🎯 **Meta Inicial (R$ 100k):** Estimada em **{t_meta1:.1f} anos** com a estratégia Quantum Algo.")
