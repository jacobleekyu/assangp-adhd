import streamlit as st
from PIL import Image

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="ADHD 성향 설문",
    page_icon="🌱",
    layout="centered"
)

# -----------------------------
# 점수 기준
# -----------------------------
OPTIONS = {
    "전혀 아니다": 0,
    "가끔": 1,
    "자주": 2,
    "매우 자주": 3
}

# -----------------------------
# 질문 데이터
# 이미지 파일만 교체하면 됨
# -----------------------------
questions = [
    {
        "title": "1번 질문",
        "question": "제출 직전에 사소한 수정에 집착한 적이 얼마나 자주 있나요?",
        "image": "q1.png"
    },
    {
        "title": "2번 질문",
        "question": "해야 할 일을 정리하기 어려웠던 적이 얼마나 자주 있나요?",
        "image": "q2.png"
    },
    {
        "title": "3번 질문",
        "question": "공부하려다 다른 생각으로 빠진 적이 얼마나 자주 있나요?",
        "image": "q3.png"
    },
    {
        "title": "4번 질문",
        "question": "가만히 앉아 있기 힘들었던 적이 얼마나 자주 있나요?",
        "image": "q4.png"
    },
    {
        "title": "5번 질문",
        "question": "지루한 일에서 집중이 끊긴 적이 얼마나 자주 있나요?",
        "image": "q5.png"
    },
    {
        "title": "6번 질문",
        "question": "남 말을 듣다가 딴생각한 적이 얼마나 자주 있나요?",
        "image": "q6.png"
    },
    {
        "title": "7번 질문",
        "question": "물건을 자주 잃어버린 적이 있나요?",
        "image": "q7.png"
    },
    {
        "title": "8번 질문",
        "question": "회의나 수업 중 자리를 뜨고 싶었던 적이 얼마나 자주 있나요?",
        "image": "q8.png"
    },
    {
        "title": "9번 질문",
        "question": "대화 중 내가 말을 너무 많이 하고 있다고 느낀 적이 있나요?",
        "image": "q9.png"
    },
    {
        "title": "10번 질문",
        "question": "상대방 말을 끊고 끼어든 적이 얼마나 자주 있나요?",
        "image": "q10.png"
    },
]

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = 0

if "scores" not in st.session_state:
    st.session_state.scores = []

# -----------------------------
# 스타일
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #FFFDF7;
}

.question-box {
    padding: 20px;
    border-radius: 20px;
    background: #F8F4EA;
    border: 2px solid #E6DDC6;
}

.result-box {
    padding: 30px;
    border-radius: 20px;
    background: #FFF3CD;
    border: 2px solid #F0C36D;
    text-align: center;
}

.big-score {
    font-size: 64px;
    font-weight: bold;
    color: #FF8C42;
}

.small-text {
    font-size: 18px;
    color: #555;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 첫 화면
# -----------------------------
if st.session_state.page == 0:

    st.title("🌱 ADHD 성향 설문")

    cover = Image.open("cover.jpg")
    st.image(cover, use_container_width=True)

    st.markdown("""
    ### 안내
    - 총 10개의 질문으로 구성되어 있습니다.
    - 각 문항에 대해 가장 가까운 답변을 선택해주세요.
    - 본 설문은 진단 목적이 아닌 참고용입니다.
    """)

    if st.button("설문 시작하기", use_container_width=True):
        st.session_state.page = 1
        st.rerun()

# -----------------------------
# 질문 화면
# -----------------------------
elif 1 <= st.session_state.page <= 10:

    idx = st.session_state.page - 1
    q = questions[idx]

    st.progress(st.session_state.page / 10)

    st.markdown(
        f"""
        <div class="question-box">
            <h2>{q['title']}</h2>
            <p style="font-size:20px;">
                {q['question']}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    image = Image.open(q["image"])
    st.image(image, use_container_width=True)

    answer = st.radio(
        "선택해주세요",
        list(OPTIONS.keys()),
        key=f"q_{idx}"
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.session_state.page > 1:
            if st.button("이전"):
                st.session_state.page -= 1
                st.rerun()

    with col2:
        if st.button("다음", use_container_width=True):

            score = OPTIONS[answer]

            if len(st.session_state.scores) > idx:
                st.session_state.scores[idx] = score
            else:
                st.session_state.scores.append(score)

            st.session_state.page += 1
            st.rerun()

# -----------------------------
# 결과 화면
# -----------------------------
elif st.session_state.page == 11:

    total_score = sum(st.session_state.scores)

    st.title("📊 결과")

    result_img = Image.open("result.png")
    st.image(result_img, use_container_width=True)

    st.markdown(
        f"""
        <div class="result-box">
            <div class="small-text">당신의 총 점수</div>
            <div class="big-score">{total_score}점</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 점수 해석
    if total_score <= 10:
        result_text = "상대적으로 ADHD 경향이 낮은 편입니다."
    elif total_score <= 20:
        result_text = "약간의 ADHD 성향이 관찰될 수 있습니다."
    else:
        result_text = "ADHD 성향이 비교적 높은 편으로 나타났습니다."

    st.info(result_text)

    st.caption("※ 본 결과는 의학적 진단이 아닙니다.")

    if st.button("다시 하기", use_container_width=True):
        st.session_state.page = 0
        st.session_state.scores = []
        st.rerun()
