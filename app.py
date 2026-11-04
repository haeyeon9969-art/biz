import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("🏬 지점별 매출 현황 대시보드")

# 데이터 불러오기
@st.cache_data
def load_data():
    # Sales.xlsx의 supermarket_sales_test 시트 로드
    df = pd.read_excel("Sales.xlsx", sheet_name="supermarket_sales_test")
    # 결측치 제거
    df = df.dropna()
    return df

try:
    df = load_data()

    # 사이드바 - 지점(Branch) 선택
    st.sidebar.header("필터 설정")
    branches = sorted(df["Branch"].unique())
    selected_branch = st.sidebar.selectbox("지점(Branch)을 선택하세요", branches)

    # 선택한 지점에 따른 데이터 필터링
    filtered_df = df[df["Branch"] == selected_branch]

    # 메트릭 계산 (열 이름은 일반적인 영문 기준으로 설정, 데이터셋 컬럼에 맞게 필요시 수정)
    # 총매출(Total), 평점(Rating)
    total_sales = filtered_df["Total"].sum()
    avg_sales = filtered_df["Total"].mean()
    avg_rating = filtered_df["Rating"].mean()

    # 3개의 컬럼 레이아웃으로 metric 표시
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="💰 총매출", value=f"${total_sales:,.2f}")
    with col2:
        st.metric(label="📈 평균 매출", value=f"${avg_sales:,.2f}")
    with col3:
        st.metric(label="⭐ 평균 평점", value=f"{avg_rating:.2f} / 10")

    st.markdown("---")

    # 상품 카테고리(Product line)별 평균 매출 계산
    category_sales = (
        filtered_df.groupby("Product line")["Total"]
        .mean()
        .reset_index()
        .rename(columns={"Total": "Average Sales"})
    )

    # Plotly를 이용한 막대그래프 시각화
    fig = px.bar(
        category_sales,
        x="Product line",
        y="Average Sales",
        title=f"[{selected_branch} 지점] 상품 카테고리별 평균 매출",
        labels={"Product line": "상품 카테고리", "Average Sales": "평균 매출 ($)"},
        text_auto=".2s",
        color="Product line"
    )
    fig.update_layout(showlegend=False)
    
    # 그래프 출력
    st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error("폴더 내에 'Sales.xlsx' 파일이 존재하지 않습니다. 파일을 업로드해 주세요.")
except Exception as e:
    st.error(f"에러가 발생했습니다: {e}")
