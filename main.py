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
# 그래프 2: 장르 및 영화별 총 관객수 분포 (트리맵)
# -------------------------------------------------------------------
st.header("2. 장르 및 영화별 총 관객수 분포 (트리맵)")

# Plotly 트리맵 생성: 계층 구조 (전체 영화 -> 장르 -> 영화명)
fig_treemap = px.treemap(
    df,
    path=[px.Constant("전체 영화"), 'genre', 'movieNm'],
    values='total_audi',
    color='genre',
    title="장르 및 영화별 총 관객수 분포"
)

# 마우스 오버(호버) 툴팁 설정: 영화명(또는 장르명)과 총 관객수 표시
fig_treemap.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객수: %{value:,.0f}명<extra></extra>"
)

# 그래프 출력
st.plotly_chart(fig_treemap, use_container_width=True)

# 그래프 해설 구역
st.subheader("📌 이 그래프로 알 수 있는 것")
st.info("흥행 규모가 큰 장르 내에서도 특정 블록버스터 영화 한두 편이 전체 관객수의 대부분을 차지하고 있음을 알 수 있습니다.")

st.markdown("---")

# -------------------------------------------------------------------
# 그래프 3: 총 관객수 분포 (히스토그램)
# -------------------------------------------------------------------
st.header("3. 총 관객수 분포 (히스토그램)")

# 최다 관객 영화 정보 자동 추출
top_movie = df.loc[df['total_audi'].idxmax()]
top_movie_title = top_movie['movieNm']
top_movie_audi = top_movie['total_audi']

# Plotly 히스토그램 생성
fig_hist = px.histogram(
    df,
    x='total_audi',
    nbins=30,
    title="영화별 총 관객수 분포",
    labels={'total_audi': '총 관객수 (명)', 'count': '영화 수'},
    hover_data=['movieNm']
)

fig_hist.update_layout(
    yaxis_title="영화 수 (편)"
)

# 그래프 출력
st.plotly_chart(fig_hist, use_container_width=True)

# 그래프 해설 구역
st.subheader("📌 이 그래프로 알 수 있는 것")
st.info(
    f"대부분의 영화가 총 관객수 **300만 명 이하의 하위 구간**에 집중되어 있으며, "
    f"가장 관객이 많은 영화는 **'{top_movie_title}'**({top_movie_audi:,.0f}명)입니다."
)

st.markdown("---")

# -------------------------------------------------------------------
# 그래프 4: 개봉일 스크린수와 총 관객수의 관계 (산점도)
# -------------------------------------------------------------------
st.header("4. 개봉일 스크린수와 총 관객수의 관계")

# Plotly 산점도 생성: 개봉일 스크린수 vs 총 관객수 (장르별 색상 지정, 영화명 마우스 오버)
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

fig_scatter.update_traces(
    hovertemplate="<b>영화명: %{hovertext}</b><br>개봉일 스크린수: %{x:,.0f}개<br>총 관객수: %{y:,.0f}명<extra></extra>"
)

# 그래프 출력
st.plotly_chart(fig_scatter, use_container_width=True)

# 그래프 해설 구역
st.subheader("📌 이 그래프로 알 수 있는 것")
st.info("개봉 첫날 확보한 스크린수가 많을수록 최종 총 관객수도 대체로 증가하는 양의 상관관계를 보이지만, 스크린수가 적어도 크게 흥행한 이례적인 영화도 존재함을 알 수 있습니다.")
