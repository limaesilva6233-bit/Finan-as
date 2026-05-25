import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime

# Configuração da página em modo Wide para melhor aproveitamento gráfico
st.set_page_config(page_title="Planner Investments Pro", layout="wide", page_icon="💰")

st.title("💸 Planner Investments Pro — Simulador & Carteira Inteligente")
st.write("Monitore ativos em tempo real, simule a evolução do seu patrimônio a longo prazo e gerencie o balanceamento da sua carteira.")

# --- FUNÇÃO PARA PEGAR DADOS EM TEMPO REAL ---
@st.cache_data(ttl=3600)  # Guarda em cache por 1 hora para o app ficar rápido
def buscar_dados_mercado():
    dados = {"dolar": 5.15, "ouro_oz": 2350.0, "ouro_g_brl": 390.0, "cdi": 10.50}
    try:
        # Dólar Comercial (USD/BRL)
        ticker_usd = yf.Ticker("BRL=X")
        df_usd = ticker_usd.history(period="1d")
        if not df_usd.empty:
            dados["dolar"] = df_usd['Close'].iloc[-1]
        
        # Ouro em Onça Troy (USD)
        ticker_gold = yf.Ticker("GC=F")
        df_gold = ticker_gold.history(period="1d")
        if not df_gold.empty:
            dados["ouro_oz"] = df_gold['Close'].iloc[-1]
            
        # Cálculo aproximado do grama do ouro em R$ (1 Oz ≈ 31.1035g)
        dados["ouro_g_brl"] = (dados["ouro_oz"] * dados["dolar"]) / 31.1035
    except Exception as e:
        st.sidebar.warning(f"Erro ao atualizar cotações em tempo real: {e}. Usando dados padrão.")
    return dados

info_mercado = buscar_dados_mercado()

# --- SIDEBAR GLOBAL (PARÂMETROS DA SIMULAÇÃO) ---
with st.sidebar:
    st.header("⚙️ Parâmetros Globais")
    st.markdown("Ajuste as variáveis para simular o seu planejamento financeiro de longo prazo:")
    
    v_inicial = st.number_input("Aplicação Inicial (R$):", min_value=0.0, value=10000.0, step=1000.0)
    aporte_mensal = st.number_input("Aporte Mensal Constante (R$):", min_value=0.0, value=1500.0, step=100.0)
    anos = st.number_input("Tempo de Investimento (Anos):", min_value=1, max_value=50, value=15, step=1)
    taxa_anual_estimada = st.number_input("Sua Taxa Rendimento Alvo (% ao ano):", min_value=0.0, value=12.0, step=0.5)
    
    st.markdown("---")
    st.markdown("💡 *Dica: Use taxas reais se quiser descontar a inflação mentalmente, ou configure o simulador de IPCA na Aba 3.*")

# --- CRIAÇÃO DAS ABAS ---
aba1, aba2, aba3 = st.tabs(["📈 Simulador Avançado & Comparativo", "💼 Gestor de Carteira & Rebalanceamento", "🧠 Inteligência Financeira & IPCA"])

# ==========================================
# TAB 1: SIMULADOR AVANÇADO & COMPARATIVO
# ==========================================
with aba1:
    st.subheader("📊 Painel Macroeconômico & Projeções")
    
    # Cards de Mercado em Tempo Real
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("💵 Dólar Comercial", f"R$ {info_mercado['dolar']:.2f}")
    m2.metric("🏆 Ouro (Grama)", f"R$ {info_mercado['ouro_g_brl']:.2f}", f"US$ {info_mercado['ouro_oz']:.1f}/oz")
    m3.metric("🏦 Taxa CDI Padrão", f"{info_mercado['cdi']:.2f}% a.a.")
    m4.metric("🎯 Sua Meta de Retorno", f"{taxa_anual_estimada:.2f}% a.a.")

    st.markdown("---")
    
    # Motor de Cálculo de Juros Compostos Mês a Mês
    meses = anos * 12
    taxa_mensal_meta = (1 + taxa_anual_estimada/100)**(1/12) - 1
    taxa_mensal_cdi = (1 + (info_mercado['cdi']/100))**(1/12) - 1
    taxa_mensal_poupanca = (1 + 0.06)**(1/12) - 1 # Poupança estimada em ~6% a.a.
    
    ev_mes = []
    tot_investido = v_inicial
    
    # Valores iniciais
    saldo_meta, saldo_cdi, saldo_poup = v_inicial, v_inicial, v_inicial
    
    for mes in range(1, meses + 1):
        if mes > 1:
            tot_investido += aporte_mensal
            saldo_meta = (saldo_meta + aporte_mensal) * (1 + taxa_mensal_meta)
            saldo_cdi = (saldo_cdi + aporte_mensal) * (1 + taxa_mensal_cdi)
            saldo_poup = (saldo_poup + aporte_mensal) * (1 + taxa_mensal_poupanca)
        else:
            saldo_meta *= (1 + taxa_mensal_meta)
            saldo_cdi *= (1 + taxa_mensal_cdi)
            saldo_poup *= (1 + taxa_mensal_poupanca)
            
        ev_mes.append({
            "Mês": mes,
            "Ano": round(mes / 12, 1),
            "Total Investido": tot_investido,
            "Sua Estratégia": saldo_meta,
            "100% do CDI": saldo_cdi,
            "Poupança": saldo_poup
        })
        
    df_evolucao = pd.DataFrame(ev_mes)
    df_final = df_evolucao.iloc[-1]
    
    # Resumo de Resultados em Cards Grandes
    st.markdown("#### 🎯 Resultado Estimado ao Final do Período")
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("💰 Capital Próprio Investido", f"R$ {df_final['Total Investido']:,.2f}")
    r2.metric("🚀 Montante na Sua Estratégia", f"R$ {df_final['Sua Estratégia']:,.2f}", f"+R$ {df_final['Sua Estratégia'] - df_final['Total Investido']:,.2f} em juros")
    r3.metric("🥈 Rendendo 100% CDI", f"R$ {df_final['100% do CDI']:,.2f}")
    r4.metric("🥉 Se ficasse na Poupança", f"R$ {df_final['Poupança']:,.2f}")

    # Gráfico de Linha Interativo com Plotly
    st.markdown("### 📈 Evolução Patrimonial Comparativa ao Longo do Tempo")
    fig_linha = go.Figure()
    fig_linha.add_trace(go.Scatter(x=df_evolucao['Ano'], y=df_evolucao['Sua Estratégia'], name='Sua Estratégia', line=dict(color='#2ECC71', width=3)))
    fig_linha.add_trace(go.Scatter(x=df_evolucao['Ano'], y=df_evolucao['100% do CDI'], name='100% do CDI', line=dict(color='#3498DB', width=2, dash='dash')))
    fig_linha.add_trace(go.Scatter(x=df_evolucao['Ano'], y=df_evolucao['Poupança'], name='Poupança Tradicional', line=dict(color='#E74C3C', width=1.5)))
    fig_linha.add_trace(go.Scatter(x=df_evolucao['Ano'], y=df_evolucao['Total Investido'], name='Apenas Aportes (Sem Juros)', line=dict(color='#95A5A6', width=2)))
    
    fig_linha.update_layout(
        xaxis_title="Tempo de Acumulação (Anos)",
        yaxis_title="Valor Acumulado (R$)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_linha, use_container_width=True)

# ==========================================
# TAB 2: GESTOR DE CARTEIRA & REBALANCEAMENTO
# ==========================================
with aba2:
    st.subheader("💼 Montagem e Balanceamento de Carteira Customizada")
    st.write("Monte a distribuição ideal dos seus investimentos e calcule para onde direcionar novos aportes.")
    
    # Inicialização do estado da carteira base padrão
    if 'carteira_ativos' not in st.session_state:
        st.session_state.carteira_ativos = pd.DataFrame([
            {"Ativo/Classe": "Renda Fixa Pós-Fixada", "Meta (%)": 40.0, "Rendimento Esperado (% a.a.)": 10.5},
            {"Ativo/Classe": "Fundos Imobiliários (FIIs)", "Meta (%)": 30.0, "Rendimento Esperado (% a.a.)": 11.5},
            {"Ativo/Classe": "Ações e ETFs Globais", "Meta (%)": 20.0, "Rendimento Esperado (% a.a.)": 14.0},
            {"Ativo/Classe": "Ouro e Proteções", "Meta (%)": 10.0, "Rendimento Esperado (% a.a.)": 8.0}
        ])

    col_carteira, col_graf_pizza = st.columns([3, 2])
    
    with col_carteira:
        st.markdown("#### 🛠️ Ajuste seus Ativos e Metas Percentuais")
        st.info("Você pode clicar diretamente na tabela abaixo para alterar os nomes, adicionar linhas ou mudar as porcentagens:")
        
        # O Editor de Dados permite que o usuário adicione e remova linhas dinamicamente na tela
        carteira_editada = st.data_editor(
            st.session_state.carteira_ativos, 
            num_rows="dynamic",
            use_container_width=True,
            key="editor_carteira"
        )
        st.session_state.carteira_ativos = carteira_editada

        total_porcentagem = carteira_editada["Meta (%)"].sum() if "Meta (%)" in carteira_editada.columns else 0
        
        if total_porcentagem == 100.0:
            st.success(f"✅ Distribuição Perfeita! Total Alocado: {total_porcentagem:.1f}%")
        else:
            st.danger(f"⚠️ Atenção: A soma das metas está em **{total_porcentagem:.1f}%**. Reajuste os valores para fechar exatamente em **100%**.")

    with col_graf_pizza:
        st.markdown("#### 🍰 Divisão Visual da sua Carteira")
        if total_porcentagem > 0:
            fig_pizza = px.pie(
                carteira_editada, 
                values="Meta (%)", 
                names="Ativo/Classe", 
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_pizza.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.1))
            st.plotly_chart(fig_pizza, use_container_width=True)
        else:
            st.write("Insira ativos na tabela para gerar o gráfico.")

    st.markdown("---")
    st.markdown("### 🧮 Calculadora de Aportes Direcionados")
    st.write("Digite o valor que você tem disponível para investir *hoje*. O sistema distribuirá o dinheiro seguindo estritamente as suas metas percentuais:")
    
    v_aporte_hoje = st.number_input("Valor do Aporte Mensal de Hoje (R$):", min_value=0.0, value=2000.0, step=500.0)
    
    if total_porcentagem == 100.0 and v_aporte_hoje > 0:
        df_aportes = carteira_editada.copy()
        df_aportes["Quanto aplicar hoje (R$)"] = (df_aportes["Meta (%)"] / 100) * v_aporte_hoje
        
        # Formatação cosmética para exibição organizada
        df_exibicao = df_aportes.copy()
        df_exibicao["Meta (%)"] = df_exibicao["Meta (%)"].map("{:.1f}%".format)
        df_exibicao["Quanto aplicar hoje (R$)"] = df_exibicao["Quanto aplicar hoje (R$)"].map("R$ {:,.2f}".format)
        
        st.table(df_exibicao[["Ativo/Classe", "Meta (%)", "Quanto aplicar hoje (R$)"]])
    else:
        st.caption("Ajuste a tabela acima para totalizar 100% para liberar o cálculo de aportes.")

# ==========================================
# TAB 3: INTELIGÊNCIA FINANCEIRA & IPCA
# ==========================================
with aba3:
    st.subheader("🧠 Ferramentas Avançadas de Simulação Humana")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("#### 📉 Impacto Real da Inflação (IPCA)")
        st.write("O dinheiro perde valor no tempo. Insira a inflação média anual projetada para descobrir o poder de compra real do seu montante final:")
        
        inflacao_anual = st.number_input("Projeção de Inflação Média (% ao ano):", min_value=0.0, value=4.5, step=0.1)
        
        # Desconto do poder de compra real pela fórmula clássica: Montante / (1 + i)^n
        valor_nominal_final = df_final['Sua Estratégia']
        poder_compra_real = valor_nominal_final / ((1 + (inflacao_anual / 100)) ** anos)
        
        st.metric("💰 Poder de Compra Corrigido", f"R$ {poder_compra_real:,.2f}")
        st.info(f"Devido à inflação acumulada de {inflacao_anual}% a.a., os R$ {valor_nominal_final:,.2f} acumulados em {anos} anos equivalerão a R$ {poder_compra_real:,.2f} em dinheiro de hoje.")
        
    with c2:
        st.markdown("#### 🏝️ Calculadora de Independência (Regra dos 4%)")
        st.write("Quantos reais você precisaria ter investidos em uma carteira sólida para cobrir seus gastos para sempre e viver de renda passiva?")
        
        custo_vida_mensal = st.number_input("Custo de Vida Mensal Alvo (R$):", min_value=0.0, value=8000.0, step=500.0)
        
        # Regra clássica dos 4% (Gasto Anual / 0.04)
        patrimonio_necessario = (custo_vida_mensal * 12) / 0.04
        
        st.metric("🎯 Seu Número de Liberdade Financeira", f"R$ {patrimonio_necessario:,.2f}")
        st.success(f"Acumulando R$ {patrimonio_necessario:,.2f}, você pode retirar R$ {custo_vida_mensal:,.2f} todos os meses (corrigidos pela inflação), sem que o seu dinheiro acabe.")

# Rodapé de assinatura simples
st.markdown("---")
st.caption(f"Planner Investments Pro — Atualizado automaticamente via cotações públicas do Yahoo Finance em {datetime.now().strftime('%d/%m/%Y')}.")
