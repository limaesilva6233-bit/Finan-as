import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf

# Configuração da página e interface ampla (Design nativo limpo)
st.set_page_config(page_title="QUANTUM | Wealth OS", layout="wide", page_icon="⚡")

# --- CABEÇALHO PURO SEM HTML ---
col_logo, col_status = st.columns([4, 1])
with col_logo:
    st.title("⚡ QUANTUM // WEALTH INTELLIGENCE ENGINE")
    st.text("SISTEMA DE ANÁLISE MATRICIAL DE ATIVOS E PROJEÇÃO PATRIMONIAL")
with col_status:
    st.write("")  # Espaçador nativo seguro
    st.success("🟢 CORE ENGINE: ONLINE")

# --- ENGINE DE DADOS (YFINANCE) ---
@st.cache_data(ttl=1800)
def fetch_financial_metrics():
    market_data = {"dolar": 5.15, "ouro_oz": 2350.0, "ouro_g_brl": 390.0, "cdi": 10.50, "sp500_ytd": 8.5}
    try:
        # Dólar
        df_usd = yf.Ticker("BRL=X").history(period="1d")
        if not df_usd.empty: 
            market_data["dolar"] = df_usd['Close'].iloc[-1]
        # Ouro
        df_gold = yf.Ticker("GC=F").history(period="1d")
        if not df_gold.empty:
            market_data["ouro_oz"] = df_gold['Close'].iloc[-1]
            market_data["ouro_g_brl"] = (market_data["ouro_oz"] * market_data["dolar"]) / 31.1035
        # S&P 500
        df_sp = yf.Ticker("^GSPC").history(period="ytd")
        if len(df_sp) > 1:
            market_data["sp500_ytd"] = ((df_sp['Close'].iloc[-1] / df_sp['Close'].iloc[0]) - 1) * 100
    except Exception:
        pass
    return market_data

market = fetch_financial_metrics()

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.markdown("### 🎛️ TERMINAL DE ENTRADA")
    st.markdown("---")
    v_inicial = st.number_input("Aporte Inicial Semente (R$)", min_value=0.0, value=15000.0, step=1000.0)
    aporte_mensal = st.number_input("Fluxo Mensal de Aporte (R$)", min_value=0.0, value=2000.0, step=100.0)
    anos = st.slider("Horizonte Temporal (Anos)", min_value=1, max_value=40, value=15)
    taxa_alvo = st.number_input("Taxa Alvo Estratégica (% a.a.)", min_value=0.0, value=13.0, step=0.5)
    
    st.markdown("---")
    st.markdown("### 🛡️ RISK MANAGEMENT")
    perfil = st.selectbox("Perfil de Alocação Algorítmica", ["Conservador Defensivo", "Moderado Balanceado", "Agressivo Quantitativo"])
    custo_vida = st.number_input("Custo de Vida Alvo Atual (R$)", value=7000.0)

# --- ABAS DE OPERAÇÃO ---
aba_painel, aba_carteira, aba_stress, aba_roadmap = st.tabs([
    "📈 TERMINAL DE PROJEÇÃO", 
    "💼 MATRIX ASSET ALLOCATION", 
    "🚨 STRESS TEST CRITICAL SCENARIOS",
    "🗓️ ROADMAP METAS 2040"
])

# ==========================================
# ABA 1: TERMINAL DE PROJEÇÃO
# ==========================================
with aba_painel:
    st.markdown("#### 🌐 MACRO DATA MONITOR")
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        with st.container(border=True):
            st.metric("💵 USD / BRL", f"R$ {market['dolar']:.2f}", "FX REAL TIME")
    with k2:
        with st.container(border=True):
            st.metric("🏆 GOLD (GRAMA)", f"R$ {market['ouro_g_brl']:.2f}", f"US$ {market['ouro_oz']:.1f} /oz")
    with k3:
        with st.container(border=True):
            st.metric("🏦 CDI ESTIMADO", f"{market['cdi']:.2f}% a.a.", "REF: SELIC")
    with k4:
        with st.container(border=True):
            st.metric("🌎 S&P 500 YTD", f"{market['sp500_ytd']:.2f}%", "GLOBAL INDEX")

    st.markdown("---")
    
    # Processamento Matricial de Juros
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
            "Capital Próprio": c_proprio,
            "Modelo Alvo": s_meta,
            "Cenário CDI": s_cdi
        })
        
    df_projeccao = pd.DataFrame(data_points)
    res_final = df_projeccao.iloc[-1]
    
    st.markdown("#### 🎯 RESULTADO ESTIMADO DO MODELO")
    r1, r2, r3 = st.columns(3)
    with r1:
        with st.container(border=True):
            st.metric("Capital Próprio Investido", f"R$ {res_final['Capital Próprio']:,.2f}")
    with r2:
        with st.container(border=True):
            st.metric("Montante na Sua Estratégia", f"R$ {res_final['Modelo Alvo']:,.2f}")
    with r3:
        with st.container(border=True):
            st.metric("Resultado Simulado em CDI", f"R$ {res_final['Cenário CDI']:,.2f}")
            
    st.write("")
    st.markdown("### 📈 Evolução Patrimonial Comparativa")
    fig_neon = go.Figure()
    fig_neon.add_trace(go.Scatter(x=df_projeccao['Ano'], y=df_projeccao['Modelo Alvo'], name='QUANTUM ALGO', line=dict(color='#00E676', width=3.5)))
    fig_neon.add_trace(go.Scatter(x=df_projeccao['Ano'], y=df_projeccao['Cenário CDI'], name='BENCHMARK CDI', line=dict(color='#00B0FF', width=2, dash='dot')))
    fig_neon.add_trace(go.Scatter(x=df_projeccao['Ano'], y=df_projeccao['Capital Próprio'], name='CAPITAL SECO', line=dict(color='#757575', width=1.5)))
    
    fig_neon.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title="ANOS DE ACUMULAÇÃO", gridcolor='#21262D'),
        yaxis=dict(title="VALOR ACUMULADO (R$)", gridcolor='#21262D'),
        hovermode="x unified"
    )
    st.plotly_chart(fig_neon, use_container_width=True)

# ==========================================
# ABA 2: MATRIX ASSET ALLOCATION
# ==========================================
with aba_carteira:
    st.subheader("💼 Engenharia de Alocação de Ativos")
    
    if 'carteira_dinamica' not in st.session_state:
        st.session_state.carteira_dinamica = pd.DataFrame([
            {"Classe Ativo": "Renda Fixa IPCA+", "Alocação (%)": 35.0, "Volatilidade Corrente": "Baixa"},
            {"Classe Ativo": "FIIs de Tijolo", "Alocação (%)": 25.0, "Volatilidade Corrente": "Média"},
            {"Classe Ativo": "Ações Nacionais", "Alocação (%)": 20.0, "Volatilidade Corrente": "Alta"},
            {"Classe Ativo": "Ouro (Hedging)", "Alocação (%)": 10.0, "Volatilidade Corrente": "Baixa"},
            {"Classe Ativo": "Ativos Internacionais (Dólar)", "Alocação (%)": 10.0, "Volatilidade Corrente": "Média"}
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
            st.warning(f"❌ CONFLITO DE VETOR: Soma atual em {soma_meta:.1f}%. Ajuste para fechar em 100%.")
            
    with c_pizza:
        st.markdown("#### Escopo Visual da Carteira")
        fig_rosca = px.pie(carteira_user, values="Alocação (%)", names="Classe Ativo", hole=0.5, template="plotly_dark")
        fig_rosca.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_rosca, use_container_width=True)

    st.markdown("---")
    st.markdown("### ⚡ Ordem de Compra Mensal Otimizada")
    valor_aporte_rebalancear = st.number_input("Aporte Disponível Imediato (R$)", value=3000.0)
    
    if soma_meta == 100 and valor_aporte_rebalancear > 0:
        df_ordens = carteira_user.copy()
        df_ordens["Boleta de Compra"] = (df_ordens["Alocação (%)"] / 100) * valor_aporte_rebalancear
        df_ordens["Boleta de Compra"] = df_ordens["Boleta de Compra"].map("R$ {:,.2f}".format)
        st.dataframe(df_ordens[["Classe Ativo", "Alocação (%)", "Boleta de Compra"]], use_container_width=True)

# ==========================================
# ABA 3: STRESS TEST CRITICAL SCENARIOS
# ==========================================
with aba_stress:
    st.subheader("🚨 Simulação de Choque de Mercado (Stress Testing)")
    st.write("Avalie o comportamento simulado do seu patrimônio final estimado se uma grande crise histórica ocorresse imediatamente no término da sua meta:")
    
    crise = st.radio(
        "Selecione o Evento Macroeconômico Histórico para Choque:",
        ["Subprime Crash 2008 (-35% na Renda Variável, +40% no Ouro)", 
         "Pandemia Coronavírus 2020 (-25% geral, Dólar +15%)", 
         "Cenário de Estagflação Severa (Retorno Real reduzido a zero por 3 anos)"]
    )
    
    patrimonio_bruto = res_final["Modelo Alvo"]
    
    st.markdown("---")
    st.markdown("#### Relatório de Danos e Impacto em Painel")
    
    sd1, sd2 = st.columns(2)
    
    if "2008" in crise:
        p_impactado = patrimonio_bruto * 0.78  
        with sd1: 
            with st.container(border=True):
                st.metric("Patrimônio Pós-Crise", f"R$ {p_impactado:,.2f}", f"-R$ {patrimonio_bruto - p_impactado:,.2f}")
        with sd2: st.error("⚠️ DIAGNÓSTICO: Alta exposição a ações causaria perda patrimonial temporária de ~22%. Suas posições em Ouro atuariam como colchão térmico limitando a queda.")
    elif "2020" in crise:
        p_impactado = patrimonio_bruto * 0.88
        with sd1: 
            with st.container(border=True):
                st.metric("Patrimônio Pós-Crise", f"R$ {p_impactado:,.2f}", f"-R$ {patrimonio_bruto - p_impactado:,.2f}")
        with sd2: st.warning("⚠️ DIAGNÓSTICO: Queda rápida de liquidez geral. Recuperação estimada em V (menos de 10 meses). Aporte mensal continuado durante esse período geraria assimetria positiva brutal.")
    else:
        p_impactado = patrimonio_bruto - (aporte_mensal * 36)
        with sd1: 
            with st.container(border=True):
                st.metric("Patrimônio Pós-Crise", f"R$ {p_impactado:,.2f}", "ESTAGNAÇÃO")
        with sd2: st.info("⚠️ DIAGNÓSTICO: Ausência de ganho real. O poder de compra é severamente corroído se a carteira não possuir ativos atrelados diretamente ao IPCA físico.")

# ==========================================
# ABA 4: ROADMAP METAS 2040
# ==========================================
with aba_roadmap:
    st.subheader("🗓️ Planejamento Temporal Estruturado (Alvos de Vida)")
    st.write("Cronograma automatizado calculando o tempo exato para atingir seus grandes marcos de investimento:")
    
    v_casamento = st.number_input("Meta Orçamentária 1: Casamento / Celebração (R$)", value=50000.0)
    v_imovel = st.number_input("Meta Orçamentária 2: Entrada Forte / Imóvel Próprio (R$)", value=250000.0)
    v_independencia = (custo_vida * 12) / 0.04  
    
    st.markdown("---")
    st.markdown("### 🗺️ Linha do Tempo de Conquistas Calculadas")
    
    t_casamento = df_projeccao[df_projeccao["Modelo Alvo"] >= v_casamento]["Ano"].min()
    t_imovel = df_projeccao[df_projeccao["Modelo Alvo"] >= v_imovel]["Ano"].min()
    t_indep = df_projeccao[df_projeccao["Modelo Alvo"] >= v_independencia]["Ano"].min()
    
    def formata_tempo(t):
        return f"{t:.1f} Anos" if not np.isnan(t) else "Acima do horizonte atual"

    st.info(f"🔹 **Alvo 1 (Casamento - R$ {v_casamento:,.2f}):** Atingível em aproximadamente **{formata_tempo(t_casamento)}**.")
    st.info(f"🔹 **Alvo 2 (Imóvel - R$ {v_imovel:,.2f}):** Atingível em aproximadamente **{formata_tempo(t_imovel)}**.")
    st.success(f"🏁 **Alvo Master (Viver de Renda Eterna - R$ {v_independencia:,.2f}):** Atingível em **{formata_tempo(t_indep)}** gerando uma retirada de R$ {custo_vida:,.2f}/mês.")
    
    # Gráfico de barras horizontais das metas
    fig_metas = go.Figure(go.Bar(
        x=[v_casamento, v_imovel, v_independencia],
        y=['Casamento', 'Imóvel', 'Independência'],
        orientation='h',
        marker_color=['#00B0FF', '#FF9100', '#00E676']
    ))
    fig_metas.update_layout(
        template="plotly_dark", 
        title="Volume Financeiro por Meta Destinada", 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_metas, use_container_width=True)

st.markdown("---")
st.text("QUANTUM MATRIX WEALTH SYSTEM // DESENVOLVIDO PARA ANÁLISE PREDITIVA DE ALTA PERFORMANCE.")
