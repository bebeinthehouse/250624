import streamlit as st
import pandas as pd

# 제목
st.title("2025년 5월 기준 고령화 지표 분석")

# CSV 파일 경로
file_path = "202505_202505_연령별인구현황_월간.csv"

# 데이터 읽기
df = pd.read_csv(file_path, encoding='euc-kr')
df = df.rename(columns=lambda x: x.strip())

# 연령별 컬럼 추출
age_cols = [col for col in df.columns if col.startswith("2025년05월_계_")]
total_col = "2025년05월_계_총인구수"

# 컬럼명 간단화
age_map = {}
for col in age_cols:
    if col == total_col:
        age_map[col] = "총인구수"
    else:
        age_str = col.replace("2025년05월_계_", "")
        age_map[col] = age_str

df = df[["행정기관"] + age_cols].rename(columns=age_map)

# 숫자형으로 변환
age_cols_simple = [col for col in df.columns if col not in ["행정기관"]]
df[age_cols_simple] = df[age_cols_simple].apply(pd.to_numeric, errors='coerce')

# 총인구수 기준 상위 5개 지역
top5 = df.sort_values(by="총인구수", ascending=False).head(5).copy()

# 연령대 범위 지정
def get_age_group_sum(row, start, end):
    return row[[col for col in row.index if col.isdigit() and start <= int(col) <= end]].sum()

# 지표 계산
top5["유소년(0-14세)"] = top5.apply(lambda row: get_age_group_sum(row, 0, 14), axis=1)
top5["생산(15-64세)"] = top5.apply(lambda row: get_age_group_sum(row, 15, 64), axis=1)
top5["노년(65세 이상)"] = top5.apply(lambda row: get_age_group_sum(row, 65, 100), axis=1)

top5["고령화지수"] = (top5["노년(65세 이상)"] / top5["유소년(0-14세)"]) * 100
top5["유소년부양비"] = (top5["유소년(0-14세)"] / top5["생산(15-64세)"]) * 100
top5["노년부양비"] = (top5["노년(65세 이상)"] / top5["생산(15-64세)"]) * 100

# 출력
st.subheader("상위 5개 행정구역 인구 구조 및 지표")
st.dataframe(top5[[
    "행정기관", "유소년(0-14세)", "생산(15-64세)", "노년(65세 이상)",
    "고령화지수", "유소년부양비", "노년부양비"
]])

# metric 카드 출력
st.subheader("지표 카드 비교")

for idx, row in top5.iterrows():
    st.markdown(f"### {row['행정기관']}")
    col1, col2, col3 = st.columns(3)
    col1.metric("고령화지수", f"{row['고령화지수']:.1f}")
    col2.metric("유소년부양비", f"{row['유소년부양비']:.1f}")
    col3.metric("노년부양비", f"{row['노년부양비']:.1f}")
