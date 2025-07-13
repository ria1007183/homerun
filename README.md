# 2025 홈런 발사각 & 비거리 분석 웹앱

이 앱은 Baseball Savant에서 수집한 2025년 Statcast 데이터를 기반으로,  
선수를 선택하면 그 선수의 홈런 발사각과 비거리를 시각화해주는 스트림릿 웹앱입니다.

## 사용 방법

### 1️⃣ 데이터 파일 준비
- [Baseball Savant Statcast Search](https://baseballsavant.mlb.com/statcast_search)에서
  `2025 시즌` 데이터를 `CSV`로 다운로드하세요.
- 파일 이름을 `2025_statcast.csv`로 바꿔서 `data/` 폴더에 넣으세요.

### 2️⃣ 앱 실행

```bash
pip install -r requirements.txt
streamlit run app.py
