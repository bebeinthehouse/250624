import streamlit as st

# MBTI 성격별 특징 + 추천 직업
mbti_profiles = {
    "INTJ": {
        "description": "🧠 전략적 사고를 가진 계획형 혁신가",
        "jobs": ["전략 컨설턴트", "시스템 분석가", "AI 연구원", "IT 기획자"]
    },
    "INTP": {
        "description": "🔍 논리와 아이디어를 사랑하는 탐구가",
        "jobs": ["데이터 분석가", "이론 물리학자", "프로그래머", "UX 리서처"]
    },
    "ENTJ": {
        "description": "💼 타고난 리더, 추진력 있는 지휘관",
        "jobs": ["CEO", "경영 컨설턴트", "기획 관리자", "변호사"]
    },
    "ENTP": {
        "description": "🌟 창의적인 아이디어 뱅크, 도전정신 가득",
        "jobs": ["스타트업 창업가", "마케팅 기획자", "기자", "방송 PD"]
    },
    "INFJ": {
        "description": "🌱 깊은 통찰력을 가진 이상주의자",
        "jobs": ["심리상담가", "교육자", "작가", "사회운동가"]
    },
    "INFP": {
        "description": "🎨 감성과 가치 중심의 예술가형",
        "jobs": ["시인", "소설가", "그래픽 디자이너", "인권운동가"]
    },
    "ENFJ": {
        "description": "🤝 사람을 이끄는 따뜻한 리더",
        "jobs": ["교사", "HR 매니저", "연설가", "멘토"]
    },
    "ENFP": {
        "description": "🌈 에너지 넘치는 낙천적 탐험가",
        "jobs": ["홍보 담당자", "크리에이터", "방송 작가", "기획자"]
    },
    "ISTJ": {
        "description": "📋 책임감 강한 현실주의자",
        "jobs": ["행정 공무원", "회계사", "군인", "검사"]
    },
    "ISFJ": {
        "description": "🛡️ 따뜻한 헌신가, 조용한 수호자",
        "jobs": ["간호사", "사회복지사", "초등 교사", "도서관 사서"]
    },
    "ESTJ": {
        "description": "📊 조직을 움직이는 관리자형",
        "jobs": ["경찰관", "은행원", "공무원", "프로젝트 매니저"]
    },
    "ESFJ": {
        "description": "🎉 모두를 챙기는 친절한 조정자",
        "jobs": ["이벤트 플래너", "간호사", "비서", "상담 교사"]
    },
    "ISTP": {
        "description": "🛠️ 실용적인 문제 해결사",
        "jobs": ["파일럿", "기계공", "응급 구조사", "보안 전문가"]
    },
    "ISFP": {
        "description": "🎨 자유로운 감성의 예술가",
        "jobs": ["플로리스트", "패션 디자이너", "요리사", "사진작가"]
    },
    "ESTP": {
        "description": "🏃‍♂️ 액션과 스릴을 사랑하는 도전가",
        "jobs": ["기업가", "스포츠 트레이너", "영업 전문가", "구조대원"]
    },
    "ESFP": {
        "description": "🎤 무대를 사랑하는 분위기 메이커",
        "jobs": ["배우", "MC", "공연 기획자", "여행 가이드"]
    }
}

# 페이지 설정
st.set_page_config(page_title="MBTI 직업 추천기", page_icon="🧭")

# 제목
st.title("🧭 MBTI 기반 직업 추천 사이트")
st.markdown("당신의 MBTI에 맞는 성향과 어울리는 **직업**을 추천해드릴게요! 😄")

# MBTI 선택
selected_mbti = st.selectbox("👇 당신의 MBTI를 선택하세요", list(mbti_profiles.keys()))

# 추천 버튼
if st.button("🎯 추천 직업 보기"):
    profile = mbti_profiles[selected_mbti]
    st.success(f"✨ {selected_mbti} - {profile['description']}")
    st.markdown("**추천 직업 리스트:**")
    for job in profile["jobs"]:
        st.write(f"💼 {job}")
    
    # 풍선 효과
    st.balloons()
