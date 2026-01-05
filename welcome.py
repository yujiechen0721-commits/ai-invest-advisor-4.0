import streamlit as st
import time

# --- 頁面基本配置 ---
st.set_page_config(
    page_title="AI 投資小秘書 - 歡迎",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 隱藏預設元素與自訂樣式 ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display:none;}
    #stDecoration {display:none;}
    
    /* 漸層背景 */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* 標題動畫 */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .welcome-title {
        animation: fadeInDown 1s ease-out;
        text-align: center;
        color: white;
        font-size: 3.5rem;
        font-weight: bold;
        margin-top: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .welcome-subtitle {
        text-align: center;
        color: #E0E0E0;
        font-size: 1.3rem;
        margin-bottom: 3rem;
        animation: fadeInDown 1.2s ease-out;
    }
    
    /* 功能卡片 */
    .feature-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 12px 48px rgba(0,0,0,0.3);
    }
    
    .feature-icon {
        font-size: 4rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .feature-desc {
        color: #666;
        text-align: center;
        line-height: 1.6;
    }
    
    /* 按鈕樣式 */
    .stButton > button {
        background: linear-gradient(90deg, #00F260 0%, #0575E6 100%);
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        padding: 1rem 3rem;
        border-radius: 50px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 25px rgba(0,0,0,0.3);
    }
    
    /* 統計數字 */
    .stat-box {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        backdrop-filter: blur(10px);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 主標題區 ---
st.markdown('<div class="welcome-title">🤖 AI 投資小秘書</div>', unsafe_allow_html=True)
st.markdown('<div class="welcome-subtitle">智能配置 · 精準預測 · 穩健成長</div>', unsafe_allow_html=True)

# --- 統計數據展示 ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">10+</div>
        <div class="stat-label">年歷史數據</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">4</div>
        <div class="stat-label">精選 ETF</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">AI</div>
        <div class="stat-label">智能演算法</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">20年</div>
        <div class="stat-label">複利模擬</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 核心功能介紹 ---
st.markdown("<h2 style='text-align: center; color: white; margin: 3rem 0 2rem 0;'>✨ 核心功能</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">智能資產配置</div>
        <div class="feature-desc">
            根據您的年齡、風險偏好，AI自動計算最適配置比例，涵蓋台股、全球股市與債券市場。
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <div class="feature-title">複利成效預測</div>
        <div class="feature-desc">
            模擬20年定期定額投資，視覺化呈現資產成長曲線，預測最終資產與報酬率。
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">風險動態監控</div>
        <div class="feature-desc">
            即時計算投資組合波動率、最大回撤、夏普比率等專業指標，掌握風險狀況。
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💡</div>
        <div class="feature-title">專業顧問建議</div>
        <div class="feature-desc">
            依據市場數據與您的投資目標，提供個人化的投資策略與調整建議。
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">標的深度分析</div>
        <div class="feature-desc">
            詳細解析每個ETF的特性、歷史績效、費用率，讓您投資更有信心。
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">情境壓力測試</div>
        <div class="feature-desc">
            模擬金融危機、熊市等極端情況下的投資組合表現，評估抗壓能力。
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 進入按鈕 ---
st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 進入投資小秘書", use_container_width=True):
        st.session_state['entered'] = True
        st.balloons()
        time.sleep(0.5)
        st.switch_page("pages/main.py")

# --- 底部資訊 ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: rgba(255,255,255,0.7); padding: 2rem;'>
    <p style='font-size: 0.9rem;'>⚠️ 投資警語：本系統僅供參考，不構成投資建議。投資有風險，請謹慎評估。</p>
    <p style='font-size: 0.8rem; margin-top: 1rem;'>© 2024 AI 投資小秘書 | 讓智能科技為您的財富護航</p>
</div>
""", unsafe_allow_html=True)
