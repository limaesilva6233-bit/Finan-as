import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf

# 1. Configuração da página em modo estendido e tema escuro nativo
st.set_page_config(page_title="QUANTUM | Wealth OS", layout="wide", page_icon="⚡")

# 2. Injeção do Layout Dark Premium com a imagem de fundo translúcida
BACKGROUND_IMAGE_URL = "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=1200&auto=format&fit=crop"

st.html(f"""
    <style>
        /* Fundo escuro absoluto do dashboard */
        .stApp {{
            background-color: #06090e !important;
            color: #f0f6fc !important;
            font-family: 'Inter', sans-serif;
        }}
        
        /* Imagem de fundo com opacidade controlada para efeito HUD */
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-image: url('{BACKGROUND_IMAGE_URL}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            opacity: 0.08; /* Deixa o fundo bem sutil e elegante */
            z-index: -1;
            pointer-events: none;
        }}
        
        /* Estilização dos containers para parecerem cartões de vidro fosco (Glassmorphism) */
        div[data-testid="stContainer"] {{
            background: rgba(13, 17, 23, 0.7) !important;
            border: 1px solid rgba(48, 54, 61, 0.6) !important;
            border-radius: 8px !important;
            padding: 15px !important;
        }}
        
        /* Cores customizadas para os títulos e métricas (Estilo Neon) */
        h1, h2, h3, h4 {{
            color: #ffffff !important;
            font-weight: 700 !important;
        }}
        
        /* Destaque para os valores das métricas principais */
        div[data-testid="stMetricValue"] {{
            font-size: 2rem !important;
            font-weight: bold !important;
        }}
    </style>
""")

# --- ENGINE DE BUSCA DE DADOS (YFINANCE) ---
@st.cache_data(ttl=1800)
def fetch_financial_metrics():
    market_data = {"dolar": 5.15, "ouro_oz": 2350.0, "ouro_g_brl": 390.0, "cdi": 10.50, "sp500_ytd": 8.5}
    try:
        df_usd = yf.Ticker("BRL=X").history(period="1d")
        if not df_usd.empty: 
            market_data["dolar"] = df_usd['Close'].iloc[-1]
            
        df_gold = yf.Ticker("GC=F").history(period="1d")
        if not df_gold.empty:
            market_data["ouro_oz"] = df_gold['Close'].iloc[-1]
            market_data["ouro_g_brl"] = (market_data["ouro_oz"] * market_data["dolar"]) / 31.1035
            
        df_sp = yf.Ticker("^GSPC").history(period="ytd")
        if len(df_sp) > 1:
            market_data["sp500_ytd"] = ((df_sp['Close'].iloc[-1] / df_sp['Close'].iloc[0]) - 1) * 100
    except Exception:
        pass
    return market_data

market = fetch_financial_metrics()

# --- CABEÇALHO SUPERIOR ---
col_logo, col_status = st.columns([4, 1])
with col_logo:
    st.title("⚡ QUANTUM // WEALTH INTELLIGENCE ENGINE")
    st.caption("SISTEMA DE ANÁLISE MATRICIAL DE ATIVOS E PROJEÇÃO PATRIMONIAL")
with col_status:
    st.write("") 
    st.success("🟢 ENGINE: ONLINE")

st.markdown("---")

# --- SIDEBAR DE PARÂMETROS ---
with st.sidebar:
    st.markdown("### 🎛️ TERMINAL DE ENTRADA")
    st.markdown("---")
    v_inicial = st.number_input("Aporte Inicial Semente (R$)", min_value=0.0, value=30000.0, step=5000.0)
    aporte_mensal = st.number_input("Fluxo Mensal de Aporte (R$)", min_value=0.0, value=500.0, step=100.0)
    anos = st.slider("Horizonte Temporal (Anos)", min_value=1, max_value=40, value=15)
    taxa_alvo = st.number_input("Taxa Alvo Estratégica (% a.a.)", min_value=0.0, value=13.0, step=0.5)
    
    st.markdown("---")
    st.markdown("### 🛡️ RISK MANAGEMENT")
    perfil = st.selectbox("Perfil de Alocação Algorítmica", ["Conservador Defensivo", "Moderado Balanceado", "Agressivo Quantitativo"])
    custo_vida = st.number_input("Custo de Vida Alvo Atual (R$)", value=7000.0)

# --- ABAS DO DASHBOARD ---
aba_painel, aba_carteira, aba_stress, aba_roadmap = st.tabs([
    "📈 TERMINAL DE PROJEÇÃO", 
    "💼 MATRIX ASSET ALLOCATION", 
    "🚨 STRESS TEST CRITICAL SCENARIOS",
    "🗓️ ROADMAP METAS 2040"
])

# ==========================================
# ABA 1: TERMINAL DE PROJEÇÃO (IGUAL À IMAGEM)
# ==========================================
with aba_painel:
    
    # Divisão em duas colunas principais como no modelo enviado
    col_esquerda, col_direita = st.columns([1, 2])
    
    with col_esquerda:
        st.markdown("#### 🌐 MACRO DATA MONITOR")
        
        with st.container(border=True):
            st.metric("💵 Dólar Comercial (USD/BRL)", f"R$ {market['dolar']:.2f}", "FX REAL TIME")
            
        st.write("")
        with st.container(border=True):
            st.metric("🏆 Gold (GC=F per gram)", f"R$ {market['ouro_g_brl']:.2f}", f"US$ {market['ouro_oz']:.1f} /oz")
            
        st.write("")
        with st.container(border=True):
            st.metric("🏦 CDI Atual", f"{market['cdi']:.2f}% a.a.", "REF: SELIC")
            
        st.write("")
        with st.container(border=True):
            st.metric("🌎 S&P 500 YTD", f"{market['sp500_ytd']:.2f}%", "GLOBAL INDEX")

    with col_direita:
        st.markdown("#### 📊 PERFORMANCE TIMELINE")
        
        # Processamento dos Juros Compostos
        meses = anos * 12
        r_meta = (1 + taxa_alvo/100)**(1/12) - 1
        r_cdi = (1 + market['cdi']/100)**(1/12) - 1
        
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
        
        # Gráfico Otimizado de Alta Performance (Visual Neon Identificado na Imagem)
        fig_neon = go.Figure()
        
        fig_neon.add_trace(go.Scatter(
            x=df_projeccao['Ano'], y=df_projeccao['Quantum Algo'], 
            name='Quantum Algo', line=dict(color='#00E676', width=4)
        ))
        fig_neon.add_trace(go.Scatter(
            x=df_projeccao['Ano'], y=df_projeccao['Benchmark CDI'], 
            name='Benchmark CDI', line=dict(color='#00B0FF', width=2.5, dash='dot')
        ))
        fig_neon.add_trace(go.Scatter(
            x=df_projeccao['Ano'], y=df_projeccao['Apenas Aportes'], 
            name='Apenas Aportes', line=dict(color='#FF5252', width=1.5)
        ))
        
        fig_neon.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(title="ANOS DE EVOLUÇÃO", gridcolor='#161b22', showgrid=True),
            yaxis=dict(title="PATRIMÔNIO ACUMULADO (R$)", gridcolor='#161b22', showgrid=True),
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        with st.container(border=True):
            st.plotly_chart(fig_neon, use_container_width=True)

# ==========================================
# ABA 2: MATRIX ASSET ALLOCATION
# ==========================================
with aba_carteira:
    st.subheader("💼 Engenharia de Alocação de Ativos")
    
    if 'carteira_dinamica' not in st.session_state:
        st.session_state.carteira_dinamica = pd.DataFrame([
            {"Classe Ativo": "IPCA+", "Alocação (%)": 35.0, "Volatilidade": "Baixa"},
            {"Classe Ativo": "FIIs", "Alocação (%)": 25.0, "Volatilidade": "Média"},
            {"Classe Ativo": "Ações Nacionais", "Alocação (%)": 20.0, "Volatilidade": "Alta"},
            {"Classe Ativo": "Ouro (Hedging)", "Alocação (%)": 10.0, "Volatilidade": "Baixa"},
            {"Classe Ativo": "Ativos Internacionais", "Alocação (%)": 10.0, "Volatilidade": "Média"}
        ])
        
    c_grid, c_pizza = st.columns([3, 2])
    
    with c_grid:
        st.markdown("#### Tabela de Pesos Estratégicos")
        carteira_user = st.data_editor(st.session_state.carteira_dinamica, num_rows="dynamic", use_container_width=True)
        st.session_state.carteira_dinamica = carteira_user
        
        soma_meta = carteira_user["Alocação (%)"].sum() if "Alocação (%)" in carteira_user.columns else 0
        if soma_meta == 100:
            st.success("🎯 MATRIX INTEGRADA: BALANCEAMENTO EQUILIBRADO (100%)")
        else:
            st.warning(f"❌ CONFLITO: Soma atual em {soma_meta:.1f}%. Ajuste para fechar em 100%.")
            
    with c_pizza:
        st.markdown("#### Escopo Visual da Carteira")
        fig_rosca = px.pie(carteira_user, values="Alocação (%)", names="Classe Ativo", hole=0.5, template="plotly_dark")
        fig_rosca.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_rosca, use_container_width=True)

# ==========================================
# ABA 3: STRESS TEST CRITICAL SCENARIOS
# ==========================================
with aba_stress:
    st.subheader("🚨 Simulação de Choque de Mercado")
    crise = st.radio(
        "Selecione o Evento Histórico:",
        ["Subprime Crash 2008 (-35% na Renda Variável)", "Pandemia Coronavírus 2020 (-25% geral)"]
    )
    patrimonio_bruto = res_final["Quantum Algo"]
    
    with st.container(border=True):
        if "2008" in crise:
            st.metric("Patrimônio Pós-Crise", f"R$ {patrimonio_bruto * 0.78:,.2f}", f"-22% de Impacto")
        else:
            st.metric("Patrimônio Pós-Crise", f"R$ {patrimonio_bruto * 0.88:,.2f}", f"-12% de Impacto")

# ==========================================
# ABA 4: ROADMAP METAS 2040
# ==========================================
with aba_roadmap:
    st.subheader("🗓️ Planejamento Temporal Estruturado")
    v_casamento = st.number_input("Meta 1: Casamento / Celebração (R$)", value=50000.0)
    v_imovel = st.number_input("Meta 2: Imóvel Próprio (R$)", value=250000.0)
    
    t_casamento = df_projeccao[df_projeccao["Quantum Algo"] >= v_casamento]["Ano"].min()
    t_imovel = df_projeccao[df_projeccao["Quantum Algo"] >= v_imovel]["Ano"].min()
    
    st.info(f"🔹 **Meta Casamento:** Atingível em aproximadamente **{t_casamento:.1f} Anos**.")
    st.info(f"🔹 **Meta Imóvel:** Atingível em aproximadamente **{t_imovel:.1f} Anos**.")

st.markdown("---")
st.caption("QUANTUM MATRIX WEALTH SYSTEM // INTERFACE PROFISSIONAL DE ALTA PERFORMANCE.")
