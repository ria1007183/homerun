import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Baseball Savant 홈런 발사각 & 비거리 분석")

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

data = load_data(selected_seasons)

if not data.empty:
    player_list = sorted(data['player_name'].dropna().unique())
    player_name = st.selectbox("선수를 선택하세요", player_list)
    hr_data = data[(data['player_name'] == player_name) & (data['events'] == 'home_run')]

    if hr_data.empty:
        st.write(f"{player_name}의 홈런 데이터가 없습니다.")
    else:
        st.write(f"{player_name}의 {len(hr_data)}개 홈런 데이터")
        plt.figure(figsize=(10,6))
        sns.scatterplot(data=hr_data, x='launch_angle', y='hit_distance_sc', hue='season', palette='tab20')
        plt.title(f"{player_name} 홈런 발사각 vs 비거리")
        plt.xlabel("발사각 (Launch Angle, degrees)")
        plt.ylabel("비거리 (Hit Distance, feet)")
        plt.legend(title='Season')
        st.pyplot(plt)

else:
    st.info("선택한 시즌의 데이터가 없습니다.")
