import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import google.generativeai as genai
import json
import re

# --- 1. 頁面基本配置 ---
st.set_page_config(
    page_title="AI 投資小秘書 - ETF 定期定額顧問",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. 安全讀取 API Key (Streamlit Cloud Secrets) ---
# 本地測試時，請在專案目錄下建立 .streamlit/secrets.toml 並寫入 GEMINI_API_KEY = "你的KEY"
# 部署到雲端後，請在 Streamlit 控制台的 Secrets 設定中貼入相同的內容
if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    GEMINI_API_KEY = "這裡放你的_GEMINI_API_KEY"

# --- 3. 核心功能函式 ---

def get_ai_allocation(age, risk_level, goal_desc):
    """透過 Gemini AI 取得精準配比"""
    if GEMINI_API_KEY == "這裡放你的_GEMINI_API_KEY":
        return {"0050.TW": 0.4, "0056.TW": 0.2, "VT": 0.2, "BND": 0.2}, "請設定 API Key 以啟用 AI 分析，目前顯示為預設模板。"

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        身為資深投資顧問，請為以下用戶配置 0050.TW, 0056.TW, VT, BND 四檔標的的投資比例：
        - 年齡: {age}
        - 風險偏好: {risk_level}/10 (1最保守, 10最積極)
        - 用戶目標: {goal_desc}
        
        請嚴格依照 JSON 格式回傳（權重總和必須為 1.0），不要回傳任何額外解釋文字。
        回傳範例：{{ "weights": {{"0050.TW": 0.4, "0056.TW": 0.2, "VT": 0.2, "BND": 0.2}}, "reason": "分析原因..." }}
        """
        response = model.generate_content(prompt)
        # 清洗 AI 回傳的 Markdown 代碼塊
        clean_text = re.sub(r'```json|```', '', response.text).strip()
        result = json.loads(clean_text)
        return result['weights'], result['reason']
    except Exception as e:
        return {"0050.TW": 0.4, "0056.TW": 0.2, "VT": 0.2, "BND": 0.2}, f"AI 分析發生錯誤，改用平衡配置。({str(e)})"

@st.cache_data(ttl=86400)
def fetch_data(tickers):
    """抓取歷史數據並計算月報酬率"""
    data = yf.download(tickers, period="10y", interval="1mo")['Adj Close']
    return data.pct_change().dropna()

def run_simulation(weights, monthly_amt, years, returns_df):
    """執行複利模擬"""
    w_series = pd.Series(weights)
    portfolio_return = (returns_df * w_series).sum(axis=1)
    
    avg_ret = portfolio_return.mean()
    std_ret = portfolio_return.std()
    
    balance = 0
    history = []
    months = years * 12
    
    for i in range(months):
        # 考慮波動性的模擬 (Monte Carlo 簡化版)
        current_ret = np.random.normal(avg_ret, std_ret)
        balance = (balance + monthly_amt) * (1 + current_ret)
        history.append(balance)
    
    return history, avg_ret * 12

# --- 4. 側邊欄 (使用者輸入) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2850/2850343.png", width=80)
    st.title("AI 參數設定")
    st.divider()
    
    u_age = st.slider("您的年齡", 18, 80, 25)
    u_risk = st.select_slider("風險承受度 (1-10)", options=list(range(1, 11)), value=7)
    u_monthly = st.number_input("每月預計投入 (TWD)", min_value=3000, value=10000, step=1000)
    u_goal = st.text_area("投資目標描述", "我想在 20 年後存到退休金，並享有穩定的被動收入。")
    
    st.divider()
    btn_start = st.button("🚀 生成個人化投資組合", use_container_width=True, type="primary")

# --- 5. 主內容顯示 ---
st.title("💰 AI 投資小秘書")
st.markdown("##### 定期定額 ETF 智能配置與複利模擬工具")

if not btn_start and 'init' not in st.session_state:
    st.info("請在左側面板填寫資訊，AI 將為您即時計算最適合的資產配置。")
    st.image("https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&q=80&w=1200", caption="長期投資是累積財富的最佳路徑")
else:
    st.session_state['init'] = True
    with st.spinner('AI 正在抓取市場數據並生成分析報告...'):
        # 1. AI 計算配置
        weights, reason = get_ai_allocation(u_age, u_risk, u_goal)
        # 2. 抓取歷史數據
        hist_returns = fetch_data(list(weights.keys()))
        # 3. 執行 20 年模擬
        sim_history, annual_ret = run_simulation(weights, u_monthly, 20, hist_returns)

    # 分頁設計
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
            st.subheader("🤖 AI 顧問分析建議")
            st.success(reason)
            st.write("---")
            for ticker, w in weights.items():
                st.write(f"**{ticker}**：`{w*100:.1f}%`")

    with tab2:
        st.subheader("20 年投資資產成長模擬")
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(y=sim_history, mode='lines', name='預估資產', 
                                     line=dict(color='#00FFAA', width=3)))
        fig_line.update_layout(template="plotly_dark", xaxis_title="月份", yaxis_title="金額 (TWD)",
                             hovermode="x unified", height=450)
        st.plotly_chart(fig_line, use_container_width=True)
        
        # 指標卡
        m1, m2, m3 = st.columns(3)
        final_val = sim_history[-1]
        total_cost = u_monthly * 12 * 20
        m1.metric("20年總投入成本", f"${total_cost:,.0f}")
        m2.metric("20年後預估資產", f"${final_val:,.0f}", delta=f"獲利 {((final_val/total_cost)-1)*100:.1f}%")
        m3.metric("組合歷史模擬年化", f"{annual_ret*100:.2f}%")

    with tab3:
        st.markdown("""
        ### 配置標的小檔案
        | 標的代码 | 名稱 | 核心屬性 |
        |---|---|---|
        | **0050.TW** | 元大台灣50 | 追蹤台灣前50大市值公司，具備高度成長性。 |
        | **0056.TW** | 元大高股息 | 選取高配息公司，提供穩定現金流，抗震性佳。 |
        | **VT** | Vanguard Total World | 投資全球股票市場，分散單一國家風險。 |
        | **BND** | Vanguard Total Bond | 美國全市場債券，資產保護傘，降低整體波動。 |
        """)

st.divider()
st.caption("免責聲明：本工具生成之建議僅供參考，不構成任何投資邀約。投資涉及風險，歷史績效不保證未來獲利。")
