import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="질소-옥신 활성화 계산기", layout="wide", page_icon="🌱")

st.title("🌱 질소 화합물 농도에 따른 옥신(Auxin) 활성화 계산기")
st.write("질소 화합물의 농도가 식물 내 옥신 생합성 및 신호전달 활성화에 미치는 영향을 가우시안 반응 모델(Bell-shaped Curve)을 통해 시뮬레이션합니다.")

# 사이드바: 파라미터 조절 패널
st.sidebar.header("🧪 실험 파라미터 설정")

nitrogen_type = st.sidebar.selectbox(
    "질소 화합물 종류 선택",
    ["질산염 (Nitrate, NO3-)", "암모늄 (Ammonium, NH4+)"]
)

# 화합물별 기본 권장값 세팅 수정을 위한 가이드라인 제공
if nitrogen_type == "질산염 (Nitrate, NO3-)":
    default_mu = 5.0      # 최적 농도 기본값 (mM)
    default_sigma = 2.5   # 민감도 범위
else:
    default_mu = 2.0      # 암모늄은 고농도 독성이 강하므로 최적 농도가 낮음
    default_sigma = 1.0

st.sidebar.subheader("모델 세부 매개변수")
mu = st.sidebar.slider("최적 질소 농도 (μ, mM)", min_value=0.5, max_value=20.0, value=default_mu, step=0.5)
sigma = st.sidebar.slider("농도 민감도 범위 (σ)", min_value=0.5, max_value=10.0, value=default_sigma, step=0.1)
max_act = st.sidebar.slider("최대 옥신 활성화도 (%)", min_value=50, max_value=100, value=100, step=5)
base_act = st.sidebar.slider("기저(최소) 활성화도 (%)", min_value=0, max_value=30, value=10, step=5)

st.sidebar.subheader("📍 현재 측정 데이터 입력")
current_N = st.sidebar.slider("현재 질소 화합물 농도 (mM)", min_value=0.0, max_value=25.0, value=mu, step=0.1)

# 옥신 활성화도 계산 함수 (가우시안 모델 기반)
def calculate_auxin_activation(N, mu, sigma, max_act, base_act):
    # f(x) = Base + (Max - Base) * exp(-(x - mu)^2 / (2 * sigma^2))
    activation = base_act + (max_act - base_act) * np.exp(-((N - mu) ** 2) / (2 * (sigma ** 2)))
    return activation

# 결과 계산
current_auxin_level = calculate_auxin_activation(current_N, mu, sigma, max_act, base_act)

# 화면 레이아웃 분할 (결과 수치 / 그래프)
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📊 계산 및 시뮬레이션 결과")
    st.write(f"**선택된 화합물:** {nitrogen_type}")
    
    st.metric(label="현재 입력된 질소 농도", value=f"{current_N:.1f} mM")
    st.metric(label="예측된 옥신 활성화도", value=f"{current_auxin_level:.2f} %")
    
    # 상태별 해석 제공
    st.markdown("### 💡 식물 생리 상태 해석")
    if current_N < (mu - sigma):
        st.error("⚠️ **질소 결핍 상태:** 질소 신호 부족으로 인해 옥신 생합성 유전자(YUCCA 등)의 발현이 저하되어 측근(Lateral Root) 발달이 억제될 수 있습니다.")
    elif (mu - sigma) <= current_N <= (mu + sigma):
        st.success("✅ **최적 질소-옥신 밸런스:** 적절한 질소 신호가 옥신의 최적 흐름과 축적을 유도하여, 뿌리 계의 분지와 성장을 극대화합니다.")
    else:
        st.warning("⚠️ **질소 과잉 (과포화) 상태:** 고농도 질소(특히 암모늄 독성 등)로 인해 옥신 수송체(PIN)의 비정상적 다운레귤레이션이 일어나
