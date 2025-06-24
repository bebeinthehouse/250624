import streamlit as st
import pandas as pd

def app():
    st.title('대한민국 연령대별 인구 분포 (상위 5개 행정구역 기준)')

    # 데이터 불러오기 ('euc-kr' 인코딩 사용)
    df = pd.read_csv('202505_202505_연령별인구현황_월간.csv', encoding='euc-kr')

    # 데이터 전처리: 행정구역 이름 정제
    df['행정구역'] = df['행정구역'].astype(str).str.split(' ').str[0]

    # 원본 데이터 표시
    st.subheader("📄 원본 데이터")
    st.dataframe(df)

# 열 이름 전처리 ('2025년05월_계_' 접두사 제거)
df = df.rename(columns=lambda x: x.replace('2025년05월_계_', '') if x.startswith('2025년05월_계_') else x)

# 총인구수 기준 상위 5개 행정구역 추출
df_top5 = df.sort_values(by='총인구수', ascending=False).head(5)

# 연령 컬럼만 필터링
age_columns = [col for col in df_top5.columns if col.isdigit()]

# 전체 연령별 인구 변화 시각화
df_all_ages = df_top5[['행정구역'] + age_columns].set_index('행정구역').T
df_all_ages.index.name = "연령"

st.subheader("📈 상위 5개 행정구역 연령별 인구 변화")
st.line_chart(df_all_ages)

# -----------------------------
# 🔍 60세 이상 고령 인구 필터링
# -----------------------------
# 숫자로 변환 후 60 이상 필터
senior_age_columns = [col for col in age_columns if col.isdigit() and int(col) >= 60]

# 고령 인구만 추출
df_senior = df_top5[['행정구역'] + senior_age_columns].set_index('행정구역').T
df_senior.index.name = "연령 (60세 이상)"

st.subheader("👵 고령 인구(60세 이상) 현황")
st.line_chart(df_senior)

# 설명
st.markdown("""
- **총인구수 기준 상위 5개 행정구역**의 **연령별 인구 분포**와 **60세 이상 고령 인구 현황**을 확인할 수 있습니다.
- 고령 인구 그래프는 60세 이상만 필터링하여 구성했습니다.
""")
