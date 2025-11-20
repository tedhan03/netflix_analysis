import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import ast
from ast import literal_eval
from collections import Counter
from pathlib import Path

st.set_page_config(page_title="🎬 Netflix 콘텐츠 분석", layout="wide")

plt.rcParams['font.family'] = 'Malgun Gothic'

st.header("netflix 컨텐츠 분석")

st.sidebar.text("sidebar")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Netflix_2015_logo.svg/1280px-Netflix_2015_logo.svg.png")
selected = st.sidebar.selectbox("선택하세요", ["장르 & 연령등급", "시간대 & 트렌드", "제작국가 & 글로벌", "평점 & 인기도"])
st.sidebar.header(selected + " 분석을 선택하셨습니다.")



@st.cache_data
def _read_csv_from_path(csv_path: Path) -> pd.DataFrame:
    return pd.read_csv(csv_path)

def load_titles_csv() -> pd.DataFrame:
    """
    1) 스크립트 파일과 같은 폴더의 titles.csv
    2) 스크립트 상위 폴더의 titles.csv
    3) 못 찾으면 업로더로 받기
    """
    base_dir = Path(__file__).resolve().parent
    candidates = [
        base_dir / "titles.csv",
        base_dir.parent / "titles.csv",
    ]
    for p in candidates:
        if p.exists():
            return _read_csv_from_path(p)

    st.warning("⚠️ titles.csv를 자동으로 찾지 못했습니다. 아래에서 파일을 업로드하세요.")
    up = st.file_uploader("📂 titles.csv 업로드", type="csv")
    if up is not None:
        return pd.read_csv(up)

    # 업로드도 없으면 빈 DF 반환(아래에서 처리)
    return pd.DataFrame()


# 메뉴 1
def show_menu1():
    st.header("장르 및 연령등급 분석")

    df = load_titles_csv()
    if df.empty:
        st.stop()

    # 장르 파싱
    def parse_genres(genre_str):
        if pd.notna(genre_str):
            genre_str = (
                str(genre_str)
                .replace("[", "")
                .replace("]", "")
                .replace("'", "")
                .replace('"', "")
            )
            genres = []
            for g in genre_str.split(","):
                if g.strip():
                    genres.append(g.strip())
            return genres
        return []

    df["genres_list"] = df["genres"].apply(parse_genres)
    df["age_certification"] = df["age_certification"].fillna("미지정")
    df["release_year"] = df["release_year"].fillna(0).astype(int)
    # 연도형 → datetime 변환 (연도 축 그리기용)
    df["release_year"] = pd.to_datetime(df["release_year"], format="%Y", errors="coerce")

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "장르별 작품수",
            "연령등급 통계",
            "장르와 연령등급 관계",
            "연도별 장르 트렌드",
        ]
    )

    with tab1:
        st.header("장르별 작품수")

        all_genres = []
        for genres in df["genres_list"]:
            for genre in genres:
                all_genres.append(genre)

        genre_counts = Counter(all_genres)
        genre_data = [{"장르": g, "작품수": c} for g, c in genre_counts.items()]
        genre_df = pd.DataFrame(genre_data).sort_values("작품수", ascending=False)

        fig = px.bar(
            genre_df,
            x="장르",
            y="작품수",
            title=f"장르별 작품 수 (총 {len(genre_df)}개 장르)",
            color="작품수",
            color_continuous_scale="Blues",
        )
        fig.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(genre_df, use_container_width=True)

    with tab2:
        st.header("연령등급별 통계")

        age_data = df["age_certification"].value_counts().reset_index()
        age_data.columns = ["연령등급", "작품수"]

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                age_data,
                x="연령등급",
                y="작품수",
                title="연령등급별 작품 수",
                color="작품수",
                color_continuous_scale="Reds",
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.pie(
                age_data, names="연령등급", values="작품수", title="연령등급 비율", hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)

        st.dataframe(age_data, use_container_width=True)

    with tab3:
        st.header("장르와 연령등급의 관계")

        input_age = st.selectbox("연령등급 선택", df["age_certification"].unique())

        result = (
            df.query("age_certification == @input_age")
            .groupby("genres")
            .agg(개수=("id", "count"))
            .sort_values("개수", ascending=False)["개수"]
            .head(3)
        )

        result = list(dict(result).items())

        cols = st.columns(3)
        for i, col in enumerate(cols):
            with col:
                st.markdown(
                    f"""
                    <div style="
                        background:#f0f2f6;
                        border-radius:10px;
                        padding:15px;
                        text-align:center;
                        box-shadow:0 2px 6px rgba(0,0,0,0.1);
                    ">
                        <h4>🏆 {i+1}위</h4>
                        <h3>{result[i][0]}</h3>
                        <p><b>{int(result[i][1])} 작품</b></p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    with tab4:
        st.header("연도별 장르 트렌드")

        all_genres = []
        for genres in df["genres_list"]:
            for genre in genres:
                all_genres.append(genre)

        genre_counts = Counter(all_genres)
        top10_genres = [genre for genre, _ in genre_counts.most_common(10)]

        year_genre_data = []
        for _, row in df.iterrows():
            year = row["release_year"]
            for genre in row["genres_list"]:
                if genre in top10_genres:
                    year_genre_data.append({"year": year, "genre": genre})

        year_genre_df = pd.DataFrame(year_genre_data)
        year_genre_summary = (
            year_genre_df.groupby(["year", "genre"]).size().reset_index(name="작품수")
        )

        fig2 = px.line(
            year_genre_summary,
            x="year",
            y="작품수",
            color="genre",
            title="연도별 TOP 10 장르 트렌드",
            markers=True,
            labels={"year": "연도", "작품수": "작품 수", "genre": "장르"},
        )
        fig2.update_layout(height=600)
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")
        st.subheader("특정 연도의 장르 분포")

        available_years = sorted([y for y in df["release_year"].dropna().unique()])
        selected_year = st.selectbox(
            "연도 선택", available_years, index=len(available_years) - 1
        )

        year_data = year_genre_df[year_genre_df["year"] == selected_year]
        year_genre_count = year_data["genre"].value_counts().head(10).reset_index()
        year_genre_count.columns = ["장르", "작품수"]

        year_str = selected_year.year if pd.notna(selected_year) else str(selected_year)

        fig4 = px.bar(
            year_genre_count,
            x="장르",
            y="작품수",
            title=f"{year_str}년 TOP 10 장르",
            color="작품수",
            color_continuous_scale="Viridis",
            text="작품수",
        )
        fig4.update_traces(texttemplate="%{text}개", textposition="outside")
        fig4.update_layout(showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)


# 메뉴 2
def show_menu2():
    st.header("📈 시간대 & 트렌드 분석")

    df = load_titles_csv()
    if df.empty:
        st.stop()

    # 장르 파싱
    def parse_genres(x):
        if pd.isna(x):
            return []
        if isinstance(x, list):
            return x
        if isinstance(x, str) and x.strip().startswith('['):
            try:
                return ast.literal_eval(x)
            except Exception:
                return []
        return []

    df['genres'] = df['genres'].apply(parse_genres)

    # 장르 분리 (explode)
    df_exploded = df.explode('genres')

    # 사용자 입력
    # release_year가 실수/문자일 수 있으니 안전 변환
    df_exploded['release_year'] = pd.to_numeric(df_exploded['release_year'], errors='coerce').astype('Int64')
    year_min = int(df_exploded['release_year'].dropna().min())
    year_max = int(df_exploded['release_year'].dropna().max())

    year_range = st.slider(
        "연도 범위 선택",
        min_value=year_min,
        max_value=year_max,
        value=(max(1900, year_min), min(1990, year_max))
    )

    select_type = st.selectbox("타입 선택", ["ALL", "MOVIE", "SHOW"])

    filtered = df_exploded[
        (df_exploded.release_year >= year_range[0]) &
        (df_exploded.release_year <= year_range[1])
    ]

    if select_type != "ALL":
        filtered = filtered[filtered['type'] == select_type]

    # 1. 연도별 작품 수 변화
    year_count = filtered.groupby('release_year').size().reset_index(name='count')
    fig1 = px.line(
        year_count, x='release_year', y='count',
        title='연도별 작품 수 변화', markers=True
    )
    st.plotly_chart(fig1, use_container_width=True)

    # 2. 연도별 평균 IMDb 점수 변화
    year_score = filtered.groupby('release_year')['imdb_score'].mean().reset_index()
    fig2 = px.line(
        year_score, x='release_year', y='imdb_score',
        title='연도별 IMDb 평균 평점', markers=True
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 3. 시대별 인기 장르 Top10
    genre_count = (
        filtered.groupby('genres')
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(10)
    )
    fig3 = px.bar(
        genre_count, x='count', y='genres',
        orientation='h', title='많이 제작된 Top10 장르'
    )
    st.plotly_chart(fig3, use_container_width=True)


# 메뉴 3
def show_menu3():
    st.header("🌍 제작국가 & 글로벌 분석")

    data = load_titles_csv()
    if data.empty:
        st.stop()

    st.subheader("📊 국가별 컨텐츠 수")
    data['production_countries'] = data['production_countries'].astype(str).str.replace(r"[\[\]' ]", '', regex=True)
    data['production_countries'] = data['production_countries'].str.split(',')
    data2 = data.explode('production_countries')
    data2 = data2[data2['production_countries'].fillna('') != '']

    result = data2.groupby('production_countries', as_index=False).agg(컨텐츠수=('production_countries', 'count'))
    st.dataframe(result, use_container_width=True)

    st.subheader("제작 컨텐츠 수 Top 10")
    result_top10 = result.sort_values('컨텐츠수', ascending=False).head(10)
    c = px.bar(data_frame=result_top10, x='production_countries', y='컨텐츠수')
    st.plotly_chart(c, use_container_width=True)

    # 분석 유형 선택
    type_sel = st.selectbox("분석 유형 선택", ['평점', '인기도'])
    option = st.selectbox("평점 분석 통계 선택", ['sum', 'mean', 'max', 'min'])

    if type_sel == '평점':
        data['production_countries'] = data['production_countries'].fillna('').astype(str)
        data['production_countries'] = data['production_countries'].str.replace(r"[\[\]' ]", '', regex=True)
        data['production_countries'] = data['production_countries'].str.split(',')
        data3 = data.explode('production_countries')
        data3 = data3[data3['production_countries'].fillna('') != '']

        result2 = data3.groupby('production_countries').agg(IMDb평점=('imdb_score', option),
                                                           TMDB평점=('tmdb_score', option))
        st.subheader("⭐ 제작국가별 평점 분석")
        st.dataframe(result2, use_container_width=True)

        st.subheader("IMDb 평균 평점 Top 10")
        result3 = (data3.groupby('production_countries', as_index=False)
                         .agg(평균IMDb평점=('imdb_score', 'mean'))
                         .sort_values('평균IMDb평점', ascending=False)
                         .head(10))
        c1 = px.bar(data_frame=result3, x='production_countries', y="평균IMDb평점")
        st.plotly_chart(c1, use_container_width=True)

        st.subheader("TMDB 평균 평점 Top 10")
        result4 = (data3.groupby('production_countries', as_index=False)
                         .agg(평균TMDB평점=('tmdb_score', 'mean'))
                         .sort_values('평균TMDB평점', ascending=False)
                         .head(10))
        c2 = px.bar(data_frame=result4, x='production_countries', y="평균TMDB평점")
        st.plotly_chart(c2, use_container_width=True)

    elif type_sel == '인기도':
        data = load_titles_csv()
        if data.empty:
            st.stop()

        data['production_countries'] = data['production_countries'].fillna('').astype(str)
        data['production_countries'] = data['production_countries'].str.replace(r"[\[\]' ]", '', regex=True)
        data['production_countries'] = data['production_countries'].str.split(',')
        data3 = data.explode('production_countries')
        data3 = data3[data3['production_countries'].fillna('') != '']

        result2 = data3.groupby('production_countries').agg(TMDB인기도=('tmdb_popularity', option))
        st.subheader("🔥 제작국가별 인기도 분석")
        st.dataframe(result2, use_container_width=True)

        st.subheader("국가별 평균 인기도 top10")
        result3 = (data3.groupby('production_countries', as_index=False)
                         .agg(평균인기도=('tmdb_popularity', 'mean'))
                         .sort_values('평균인기도', ascending=False)
                         .head(10))

        fig = plt.figure()
        sns.barplot(data=result3, x='production_countries', y="평균인기도", hue='production_countries')
        st.pyplot(fig)


# 메뉴 4
def show_menu4():
    st.header("🎬 장르별 평점 & 인기도 분석")

    df = load_titles_csv()
    if df.empty:
        st.stop()

    # 문자열 객체로 변경
    df['genres'] = df['genres'].apply(literal_eval)
    genre_df = df.explode('genres')

    input1 = st.selectbox("그룹", ["genres", "release_year", "production_countries"])
    input2 = st.selectbox("비교 기준", ["imdb_score", "tmdb_score", "tmdb_popularity"])
    input3 = st.selectbox("통계 방식", ["sum", "mean", "max", "min"])

    # 그룹별 통계
    result = (
        genre_df.groupby(input1)
        .agg(value=(input2, input3))
        .reset_index()
    )
    st.dataframe(result, use_container_width=True)

    st.subheader("장르별 평균 평점 / 인기도")
    genre_stats = (
        genre_df.groupby('genres')[['imdb_score', 'tmdb_score', 'tmdb_popularity']]
        .mean()
        .sort_values('tmdb_popularity', ascending=False)
    )

    st.dataframe(
        genre_stats.head(10).style.format({
            'imdb_score': '{:.2f}',
            'tmdb_score': '{:.2f}',
            'tmdb_popularity': '{:.2f}'
        }),
        use_container_width=True
    )

    st.subheader("장르별 TMDB 인기도 (Top 10)")
    fig, ax = plt.subplots(figsize=(8, 5))
    top10 = genre_stats.head(10)
    sns.barplot(y=top10.index, x=top10['tmdb_popularity'], palette='coolwarm', ax=ax)
    ax.set_xlabel('TMDB 인기도')
    ax.set_ylabel('장르')
    st.pyplot(fig)


# 라우팅

if selected == "장르 & 연령등급":
    show_menu1()
elif selected == "시간대 & 트렌드":
    show_menu2()
elif selected == "제작국가 & 글로벌":
    show_menu3()
elif selected == "평점 & 인기도":
    show_menu4()