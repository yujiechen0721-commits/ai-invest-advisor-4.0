import streamlit as st
import time

# --- 1. 頁面基本配置 ---
st.set_page_config(
    page_title="AI 投資小秘書 - 歡迎",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS 樣式修正 ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display:none;}
    #stDecoration {display:none;}
    
    .stApp {
        background-color: #0f172a;
    }
    
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
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem 1.5rem;
        margin-bottom: 1.5rem;
        height: 300px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .stat-box {
        background: #1e293b;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        color: white;
    }

    /* --- 強制按鈕與文字放大 --- */
    .stButton > button {
        background: #38bdf8 !important;
        color: #0f172a !important;
        font-size: 2.5rem !important; /* 再放大字體 */
        font-weight: 900 !important;
        height: 5rem !important;
        border-radius: 20px !important;
        border: none !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.5) !important;
        transition: 0.3s !important;
        width: 100% !important; /* 填滿容器 */
    }
    
    .stButton > button:hover {
        transform: scale(1.02) !important;
        background: #7dd3fc !important;
    }

    /* 針對按鈕文字的額外放大 */
    .stButton > button p {
        font-size: 2.5rem !important;
        font-weight: 900 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 頁面內容 ---
st.markdown('<div class="welcome-title">🤖 AI 投資小秘書</div>', unsafe_allow_html=True)
st.markdown('<div class="welcome-subtitle">數據驅動配置 · 精準複利模擬</div>', unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)
stats = [("10Y+", "歷史數據"), ("4大", "精選標的"), ("Smart", "自動配置"), ("20Y", "長線模擬")]
for col, (num, label) in zip([s1, s2, s3, s4], stats):
    with col:
        st.markdown(f'<div class="stat-box"><div style="font-size:1.6rem; font-weight:800; color:#38bdf8;">{num}</div><div style="font-size:0.8rem; color:#94a3b8;">{label}</div></div>', unsafe_allow_html=True)

st.write("---")

features = [
    {"icon": "📊", "title": "智能資產配置", "desc": "結合年齡與風險承受度，自動計算最優比例。"},
    {"icon": "📈", "title": "複利成效預測", "desc": "預測未來20年資產走勢，讓複利清晰可見。"},
    {"icon": "🎯", "title": "風險指標監控", "desc": "分析報酬與最大回撤，取得風險平衡。"},
    {"icon": "💡", "title": "策略調整建議", "desc": "提供動態再平衡建議，守護投資成果。"},
    {"icon": "🔍", "title": "標的深度解析", "desc": "0050、0056、VT、BND 深度拆解。"},
    {"icon": "⚡", "title": "情境壓力測試", "desc": "模擬金融危機，測試資產抗壓能力。"}
]

for i in range(0, 6, 3):
    cols = st.columns(3)
    for j in range(3):
        f = features[i + j]
        with cols[j]:
            st.markdown(f"""<div class="feature-card">
                <div style="font-size:3rem;">{f['icon']}</div>
                <div style="font-size:1.3rem; font-weight:700; color:white; margin:1rem;">{f['title']}</div>
                <div style="color:#94a3b8; text-align:center;">{f['desc']}</div>
            </div>""", unsafe_allow_html=True)

# --- 4. 操作區：使用三欄式布局並將按鈕置於中間 ---
st.markdown("<br><br>", unsafe_allow_html=True)
left, mid, right = st.columns([1, 2, 1]) # 中間寬度佔 2/4
with mid:
    # use_container_width=True 確保它填滿中間這 2/4 的寬度，達到視覺絕對置中
    if st.button("🚀 開 始 體 驗", use_container_width=True):
        st.balloons()
        time.sleep(0.5)
        st.switch_page("pages/main.py")

# 頁尾
st.markdown("""
    <div style='text-align: center; color: #64748b; padding-top: 5rem; padding-bottom: 2rem;'>
        <p style='font-size: 0.85rem;'>本工具僅供教學參考，投資必有風險，入市請謹慎評估。</p>
        <p style='font-size: 0.75rem;'>© 2026 AI Investment Assistant Team</p>
    </div>
""", unsafe_allow_html=True)
