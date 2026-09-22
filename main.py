import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

# 메인 타이틀
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown("박스오피스 상위 영화 216편의 데이터를 바탕으로 장르별 분포와 변수 간의 관계를 시각화합니다.")

# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # genre 열 전처리: '|' 구분자로 나눈 후 첫 번째 장르만 추출
    df['genre'] = df['genre'].fillna('미상').astype(str).apply(lambda x: x.split('|')[0].strip())
    
    return df

df = load_data()

# 데이터 미리보기 (접기/펼치기)
with st.expander("📄 데이터 요약표 보기 (상위 10개 행)"):
    st.dataframe(df.head(10), use_container_width=True)

st.markdown("---")

# -------------------------------------------------------------------
# 그래프 1: 장르별 영화 편수 (도넛 그래프)
# -------------------------------------------------------------------
st.header("1. 장르별 영화 편수 분포")

# 장르별 편수 집계
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

# Plotly 도넛 차트 생성
fig_donut = px.pie(
    genre_counts,
    names='genre',
    values='count',
    hole=0.4,
    title="장르별 영화 편수 비율"
)

# 마우스 오버(호버) 툴팁 설정: 편수와 비율 표시
fig_donut.update_traces(
    hovertemplate="<b>장르: %{label}</b><br>영화 편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

# 그래프 출력
st.plotly_chart(fig_donut, use_container_width=True)

# 그래프 해설 구역
st.subheader("📌 이 그래프로 알 수 있는 것")
st.info("특정 주요 장르가 전체 개봉 영화의 상당 부분을 차지하며, 특정 장르 선호 및 제작 쏠림 현상이 존재함을 알 수 있습니다.")

st.markdown("---")

# -------------------------------------------------------------------
# 그래프 2: 개봉일 스크린수와 총 관객수의 관계 (산점도)
# -------------------------------------------------------------------
st.header("2. 개봉일 스크린수와 총 관객수의 관계")

# Plotly 산점도 생성
fig_scatter = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title="개봉일 스크린수 vs 총 관객수",
    labels={
        'first_scrn': '개봉일 스크린수 (개)',
        'total_audi': '총 관객수 (명)',
        'genre': '장르'
    }
)

# 그래프 출력
st.plotly_chart(fig_scatter, use_container_width=True)

# 그래프 해설 구역
st.subheader("📌 이 그래프로 알 수 있는 것")
st.info("개봉 첫날 확보한 스크린수가 많을수록 최종 총 관객수도 대체로 증가하는 양의 상관관계가 나타남을 알 수 있습니다.")
