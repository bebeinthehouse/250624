import streamlit as st
import pandas as pd

# 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# CSV 파일 읽기
file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding='euc-kr')

# 원본 데이터 표시
st.subheader("원본 데이터")
st.dataframe(df)

# 필요한 열 추출 및 전처리
df = df.rename(columns=lambda x: x.strip())  # 공백 제거
cols = df.columns

# '2025년05월_계_'로 시작하는 열만 선택 + '총인구수'
age_cols = [col for col in cols if col.startswith("2025년05월_계_")]
total_col = "2025년05월_계_총인구수"

# 연령 숫자만 추출하여 새로운 컬럼명 생성
age_map = {}
for col in age_cols:
    if col == total_col:
        age_map[col] = "총인구수"
    else:
        age_str = col.replace("2025년05월_계_", "")
        age_map[col] = age_str

# 컬럼명 변경
df = df[["행정기관"] + age_cols]
df = df.rename(columns=age_map)

# 총인구수 기준 상위 5개 행정구역 추출
top5 = df.sort_values(by="총인구수", ascending=False).head(5)

# 총인구수 제외한 연령 데이터만 선택
age_only_cols = [col for col in top5.columns if col not in ["행정기관", "총인구수"]]

# 정수형으로 변환
top5[age_only_cols] = top5[age_only_cols].apply(pd.to_numeric, errors='coerce')

# 연령별 인구 데이터: index=연령, columns=행정기관 형태로 변환
top5_age = top5.set_index("행정기관")[age_only_cols].T
top5_age.index.name = "연령"

# 시각화
st.subheader("상위 5개 행정구역의 연령별 인구 분포")
st.line_chart(top5_age)

# 부가 설명
st.markdown("""
- 본 그래프는 2025년 5월 기준, 총인구수가 많은 상위 5개 행정기관의 연령별 인구를 선 그래프로 표현한 것입니다.
- 데이터 출처: 통계청 월간 인구 동향
""")
