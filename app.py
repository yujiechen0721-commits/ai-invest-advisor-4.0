import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
import re

# --- 1. 頁面基本配置 ---
st.set_page_config(
    page_title="AI 投資小秘書 - ETF 定期定額顧問",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. 核心功能函式 (專家邏輯取代 AI 串接) ---

def get_expert_allocation(age, risk_level):
    """
    根據『年齡』與『風險偏好』自動計算配比
    邏輯：年齡越大，BND(債券)比例越高；風險越高，0050與VT比例越高
    """
    # 基礎比例計算 (100 - 年齡 = 積極資產佔比)
    equity_base = max(0.2, (100 - age) / 100)
    
    # 根據風險等級 (1-10) 調整
    risk_factor = risk_level / 10
    
    # 計算各標的權重
    bnd_w = max(0.1, 1 - (equity_base * risk_factor))
    remaining = 1 - bnd_w
    
    # 將剩餘比例分配給股票型 ETF
    vt_w = remaining * 0.4
    stock_tw_total = remaining * 0.6
    
    # 台灣股票再拆分市值型與高股息
    # 風險越高，0050 越多；風險越低，0056 越多
    tw_0050_w = stock_tw_total * risk_factor
    tw_0056_w = stock_tw_total * (1 - risk_factor)
    
    weights = {
        "0050.TW": round(tw_0050_w, 2),
        "0056.TW": round(tw_0056_w, 2),
        "VT": round(vt_w, 2),
        "BND": round(bnd_w, 2)
    }
    
    # 確保總和為 1 (修正捨入誤差)
    diff = 1.0 - sum(weights.values())
    weights["0050.TW"] += round(diff, 2)

    # 產生顧問評論
    reason = f"根據您的年齡({age}歲)與風險承受度({risk_level}/10)，系統為您配置了 "
    reason += f"{weights['BND']*100:.0f}% 的防禦性資產與 {(1-weights['BND'])*100:.0f}% 的攻擊性資產。 "
    if risk_level >= 7:
        reason += "此配置著重於長期資本增值，適合能忍受短期波動並追求財富翻倍的您。"
    elif risk_level <= 4:
        reason += "此配置著重於資產保護與穩定配息，適合追求資產穩健成長的保守型投資者。"
    else:
        reason += "這是一個平衡型配置，兼顧了全球分散投資與台灣市場的成長性。"

    return weights, reason

@st.cache_data(ttl=86400)
def fetch_data(tickers):
    """抓取歷史數據"""
    try:
        data = yf.download(tickers, period="10y", interval="1mo")['Adj Close']
        returns = data.pct_change().dropna()
        return returns
    except:
        return pd.DataFrame()

def run_simulation(weights, monthly_amt, years, returns_df):
    """執行複利模擬 - 含波動率補償"""
    try:
        w_series = pd.Series(weights)
        portfolio_return = (returns_df * w_series).sum(axis=1)
        avg_ret = portfolio_return.mean()
        std_ret = portfolio_return.std()
        
        # 若無數據，預設年化 7.2%
        if np.isnan(avg_ret):
            avg_ret, std_ret = 0.006, 0.015
    except:
        avg_ret, std_ret = 0.006, 0.015

    balance = 0
    history = []
    months = years * 12
    
    for i in range(months):
        current_ret = np.random.normal(avg_ret, std_ret)
        balance = (balance + monthly_amt) * (1 + current_ret)
        history.append(balance)
    
    return history, avg_ret * 12

# --- 3. 側邊欄 ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2850/2850343.png", width=80)
    st.title("投資參數設定")
    st.divider()
    
    u_age = st.slider("您的年齡", 18, 80, 25)
    u_risk = st.select_slider("風險承受度 (1-10)", options=list(range(1, 11)), value=7)
    u_monthly = st.number_input("每月預計投入 (TWD)", min_value=1000, value=10000, step=1000)
    u_goal = st.text_area("投資目標描述", "我想在 20 年後存到退休金。")
    
    st.divider()
    btn_start = st.button("🚀 開始智能模擬", use_container_width=True, type="primary")

# --- 4. 主內容顯示 ---
st.title("💰 AI 投資小秘書")
st.markdown("##### 定期定額 ETF 智能配置與複利模擬工具")

if not btn_start and 'init' not in st.session_state:
    st.info("👋 歡迎！請在左側面板輸入您的資料，然後點擊「開始智能模擬」。")
    st.image("https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&q=80&w=1200", caption="長期投資是累積財富的最佳路徑")
else:
    st.session_state['init'] = True
    with st.spinner('正在分析數據中...'):
        # 1. 執行專家邏輯配置
        weights, reason = get_expert_allocation(u_age, u_risk)
        # 2. 獲取數據
        hist_returns = fetch_data(list(weights.keys()))
        # 3. 執行模擬
        sim_history, annual_ret = run_simulation(weights, u_monthly, 20, hist_returns)

    tab1, tab2, tab3 = st.tabs(["📊 資產配置", "📈 成效預測", "🔎 標的深度分析"])

    with tab1:
        c1, c2 = st.columns([1, 1.2])
        with c1:
            fig_pie = go.Figure(data=[go.Pie(labels=list(weights.keys()), 
                                            values=list(weights.values()), 
                                            hole=.4,
                                            marker=dict(colors=['#00FFAA', '#1F77B4', '#FF7F0E', '#D62728']))])
            fig_pie.update_layout(title="建議比例佔比", margin=dict(t=30, b=0, l=0, r=0))
            st.plotly_chart(fig_pie, use_container_width=True)
        with c2:
            st.subheader("💡 顧問分析建議")
            st.success(reason)
            st.write("---")
            for ticker, w in weights.items():
                st.write(f"**{ticker}**：`{w*100:.0f}%`")

    with tab2:
        st.subheader("20 年投資資產成長模擬")
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(y=sim_history, mode='lines', name='預估資產', line=dict(color='#00FFAA', width=3)))
        fig_line.update_layout(template="plotly_dark", xaxis_title="月份", yaxis_title="金額 (TWD)", height=450)
        st.plotly_chart(fig_line, use_container_width=True)
        
        m1, m2, m3 = st.columns(3)
        final_val = sim_history[-1]
        total_cost = u_monthly * 12 * 20
        m1.metric("20年總投入成本", f"${total_cost:,.0f}")
        m2.metric("20年後預估資產", f"${final_val:,.0f}", delta=f"獲利 {((final_val/total_cost)-1)*100:.1f}%")
        m3.metric("組合模擬年化率", f"{annual_ret*100:.2f}%")

    with tab3:
        st.markdown("""
        ### 配置標的小檔案
        | 標的代碼 | 名稱 | 核心屬性 |
        |---|---|---|
        | **0050.TW** | 元大台灣50 | 追蹤台灣市值前50大。 |
        | **0056.TW** | 元大高股息 | 鎖定高股息成分股。 |
        | **VT** | Vanguard World | 投資全球股票市場。 |
        | **BND** | Vanguard Bond | 全球債券避險。 |
        """)

st.divider()
st.caption("警語：數據模擬基於歷史表現，不保證未來獲利。投資前請自行評估風險。")
