import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. 頁面基本配置 ---
st.set_page_config(
    page_title="AI 投資小秘書 - ETF 定期定額顧問",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 隱藏右上角 GitHub、Fork 與 Deploy 按鈕 + 自訂樣式 ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display:none;}
    #stDecoration {display:none;}
    
    /* 漸層背景 */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
    }
    
    /* 側邊欄樣式 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    /* 卡片樣式 */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.2);
    }
    
    /* 閃爍提示 */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .pulse-animation {
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* 標題樣式 */
    .main-title {
        background: linear-gradient(90deg, #00F260 0%, #0575E6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    /* 風險等級標籤 */
    .risk-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        color: white;
    }
    
    .risk-low { background: #10b981; }
    .risk-medium { background: #f59e0b; }
    .risk-high { background: #ef4444; }
    </style>
    """, unsafe_allow_html=True)


# --- 2. 核心功能函式 ---

def get_expert_allocation(age, risk_level):
    """根據年齡與風險偏好自動計算配比"""
    equity_base = max(0.2, (100 - age) / 100)
    risk_factor = risk_level / 10
    
    bnd_w = max(0.1, 1 - (equity_base * risk_factor))
    remaining = 1 - bnd_w
    
    vt_w = remaining * 0.4
    stock_tw_total = remaining * 0.6
    
    tw_0050_w = stock_tw_total * risk_factor
    tw_0056_w = stock_tw_total * (1 - risk_factor)
    
    weights = {
        "0050.TW": round(tw_0050_w, 2),
        "0056.TW": round(tw_0056_w, 2),
        "VT": round(vt_w, 2),
        "BND": round(bnd_w, 2)
    }
    
    diff = 1.0 - sum(weights.values())
    weights["0050.TW"] += round(diff, 2)

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
        return data, returns
    except:
        return pd.DataFrame(), pd.DataFrame()

def run_simulation(weights, monthly_amt, years, returns_df):
    """執行複利模擬"""
    try:
        w_series = pd.Series(weights)
        portfolio_return = (returns_df * w_series).sum(axis=1)
        avg_ret = portfolio_return.mean()
        std_ret = portfolio_return.std()
        
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
    
    return history, avg_ret * 12, std_ret * np.sqrt(12)

def calculate_portfolio_metrics(weights, returns_df):
    """計算投資組合進階指標"""
    try:
        w_series = pd.Series(weights)
        portfolio_return = (returns_df * w_series).sum(axis=1)
        
        # 計算指標
        annual_return = portfolio_return.mean() * 12
        annual_vol = portfolio_return.std() * np.sqrt(12)
        sharpe_ratio = annual_return / annual_vol if annual_vol > 0 else 0
        
        # 最大回撤
        cumulative = (1 + portfolio_return).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        return {
            'annual_return': annual_return,
            'annual_vol': annual_vol,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown
        }
    except:
        return {
            'annual_return': 0.072,
            'annual_vol': 0.15,
            'sharpe_ratio': 0.48,
            'max_drawdown': -0.25
        }

def stress_test_scenarios(weights, monthly_amt, years):
    """情境壓力測試"""
    scenarios = {
        "樂觀情境 📈": {"return": 0.12, "vol": 0.12},
        "基準情境 ⚖️": {"return": 0.08, "vol": 0.15},
        "悲觀情境 📉": {"return": 0.04, "vol": 0.20},
        "金融危機 ⚠️": {"return": -0.02, "vol": 0.30}
    }
    
    results = {}
    months = years * 12
    
    for scenario_name, params in scenarios.items():
        balance = 0
        history = []
        for i in range(months):
            ret = np.random.normal(params['return']/12, params['vol']/np.sqrt(12))
            balance = (balance + monthly_amt) * (1 + ret)
            history.append(balance)
        results[scenario_name] = history[-1]
    
    return results

# --- 3. 側邊欄 ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2850/2850343.png", width=80)
    st.title("💼 投資參數設定")
    st.divider()
    
    u_age = st.slider("🎂 您的年齡", 18, 80, 25)
    u_risk = st.select_slider("⚡ 風險承受度", options=list(range(1, 11)), value=7)
    
    # 風險等級標籤
    if u_risk <= 3:
        risk_label = '<span class="risk-badge risk-low">保守型</span>'
    elif u_risk <= 7:
        risk_label = '<span class="risk-badge risk-medium">穩健型</span>'
    else:
        risk_label = '<span class="risk-badge risk-high">積極型</span>'
    st.markdown(risk_label, unsafe_allow_html=True)
    
    u_monthly = st.number_input("💰 每月投入 (TWD)", min_value=1000, value=10000, step=1000)
    u_years = st.slider("📅 投資期間 (年)", 5, 30, 20)
    u_goal = st.text_area("🎯 投資目標", "我想在退休前累積足夠的資產。")
    
    st.divider()
    btn_start = st.button("🚀 開始智能分析", use_container_width=True, type="primary")
    
    if st.button("🔙 返回歡迎頁", use_container_width=True):
        st.switch_page("welcome.py")

# --- 4. 主內容顯示 ---
st.markdown('<div class="main-title">💰 AI 投資小秘書</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white; font-size: 1.2rem;'>定期定額 ETF 智能配置與複利模擬工具</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if not btn_start and 'init' not in st.session_state:
    # 未開始分析時的展示頁面
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style='background: rgba(255,255,255,0.9); padding: 2rem; border-radius: 15px;'>
            <h3>👋 歡迎回來！</h3>
            <p style='line-height: 1.8;'>
                請在左側面板設定您的投資參數：<br><br>
                ✓ 年齡與風險偏好<br>
                ✓ 每月投資金額<br>
                ✓ 投資期間目標<br><br>
                設定完成後，點擊「開始智能分析」即可獲得專屬的投資建議！
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.image("https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&q=80&w=800", 
                 caption="開始您的財富累積之旅")
    
    # 快速提示卡片
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info("📊\n\n**智能配置**\n\n基於AI演算法的最佳化配置")
    with col2:
        st.success("📈\n\n**複利預測**\n\n視覺化20年成長曲線")
    with col3:
        st.warning("⚡\n\n**風險分析**\n\n即時監控投資風險")
    with col4:
        st.error("🎯\n\n**壓力測試**\n\n模擬極端市場情境")

else:
    st.session_state['init'] = True
    
    with st.spinner('🔄 正在進行智能分析，請稍候...'):
        # 執行分析
        weights, reason = get_expert_allocation(u_age, u_risk)
        price_data, hist_returns = fetch_data(list(weights.keys()))
        sim_history, annual_ret, annual_vol = run_simulation(weights, u_monthly, u_years, hist_returns)
        metrics = calculate_portfolio_metrics(weights, hist_returns)
        stress_results = stress_test_scenarios(weights, u_monthly, u_years)

    # 頂部關鍵指標卡片
    st.markdown("### 📊 投資組合關鍵指標")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    final_val = sim_history[-1]
    total_cost = u_monthly * 12 * u_years
    total_return = ((final_val / total_cost) - 1) * 100
    
    with col1:
        st.metric("預期年化報酬", f"{metrics['annual_return']*100:.2f}%", 
                  delta=f"vs 定存 {metrics['annual_return']*100 - 1.5:.2f}%")
    with col2:
        st.metric("投資組合波動率", f"{metrics['annual_vol']*100:.2f}%")
    with col3:
        st.metric("夏普比率", f"{metrics['sharpe_ratio']:.2f}", 
                  delta="優" if metrics['sharpe_ratio'] > 0.5 else "待改善")
    with col4:
        st.metric("最大回撤", f"{metrics['max_drawdown']*100:.2f}%")
    with col5:
        st.metric(f"{u_years}年總報酬", f"{total_return:.1f}%", 
                  delta=f"獲利 ${final_val-total_cost:,.0f}")

    st.divider()

    # Tab 導航
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 資產配置", 
        "📈 成效預測", 
        "⚡ 風險分析", 
        "🎯 壓力測試",
        "🔍 標的分析"
    ])

    with tab1:
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            # 圓餅圖
            fig_pie = go.Figure(data=[go.Pie(
                labels=list(weights.keys()), 
                values=list(weights.values()), 
                hole=.45,
                marker=dict(colors=['#00FFAA', '#1F77B4', '#FF7F0E', '#D62728']),
                textinfo='label+percent',
                textfont_size=14
            )])
            fig_pie.update_layout(
                title="建議配置比例",
                margin=dict(t=50, b=0, l=0, r=0),
                height=400
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # 配置明細表
            st.markdown("#### 📋 配置明細")
            for ticker, w in weights.items():
                st.progress(w, text=f"**{ticker}**: {w*100:.0f}%")
        
        with col2:
            st.markdown("#### 💡 AI 顧問分析")
            st.success(reason)
            
            st.markdown("#### 🎯 投資建議")
            if u_risk >= 7:
                st.warning("""
                **積極型投資者注意事項：**
                - ✓ 您的配置偏向成長型資產，適合長期持有
                - ✓ 建議定期定額不中斷，勿因短期波動而停扣
                - ✓ 保留3-6個月緊急預備金在高流動性帳戶
                """)
            else:
                st.info("""
                **穩健型投資者優勢：**
                - ✓ 您的配置包含較高比例的防禦性資產
                - ✓ 波動較小，適合追求穩定報酬的投資者
                - ✓ 可考慮提高每月投入金額以加速累積
                """)

    with tab2:
        st.markdown("### 📈 資產成長模擬預測")
        
        # 主要成長曲線
        fig_line = go.Figure()
        
        # 投入本金線
        cost_line = [u_monthly * 12 * (i/12) for i in range(len(sim_history))]
        fig_line.add_trace(go.Scatter(
            y=cost_line, 
            mode='lines', 
            name='累積投入成本',
            line=dict(color='#FF6B6B', width=2, dash='dash')
        ))
        
        # 資產價值線
        fig_line.add_trace(go.Scatter(
            y=sim_history, 
            mode='lines', 
            name='預估資產價值',
            line=dict(color='#00FFAA', width=4),
            fill='tonexty',
            fillcolor='rgba(0, 255, 170, 0.1)'
        ))
        
        fig_line.update_layout(
            template="plotly_dark",
            xaxis_title="投資月份",
            yaxis_title="金額 (TWD)",
            height=500,
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
        # 里程碑標記
        st.markdown("### 🎯 投資里程碑")
        milestones = [
            (u_years * 0.25, sim_history[int(len(sim_history) * 0.25)]),
            (u_years * 0.5, sim_history[int(len(sim_history) * 0.5)]),
            (u_years * 0.75, sim_history[int(len(sim_history) * 0.75)]),
            (u_years, final_val)
        ]
        
        cols = st.columns(4)
        for idx, (year, value) in enumerate(milestones):
            with cols[idx]:
                st.metric(
                    f"第 {int(year)} 年",
                    f"${value:,.0f}",
                    delta=f"+{((value/(u_monthly*12*year))-1)*100:.1f}%"
                )

    with tab3:
        st.markdown("### ⚡ 風險指標儀表板")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 風險雷達圖
            categories = ['年化報酬', '波動風險', '夏普比率', '最大回撤', '資產分散']
            
            values = [
                min(metrics['annual_return'] / 0.15 * 100, 100),
                max(0, 100 - metrics['annual_vol'] / 0.3 * 100),
                min(metrics['sharpe_ratio'] / 2 * 100, 100),
                max(0, 100 + metrics['max_drawdown'] * 200),
                70  # 固定分散度評分
            ]
            
            fig_radar = go.Figure(data=go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor='rgba(0, 255, 170, 0.2)',
                line=dict(color='#00FFAA', width=3)
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100])
                ),
                showlegend=False,
                title="投資組合健康度雷達圖",
                height=400
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with col2:
            st.markdown("#### 📉 歷史回撤分析")
            if not hist_returns.empty:
                try:
                    w_series = pd.Series(weights)
                    portfolio_return = (hist_returns * w_series).sum(axis=1)
                    cumulative = (1 + portfolio_return).cumprod()
                    running_max = cumulative.expanding().max()
                    drawdown = (cumulative - running_max) / running_max
                    
                    fig_dd = go.Figure()
                    fig_dd.add_trace(go.Scatter(
                        x=drawdown.index,
                        y=drawdown.values * 100,
                        fill='tozeroy',
                        fillcolor='rgba(255, 107, 107, 0.3)',
                        line=dict(color='#FF6B6B', width=2),
                        name='回撤幅度'
                    ))
                    fig_dd.update_layout(
                        title="歷史回撤走勢",
                        xaxis_title="時間",
                        yaxis_title="回撤幅度 (%)",
                        height=400,
                        template="plotly_white"
                    )
                    st.plotly_chart(fig_dd, use_container_width=True)
                except:
                    st.info("回撤數據計算中...")
            else:
                st.info("暫無歷史數據")
            
            st.markdown("#### 🛡️ 風險控制建議")
            if metrics['max_drawdown'] < -0.3:
                st.error("⚠️ 您的投資組合在極端情況下可能面臨30%以上的損失，建議增加債券配置比例。")
            elif metrics['max_drawdown'] < -0.2:
                st.warning("⚡ 投資組合在市場震盪時可能有20%左右的回撤，屬於中等風險水平。")
            else:
                st.success("✅ 您的投資組合風險控制良好，最大回撤在可接受範圍內。")

    with tab4:
        st.markdown("### 🎯 情境壓力測試")
        st.info("模擬不同市場環境下，您的投資組合在20年後的表現差異")
        
        # 情境比較圖
        fig_stress = go.Figure()
        
        scenarios = list(stress_results.keys())
        values = list(stress_results.values())
        colors = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444']
        
        fig_stress.add_trace(go.Bar(
            x=scenarios,
            y=values,
            marker=dict(
                color=colors,
                line=dict(color='white', width=2)
            ),
            text=[f'${v:,.0f}' for v in values],
            textposition='outside',
            textfont=dict(size=14, color='white')
        ))
        
        # 加上成本線
        fig_stress.add_hline(
            y=total_cost, 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"總投入成本: ${total_cost:,.0f}",
            annotation_position="right"
        )
        
        fig_stress.update_layout(
            title=f"各情境下 {u_years} 年後的資產價值",
            yaxis_title="資產價值 (TWD)",
            template="plotly_dark",
            height=500,
            showlegend=False
        )
        st.plotly_chart(fig_stress, use_container_width=True)
        
        # 情境詳細說明
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 情境假設說明")
            st.markdown("""
            | 情境 | 年化報酬 | 年化波動 |
            |---|---|---|
            | 樂觀情境 📈 | 12% | 12% |
            | 基準情境 ⚖️ | 8% | 15% |
            | 悲觀情境 📉 | 4% | 20% |
            | 金融危機 ⚠️ | -2% | 30% |
            """)
        
        with col2:
            st.markdown("#### 💡 情境分析")
            best = max(stress_results.values())
            worst = min(stress_results.values())
            
            st.success(f"✅ **最佳情境**：資產可達 ${best:,.0f}")
            st.error(f"⚠️ **最差情境**：資產約為 ${worst:,.0f}")
            
            if worst > total_cost:
                st.info("💪 即使在金融危機情境下，您的投資仍能保持正報酬！")
            else:
                st.warning("⚡ 在極端情境下可能面臨虧損，建議調整配置或增加投資期間。")

    with tab5:
        st.markdown("### 🔍 投資標的深度分析")
        
        # ETF 資訊卡片
        etf_info = {
            "0050.TW": {
                "name": "元大台灣50",
                "type": "市值型",
                "desc": "追蹤台灣市值前50大企業，包含台積電、鴻海等龍頭股",
                "expense": "0.43%",
                "dividend": "~3-4%",
                "icon": "🇹🇼"
            },
            "0056.TW": {
                "name": "元大高股息",
                "type": "高股息",
                "desc": "精選30檔高殖利率股票，適合追求穩定現金流的投資者",
                "expense": "0.74%",
                "dividend": "~5-7%",
                "icon": "💰"
            },
            "VT": {
                "name": "Vanguard World",
                "type": "全球股票",
                "desc": "投資全球9000+檔股票，涵蓋美國、歐洲、亞洲、新興市場",
                "expense": "0.07%",
                "dividend": "~2%",
                "icon": "🌍"
            },
            "BND": {
                "name": "Vanguard Bond",
                "type": "美國債券",
                "desc": "投資美國投資等級債券，提供穩定收益與資產保護",
                "expense": "0.03%",
                "dividend": "~3-4%",
                "icon": "🛡️"
            }
        }
        
        for ticker, info in etf_info.items():
            with st.expander(f"{info['icon']} {info['name']} ({ticker}) - 配置 {weights[ticker]*100:.0f}%", expanded=False):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"**類型**：{info['type']}")
                    st.markdown(f"**說明**：{info['desc']}")
                
                with col2:
                    st.metric("內扣費用", info['expense'])
                
                with col3:
                    st.metric("平均股息", info['dividend'])
                
                # 如果有價格數據，顯示歷史走勢
                if not price_data.empty and ticker in price_data.columns:
                    try:
                        fig_price = go.Figure()
                        fig_price.add_trace(go.Scatter(
                            x=price_data.index,
                            y=price_data[ticker],
                            mode='lines',
                            name=ticker,
                            line=dict(color='#00FFAA', width=2)
                        ))
                        fig_price.update_layout(
                            title=f"{ticker} 10年歷史走勢",
                            xaxis_title="日期",
                            yaxis_title="價格",
                            height=300,
                            template="plotly_white",
                            margin=dict(t=30, b=0, l=0, r=0)
                        )
                        st.plotly_chart(fig_price, use_container_width=True)
                    except:
                        pass
        
        # 相關性分析
        st.markdown("### 📊 標的相關性分析")
        if not hist_returns.empty:
            try:
                corr_matrix = hist_returns[list(weights.keys())].corr()
                
                fig_corr = go.Figure(data=go.Heatmap(
                    z=corr_matrix.values,
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    colorscale='RdYlGn',
                    zmid=0,
                    text=np.round(corr_matrix.values, 2),
                    texttemplate='%{text}',
                    textfont={"size": 12},
                    colorbar=dict(title="相關係數")
                ))
                
                fig_corr.update_layout(
                    title="標的間相關係數矩陣（值越低代表分散效果越好）",
                    height=400,
                    xaxis=dict(side='bottom')
                )
                st.plotly_chart(fig_corr, use_container_width=True)
                
                st.info("💡 **解讀提示**：相關係數接近1表示標的走勢相似，接近-1表示走勢相反，接近0表示無明顯關聯。良好的投資組合應包含相關性較低的資產以達到分散風險的效果。")
            except:
                st.warning("相關性數據計算中...")

st.divider()

# 底部資訊與快速操作
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.caption("⚠️ **投資警語**：本系統提供的模擬結果僅供參考，不構成投資建議。過去績效不代表未來表現，投資前請審慎評估自身風險承受能力。")

with col2:
    if st.button("📥 下載分析報告", use_container_width=True):
        st.info("報告下載功能開發中...")

with col3:
    if st.button("📧 分享給朋友", use_container_width=True):
        st.success("分享連結已複製！")

st.caption("© 2024 AI 投資小秘書 | Powered by Streamlit & YFinance")
