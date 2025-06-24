import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

# 제목
st.title("2025년 5월 기준 고령화 인구현황 시각화")

# CSV 파일 경로
file_path = "202505_202505_연령별인구현황_월간.csv"

# 데이터 로드
df = pd.read_csv(file_path, encoding='euc-kr')

# 열 이름 전처리
df = df.rename(columns=lambda x: x.replace('2025년05월_계_', '') if x.startswith('2025년05월_계_') else x)

# 총인구수 기준 상위 5개 지역 선택
df_top5 = df.sort_values(by='총인구수', ascending=False).head(5)

# 연령 컬럼만 추출
age_columns = [col for col in df_top5.columns if col.isdigit()]

# 고령 인구만 (60세 이상)
senior_columns = [col for col in age_columns if int(col) >= 60]
df_senior = df_top5[['행정구역'] + senior_columns].set_index('행정구역').T
df_senior.index = df_senior.index.astype(int)  # 연령을 int로 변환
df_senior.index.name = '연령'

# 📈 Plotly 그래프 (연령 = Y축, 인구 = X축)
st.subheader("👵 고령 인구(60세 이상) 연령-인구 선그래프")

# Plotly 선그래프: 연령(Y), 인구(X)
fig = px.line(
    df_senior,
    y=df_senior.index,
    x=df_senior.values,
    orientation='h',  # 가로형
    labels={"x": "인구 수", "y": "연령"},
    title="상위 5개 지역 고령 인구 분포"
)

fig.update_layout(
    height=600,
    xaxis_title="인구 수",
    yaxis_title="연령",
    legend_title="행정구역",
)

# Plotly 차트 출력
st.plotly_chart(fig, use_container_width=True)

# 🗺️ Folium 지도 시각화 (임시 행정구역 중심점 사용 예시)
st.subheader("📍 상위 5개 지역 위치 지도")

# 간단한 위도/경도 매핑 (예: 실제 값 필요 시 외부 DB 필요)
# 아래 예시는 서울, 부산, 인천, 대구, 대전 중심 좌표 예시
area_coords = {
    "서울특별시": [37.5665, 126.9780],
    "부산광역시": [35.1796, 129.0756],
    "인천광역시": [37.4563, 126.7052],
    "대구광역시": [35.8722, 128.6025],
    "대전광역시": [36.3504, 127.3845],
}

# folium 지도 생성
m = folium.Map(location=[36.5, 127.8], zoom_start=6)

# 마커 추가
for area in df_top5['행정구역']:
    if area in area_coords:
        folium.Marker(
            location=area_coords[area],
            popup=f"{area}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

# streamlit-folium으로 표시
st_folium(m, width=700, height=450)

# 🔍 참고: yfinance는 주식 데이터용으로, 인구 데이터와 직접 연관은 없습니다.
