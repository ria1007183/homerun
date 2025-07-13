import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob

st.title("Baseball Savant 홈런 발사각 & 비거리 분석")

# 1) 선수명 입력
player_name = st.text_input("선수 이름을 입력하세요 (예: Shohei Ohtani)")

# 2) 시즌 선택 (1998~2024)
seasons = list(range(1998, 2025))
selected_seasons = st.multiselect("분석할 시즌을 선택하세요", seasons, default=[2024])

@st.cache_data
def load_data(seasons):
    dfs = []
    for season in seasons:
        try:
            path = f"data/{season}_statcast.csv"
            df = pd.read_csv(path)
            df['season'] = season
            dfs.append(df)
        except FileNotFoundError:
            st.warning(f"{season} 데이터가 없습니다.")
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame()

if player_name and selected_seasons:
    data = load_data(selected_seasons)
    # 홈런만 필터링
    hr_data = data[
        (data['player_name'].str.lower() == player_name.lower()) &
        (data['events'] == 'home_run')
    ]

    if hr_data.empty:
        st.write(f"{player_name}의 홈런 데이터가 선택한 시즌에 없습니다.")
    else:
        st.write(f"{player_name}의 {len(hr_data)}개의 홈런 데이터")
        # 발사각과 비거리 산점도
        plt.figure(figsize=(10,6))
        sns.scatterplot(data=hr_data, x='launch_angle', y='hit_distance_sc', hue='season', palette='tab20')
        plt.title(f"{player_name} 홈런 발사각 vs 비거리")
        plt.xlabel("발사각 (Launch Angle, degrees)")
        plt.ylabel("비거리 (Hit Distance, feet)")
        plt.legend(title='Season')
        st.pyplot(plt)
else:
    st.info("선수 이름과 시즌을 선택해주세요.")
