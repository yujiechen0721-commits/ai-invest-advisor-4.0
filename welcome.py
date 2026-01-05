import streamlit as st
import time

# --- 1. 頁面基本配置 ---
st.set_page_config(
    page_title="AI 投資小秘書 - 歡迎",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS 樣式修正 (移除漸層、強化按鈕置中) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display:none;}
    #stDecoration {display:none;}
    
    /* 改為純色背景 (深色專業藍) */
    .stApp {
        background-color: #0f172a;
    }
    
    /* 標題區域 */
    .welcome-title {
        text-align: center;
        color: white;
        font-size: clamp(2.5rem, 5vw, 4rem);
        font-weight: 800;
        margin-top: 3rem;
        text-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    
    .welcome-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.3rem;
        margin-bottom: 4rem;
        letter-spacing: 1px;
    }
    
    /* 功能卡片樣式 */
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        height: 300px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .feature-card:hover {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid #38bdf8;
        transform: translateY(-5px);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.8rem;
    }
    
    .feature-desc {
        color: #94a3b8;
        text-align: center;
        line-height: 1.5;
        font-size: 0.9rem;
    }
    
    /* 統計方塊 */
    .stat-box {
        background: #1e293b;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* 強制按鈕置中樣式 */
    .stButton {
        display: flex;
        justify-content: center;
        width: 100%;
        margin-top: 4rem;
    }
    
    .stButton > button {
        background: #38bdf8 !important; /* 天藍色 */
        color: #0f172a !important;
        font-size: 1.8rem !important; /* 放大字體 */
        font-weight: 800 !important;
        padding: 1rem 5rem !important; /* 放大按鈕尺寸 */
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 14px 0 rgba(56, 189, 248, 0.39) !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background: #7dd3fc !important;
        transform: scale(1.05) !important;
        box-shadow: 0 6px 20px rgba(56, 189, 248, 0.5) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 頁面內容渲染 ---

st.markdown('<div class="welcome-title">🤖 AI 投資小秘書</div>', unsafe_allow_html=True)
st.markdown('<div class="welcome-subtitle">數據驅動配置 · 精準複利模擬</div>', unsafe_allow_html=True)

# 統計數據
s1, s2, s3, s4 = st.columns(4)
stats = [("10Y+", "歷史數據"), ("4大", "精選標的"), ("Smart", "自動配置"), ("20Y", "長線模擬")]
for col, (num, label) in zip([s1, s2, s3, s4], stats):
    with col:
        st.markdown(f'<div class="stat-box"><div style="font-size:1.6rem; font-weight:800; color:#38bdf8;">{num}</div><div style="font-size:0.8rem; color:#94a3b8;">{label}</div></div>', unsafe_allow_html=True)

st.write("---")

# 功能卡片矩陣
features = [
    {"icon": "📊", "title": "智能資產配置", "desc": "結合年齡與風險承受度，自動計算台股、全球股市與債券的最優比例。"},
    {"icon": "📈", "title": "複利成效預測", "desc": "運用歷史數據預測未來20年資產走勢，讓複利效應清晰可見。"},
    {"icon": "🎯", "title": "風險指標監控", "desc": "即時分析年化報酬、波動率與最大回撤，在獲利與風險間取得平衡。"},
    {"icon": "💡", "title": "策略調整建議", "desc": "依據人生階段提供動態再平衡建議，守護您的投資成果。"},
    {"icon": "🔍", "title": "標的深度解析", "desc": "0050、0056、VT、BND 深度拆解，理解每一塊錢的去向。"},
    {"icon": "⚡", "title": "情境壓力測試", "desc": "模擬歷史金融危機對組合的影響，評估資產的抗壓能力。"}
]

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

# --- 4. 操作區 (按鈕置中優化) ---
# 使用單一 column 或調整比例來確保置中
st.button("🚀 開 始 體 驗", use_container_width=False) # CSS 會接手置中

if st.session_state.get('clicked_button'): # 這裡可以連接跳轉邏輯
    pass 

# 為了與跳轉邏輯結合，建議這樣寫：
if st.session_state.get('button_sentinel'):
    st.balloons()
    time.sleep(1)
    st.switch_page("pages/main.py")

# 頁尾
st.markdown("""
    <div style='text-align: center; color: #64748b; padding-top: 5rem; padding-bottom: 2rem;'>
        <p style='font-size: 0.85rem;'>本工具僅供教學參考，投資必有風險，入市請謹慎評估。</p>
        <p style='font-size: 0.75rem;'>© 2026 AI Investment Assistant Team</p>
    </div>
""", unsafe_allow_html=True)
