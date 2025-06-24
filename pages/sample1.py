import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

def app():
    st.title('대한민국 연령대별 인구 분포 (상위 5개 행정구역 기준)')

    # 데이터 불러오기
    df = pd.read_csv('202505_202505_연령별인구현황_월간.csv', encoding='euc-kr')
    df['행정구역'] = df['행정구역'].astype(str).str.split(' ').str[0]

    # 열 이름 정리
    새로운_열_이름 = []
    for 열 in df.columns:
        if '2025년05월_계_' in 열:
            새_열 = 열.replace('2025년05월_계_', '')
            if '총인구수' in 새_열:
                새_열 = '총인구수'
            elif '연령구간인구수' in 새_열:
                새_열 = '연령구간인구수'
            새로운_열_이름.append(새_열)
        else:
            새로운_열_이름.append(열)
    df.columns = 새로운_열_이름

    # 숫자형 변환
    숫자열_목록 = [열 for 열 in df.columns if 열 != '행정구역']
    for 열 in 숫자열_목록:
        df[열] = df[열].astype(str).str.replace(',', '', regex=False).astype(int)

    # 상위 5개 행정구역 추출
    상위5 = df.sort_values(by='총인구수', ascending=False).head(5)['행정구역'].tolist()
    df_상위5 = df[df['행정구역'].isin(상위5)].copy()

    # 연령별 melt 처리
    df_변환 = df_상위5.melt(id_vars=['행정구역', '총인구수', '연령구간인구수'],
                         var_name='연령',
                         value_name='인구수')
    df_변환['연령'] = df_변환['연령'].str.extract('(\d+)').astype(int)

    st.write("---")
    st.header("📄 원본 데이터")
    st.dataframe(df)

    st.write("---")
    st.header("📈 Streamlit 기본 선그래프")
    피벗 = df_변환.pivot_table(index='연령', columns='행정구역', values='인구수')
    st.line_chart(피벗)

    # 60세 이상만 필터링
    고령_데이터 = df_변환[df_변환['연령'] >= 60]

    st.write("---")
    st.header("📊 Plotly 선그래프 (연령 세로축, 인구 가로축)")

    fig = px.line(
        고령_데이터,
        x="인구수",
        y="연령",
        color="행정구역",
        orientation="h",
        labels={"인구수": "인구 수", "연령": "연령"},
        title="고령 인구 (60세 이상) - 상위 5개 행정구역"
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

    st.write("---")
    st.header("🗺️ 지도 시각화 (Folium)")

    # 행정구역 위도/경도 (예시)
    행정구역_좌표 = {
        "서울특별시": [37.5665, 126.9780],
        "부산광역시": [35.1796, 129.0756],
        "인천광역시": [37.4563, 126.7052],
        "대구광역시": [35.8722, 128.6025],
        "대전광역시": [36.3504, 127.3845]
    }

    지도 = folium.Map(location=[36.5, 127.8], zoom_start=6)

    for 지역 in 상위5:
        if 지역 in 행정구역_좌표:
            folium.Marker(
                location=행정구역_좌표[지역],
                popup=f"{지역}",
                icon=folium.Icon(color="blue")
            ).add_to(지도)

    st_folium(지도, width=700, height=450)

if __name__ == '__main__':
    app()
