import streamlit as st
import pandas as pd

# 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# CSV 파일 경로
file_path = "202505_202505_연령별인구현황_월간.csv"

# 데이터 불러오기
df = pd.read_csv(file_path, encoding='euc-kr')

# 원본 데이터 출력
st.subheader("📄 원본 데이터")
st.dataframe(df)

# 열 이름 전처리 ('2025년05월_계_' 접두사 제거)
df = df.rename(columns=lambda x: x.replace('2025년05월_계_', '') if x.startswith('2025년05월_계_') else x)

# '총인구수' 기준 상위 5개 행정구역 추출
df_top5 = df.sort_values(by='총인구수', ascending=False).head(5)

# 연령 열만 추출
age_columns = [col for col in df_top5.columns if col.isdigit()]
age_df = df_top5[['행정구역'] + age_columns].set_index('행정구역').T
age_df.index.name = "연령"

# 시각화
st.subheader("📈 상위 5개 행정구역 연령별 인구 변화")
st.line_chart(age_df)

# 설명 텍스트
st.markdown("""
- 위 그래프는 **총인구수 기준 상위 5개 지역**의 **연령별 인구 분포**를 보여줍니다.
- 연령은 세로축, 인구수는 가로축에 표시됩니다.
- `st.line_chart`를 사용하여 Streamlit 기본 기능만으로 시각화했습니다.
""")
