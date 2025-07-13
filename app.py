import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="2025 홈런 분석", layout="wide")
st.title("⚾ 2025년 홈런 발사각 & 비거리 분석")

@st.cache_data
def load_2025_data():
    df = pd.read_csv("data/2025_statcast.csv")
    df['season'] = 2025
    return df

data = load_2025_data()

# 유효성 검사
if data.empty:
    st.error("데이터를 불러올 수 없습니다. 파일 경로 또는 내용 확인 필요.")
else:
    # 선수명 자동완성용 리스트
    player_list = sorted(data['player_name'].dropna().unique())
    player_name = st.selectbox("분석할 선수를 선택하세요", player_list)

    # 홈런 데이터 필터링
    hr_data = data[(data['player_name'] == player_name) & (data['events'] == 'home_run')]

    if hr_data.empty:
        st.warning(f"{player_name}의 홈런 데이터가 없습니다.")
    else:
        st.success(f"{player_name}의 2025 시즌 홈런 {len(hr_data)}개 분석 결과")
        avg_angle = hr_data['launch_angle'].mean()
        avg_dist = hr_data['hit_distance_sc'].mean()
        st.write(f"📐 평균 발사각: **{avg_angle:.1f}°**, 📏 평균 비거리: **{avg_dist:.1f} ft**")

        # 산점도
        plt.figure(figsize=(10,6))
        sns.scatterplot(data=hr_data, x='launch_angle', y='hit_distance_sc', color='crimson')
        plt.title(f"{player_name} - 2025 홈런 발사각 vs 비거리")
        plt.xlabel("발사각 (Launch Angle, degrees)")
        plt.ylabel("비거리 (Hit Distance, feet)")
        st.pyplot(plt)
