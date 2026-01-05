import streamlit as st
import time

# --- 1. 頁面基本配置 ---
st.set_page_config(
    page_title="AI 投資小秘書 - 歡迎",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. 增強版 CSS 樣式 ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display:none;}
    #stDecoration {display:none;}
    
    /* 現代漸層背景 */
    .stApp {
        background: linear-gradient(160deg, #1a2a6c 0%, #b21f1f 50%, #fdbb2d 100%);
        background-attachment: fixed;
    }
    
    /* 標題區域優化 */
    .welcome-title {
        text-align: center;
        color: white;
        font-size: clamp(2.5rem, 5vw, 4rem); /* 自動適應螢幕 */
        font-weight: 800;
        margin-top: 3rem;
        letter-spacing: -1px;
        text-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    
    .welcome-subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.85);
        font-size: 1.2rem;
        margin-bottom: 4rem;
        letter-spacing: 2px;
    }
    
    /* 毛玻璃卡片優化 */
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 24px;
        padding: 2.5rem 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 320px; /* 固定高度確保對齊 */
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .feature-card:hover {
        transform: translateY(-12px) scale(1.02);
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 1.5rem;
        filter: drop-shadow(0 5px 15px rgba(0,0,0,0.2));
    }
    
    .feature-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
    }
    
    .feature-desc {
        color: rgba(255, 255, 255, 0.8);
        text-align: center;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    /* 數據統計方塊 */
    .stat-box {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 20px;
        padding: 1.2rem;
        text-align: center;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* 修正按鈕置中與樣式 */
    div.stButton {
        text-align: center;
        margin-top: 3rem;
    }
    
    .stButton > button {
        background: white !important;
        color: #b21f1f !important;
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        padding: 0.8rem 4rem !important;
        border-radius: 100px !important;
        border: none !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5) !important;
        background: #f8f8f8 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 頁面內容渲染 ---

# 主標題
st.markdown('<div class="welcome-title">🤖 AI 投資小秘書</div>', unsafe_allow_html=True)
st.markdown('<div class="welcome-subtitle">專業級資產配置 · 數據驅動成長</div>', unsafe_allow_html=True)

# 統計數據欄位 (減少留白)
s1, s2, s3, s4 = st.columns(4)
stats = [
    ("10Y+", "歷史數據"), ("4大", "精選標的"), 
    ("Smart", "AI配置"), ("20Y", "長線模擬")
]
for col, (num, label) in zip([s1, s2, s3, s4], stats):
    with col:
        st.markdown(f'<div class="stat-box"><div style="font-size:1.8rem; font-weight:800;">{num}</div><div style="font-size:0.8rem; opacity:0.8;">{label}</div></div>', unsafe_allow_html=True)

st.write("---")

# 功能矩陣 (優化卡片布局)
features = [
    {"icon": "📊", "title": "智能資產配置", "desc": "結合年齡與風險承受度，自動計算台股、全球股市與債券的最優比例。"},
    {"icon": "📈", "title": "複利成效預測", "desc": "運用蒙地卡羅模擬法預測未來20年資產走勢，讓複利效應清晰可見。"},
    {"icon": "🎯", "title": "風險指標監控", "desc": "即時分析年化報酬、波動率與最大回撤，在獲利與風險間取得平衡。"},
    {"icon": "💡", "title": "策略調整建議", "desc": "依據不同人生階段與市場情緒，提供動態再平衡建議，守護您的投資成果。"},
    {"icon": "🔍", "title": "標的深度解析", "desc": "0050、0056、VT、BND 深度拆解，理解每一塊錢的去向。"},
    {"icon": "⚡", "title": "情境壓力測試", "desc": "模擬歷史金融危機對組合的影響，確保您的資產在極端市場下依然穩健。"}
]

# 循環產生 2x3 的排列
for i in range(0, 6, 3):
    cols = st.columns(3)
    for j in range(3):
        f = features[i + j]
        with cols[j]:
            st.markdown(f"""
                <div class="feature-card">
                    <div class="feature-icon">{f['icon']}</div>
                    <div class="feature-title">{f['title']}</div>
                    <div class="feature-desc">{f['desc']}</div>
                </div>
            """, unsafe_allow_html=True)

# --- 4. 操作區 ---
st.write("")
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    if st.button("🚀 開 始 體 驗"):
        st.balloons()
        time.sleep(1)
        st.switch_page("pages/main.py")

# 頁尾
st.markdown("""
    <div style='text-align: center; color: rgba(255,255,255,0.6); padding-top: 5rem; padding-bottom: 2rem;'>
        <p style='font-size: 0.85rem;'>本工具僅供教學參考，投資必有風險，入市請謹慎評估。</p>
        <p style='font-size: 0.75rem;'>© 2026 AI Investment Assistant Team</p>
    </div>
""", unsafe_allow_html=True)
