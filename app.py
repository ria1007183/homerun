import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="2025 홈런 분석", layout="wide")
st.title("⚾ 2025년 홈런 발사각 & 비거리 분석")

@st.cache_data
def load_2025_data():
    try:
        df = pd.read_csv("data/2025_statcast.csv")
        if df.empty or df.columns.size == 0:
            raise ValueError("CSV 파일이 비어 있거나 형식이 잘못되었습니다.")
        df['season'] = 2025
        return df
    except Exception as e:
        st.error(f"데이터 로딩 중 오류 발생: {e}")
        return pd.DataFrame()

data = load_2025_data()

if data.empty:
    st.warning("2025 시즌 데이터를 불러오지 못했습니다. 파일이 있는지 확인해주세요.")
else:
    # 선수명 자동완성 리스트
    player_list = sorted(data['player_name'].dropna().unique())
    player_name = st.selectbox("분석할 선수를 선택하세요", player_list)

    # 홈런 데이터 필터링
    hr_data = data[
        (data['player_name'] == player_name) &
        (data['events'] == 'home_run')
    ]

    if hr_data.empty:
        st.warning(f"{player_name}의 홈런 데이터가 없습니다.")
    else:
        # 피트 → 미터 변환
        hr_data['distance_m'] = hr_data['hit_distance_sc'] * 0.3048

        # 평균값 계산
        avg_angle = hr_data['launch_angle'].mean()
        avg_dist_m = hr_data['distance_m'].mean()

        # 요약 정보 출력
        st.success(f"{player_name}의 2025 시즌 홈런 {len(hr_data)}개 분석 결과")
        st.markdown(f"📐 평균 발사각: **{avg_angle:.1f}°**")
        st.markdown(f"📏 평균 비거리: **{avg_dist_m:.1f} m**")

        # 산점도 출력 (미터 단위)
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=hr_data, x='launch_angle', y='distance_m', color='crimson')
        plt.title(f"{player_name} - 2025 홈런 발사각 vs 비거리 (미터)")
        plt.xlabel("발사각 (Launch Angle, degrees)")
        plt.ylabel("비거리 (Distance, meters)")
        st.pyplot(plt)

