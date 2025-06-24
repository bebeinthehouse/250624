import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# CSV 파일 읽기
file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding='euc-kr')

# 원본 데이터 표시
st.subheader("원본 데이터")
st.dataframe(df)

# 컬럼 정리
df = df.rename(columns=lambda x: x.strip())  # 공백 제거
age_cols = [col for col in df.columns if col.startswith("2025년05월_계_")]
total_col = "2025년05월_계_총인구수"
age_map = {}

for col in age_cols:
    if col == total_col:
        age_map[col] = "총인구수"
    else:
        age_str = col.replace("2025년05월_계_", "")
        age_map[col] = age_str

# 컬럼명 변경
df = df[["행정기관"] + age_cols].rename(columns=age_map)

# 상위 5개 지역 추출
top5 = df.sort_values(by="총인구수", ascending=False).head(5)
age_only_cols = [col for col in top5.columns if col not in ["행정기관", "총인구수"]]
top5[age_only_cols] = top5[age_only_cols].apply(pd.to_numeric, errors='coerce')

# 데이터 구조 변환
top5_age = top5.set_index("행정기관")[age_only_cols].T
top5_age.index.name = "연령"

# 시각화
st.subheader("상위 5개 행정구역의 연령별 인구 분포 (원의 크기로 표시)")

fig, ax = plt.subplots(figsize=(10, 6))

for region in top5_age.columns:
    y = top5_age.index.astype(int)
    x = top5_age[region]
    sizes = (x / x.max()) * 300  # 원 크기 비례
    ax.plot(y, x, label=region)
    ax.scatter(y, x, s=sizes, alpha=0.6)

ax.set_xlabel("연령")
ax.set_ylabel("인구 수")
ax.set_title("연령별 인구 분포 (단위: 명)")
ax.legend(title="행정기관")
ax.grid(True)

st.pyplot(fig)

# 설명
st.markdown("""
- 위 그래프는 연령별 인구를 선과 원으로 동시에 표현합니다.
- 각 원의 크기는 해당 연령의 인구 수에 비례합니다.
""")
