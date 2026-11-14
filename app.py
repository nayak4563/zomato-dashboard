import base64
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

px.defaults.template = "plotly_dark"
px.defaults.color_discrete_sequence = ["#e23744", "#f18b91", "#b91f31", "#f7c5c8", "#7d2634"]

st.set_page_config(
    page_title="Zomato Analytics Dashboard",
    page_icon="assets/zomato-mark.svg",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- Styling --------------------
st.markdown("""
<style>
    :root { --zomato: #e23744; --zomato-dark: #b91f31; --ink: #fff4f2; --muted: #c3afb2; --canvas: #170d10; --line: #45272e; }
    html, body, [class*="css"] { font-family: 'DM Sans', 'Segoe UI', sans-serif; }
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #170d10;
        background-image:
            radial-gradient(ellipse 820px 600px at 100% 0%, rgba(226,55,68,.2), transparent 72%),
            radial-gradient(ellipse 700px 520px at 0% 82%, rgba(122,28,43,.22), transparent 74%),
            radial-gradient(circle at 1px 1px, rgba(255,209,212,.055) 1px, transparent 1.5px),
            linear-gradient(145deg, #170d10 0%, #1d1014 48%, #241116 100%);
        background-size: auto, auto, 30px 30px, auto;
        background-attachment: fixed;
        color: var(--ink);
    }
    [data-testid="stMain"], .main { background: transparent !important; }
    [data-testid="stHeader"] { background: rgba(23,13,16,.9); }
    [data-testid="stSidebar"] { background: #1d1216; border-right: 1px solid #45272e; }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: var(--ink); }
    .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1500px; }
    h1, h2, h3 { font-family: 'DM Sans', 'Segoe UI', sans-serif; color: var(--ink); letter-spacing: -.035em; }
    h1 { font-size: clamp(2rem, 3vw, 2.7rem) !important; font-weight: 800 !important; }
    h2 { font-size: 1.45rem !important; font-weight: 750 !important; margin-top: 1.6rem !important; }
    h3 { font-size: 1.1rem !important; font-weight: 700 !important; }
    p, .stCaption { color: var(--muted); }
    .brand-row { display:flex; align-items:center; gap:14px; margin-bottom:6px; }
    .brand-mark { width:48px; height:48px; flex:0 0 48px; border-radius:15px; background:#e23744; display:grid; place-items:center; color:white; font-size:29px; font-weight:800; box-shadow:0 8px 20px #e2374433; }
    .brand-word { color:#e23744; font-size:18px; font-weight:800; letter-spacing:-.06em; }
    .eyebrow { text-transform:uppercase; letter-spacing:.13em; font-size:11px; font-weight:700; color:#e23744; margin-bottom:4px; }
    .hero { position:relative; overflow:hidden; display:flex; align-items:center; gap:20px; margin:2px 0 14px; padding:30px 34px; border-radius:24px; color:#fff; background:linear-gradient(112deg,#b91f31 0%,#e23744 62%,#f15c66 100%); box-shadow:0 16px 38px rgba(185,31,49,.2); }
    .hero:after { content:""; position:absolute; width:330px; height:330px; right:7%; top:-195px; border:1px solid rgba(255,255,255,.18); border-radius:50%; box-shadow:0 0 0 32px rgba(255,255,255,.045),0 0 0 68px rgba(255,255,255,.035); }
    .hero .brand-mark { width:62px; height:62px; flex-basis:62px; border-radius:19px; color:#e23744; background:#fff; font-size:37px; box-shadow:0 8px 25px rgba(80,0,10,.16); }
    .hero-logo-wrap { position:relative; z-index:1; flex:0 0 174px; display:flex; align-items:center; }
    .hero-logo { display:block; width:100%; height:auto; }
    .sidebar-logo-wrap { width:112px; margin:7px 0 15px; }
    .sidebar-logo { display:block; width:100%; height:auto; }
    .hero-copy { position:relative; z-index:1; }
    .hero-word { color:#fff; font-size:14px; line-height:1; font-weight:800; letter-spacing:-.04em; margin-bottom:7px; }
    .hero h1 { color:#fff !important; font-size:clamp(1.8rem,3vw,2.45rem) !important; line-height:1.1; margin:0 0 8px; letter-spacing:-.045em; }
    .hero p { color:rgba(255,255,255,.86); margin:0; font-size:14px; }
    .hero-tags { display:flex; flex-wrap:wrap; gap:8px; margin-top:15px; }
    .hero-tag { padding:5px 10px; border:1px solid rgba(255,255,255,.3); border-radius:999px; color:white; font-size:11px; font-weight:650; background:rgba(255,255,255,.1); }
    .hero-image-wrap { position:relative; z-index:1; flex:0 1 340px; margin-left:auto; padding:6px; border-radius:17px; background:#fff; box-shadow:0 12px 28px rgba(65,0,10,.25); }
    .hero-image { display:block; width:100%; aspect-ratio:2/1; object-fit:cover; border-radius:12px; }
    .chart-nav { position:sticky; top:0; z-index:999; display:flex; align-items:center; gap:8px; overflow-x:auto; white-space:nowrap; margin:18px 0 26px; padding:10px 12px; background:rgba(38,21,26,.96); border:1px solid #543039; border-radius:14px; box-shadow:0 8px 28px #08040655; scrollbar-width:thin; }
    .chart-nav a { display:inline-block; padding:8px 13px; border-radius:9px; color:#e4d1d3 !important; text-decoration:none !important; font-size:13px; font-weight:650; transition:background .15s,color .15s; }
    .chart-nav a:hover { background:#49212a; color:#ff8b93 !important; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] hr { border-color:var(--line); }
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { color:#51484b; font-weight:650; }
    [data-baseweb="select"] > div, [data-baseweb="input"] > div { background:#28191e; border-color:#543039; border-radius:10px; }
    [data-baseweb="select"] > div:focus-within, [data-baseweb="input"] > div:focus-within { border-color:#e23744; box-shadow:0 0 0 1px #e23744; }
    [data-testid="stSlider"] [role="slider"] { background:#e23744; border-color:#e23744; }
    [data-testid="stMetric"] {
        background: #28191e; border: 1px solid #45272e; padding: 19px 20px;
        border-radius: 16px; box-shadow: 0 8px 24px #08040630; min-height: 112px;
    }
    [data-testid="stMetricLabel"] { color:#c3afb2; font-weight:600; }
    [data-testid="stMetricValue"] { color:#fff4f2; font-weight:800; }
    [data-testid="stPlotlyChart"] { background:#24171b; border:1px solid #45272e; border-radius:16px; padding:10px 10px 0; box-shadow:0 8px 24px #08040630; }
    div[data-testid="stFileUploader"] section { background:#28191e; border:1px dashed #9d4551; border-radius:14px; }
    div.stButton > button, div.stDownloadButton > button { border-radius:10px; font-weight:650; border-color:#e23744; color:#ff969d; background:#28191e; }
    div.stButton > button[kind="primary"] { background:#e23744; border-color:#e23744; }
    div.stDownloadButton > button:hover, div.stButton > button:hover { border-color:#b91f31; color:#b91f31; }
    div.stButton > button[kind="primary"]:hover { background:#b91f31; color:#fff; }
    [data-testid="stDataFrame"], [data-testid="stTable"] { border:1px solid #45272e; border-radius:12px; overflow:hidden; }
    [data-testid="stExpander"] { background:#24171b; border:1px solid #45272e; border-radius:14px; }
    [data-testid="stAlert"] { border-radius:12px; }
    [data-testid="stAlert"][kind="info"] { background:#351c23; }
    hr { border-color:#eee7e4; }
    @media (max-width: 700px) { .block-container { padding:1rem 1rem 2rem; } .hero-image-wrap { display:none; } .hero { padding:24px 20px; } }
</style>
""", unsafe_allow_html=True)

hero_image_path = Path(__file__).with_name("SEBI-grants-approval-to-Zomatos-blockbuster-IPO-1024x512.jpg")
hero_image_data = base64.b64encode(hero_image_path.read_bytes()).decode("ascii")
logo_image_path = Path(__file__).parent / "assets" / "zomato-wordmark-white.png"
logo_image_data = base64.b64encode(logo_image_path.read_bytes()).decode("ascii")
sidebar_logo_path = Path(__file__).parent / "assets" / "zomato-wordmark.png"
sidebar_logo_data = base64.b64encode(sidebar_logo_path.read_bytes()).decode("ascii")

st.markdown(f"""
<section class="hero">
  <div class="hero-logo-wrap"><img class="hero-logo" src="data:image/png;base64,{logo_image_data}" alt="Zomato"></div>
  <div class="hero-copy">
    <h1>Restaurant analytics</h1>
    <p>Discover the restaurants, ratings and flavors shaping every city.</p>
    <div class="hero-tags"><span class="hero-tag">DINING</span><span class="hero-tag">DELIVERY</span><span class="hero-tag">CUISINES</span><span class="hero-tag">₹ PRICES</span></div>
  </div>
  <div class="hero-image-wrap"><img class="hero-image" src="data:image/jpeg;base64,{hero_image_data}" alt="Zomato food delivery rider illustration"></div>
</section>
""", unsafe_allow_html=True)
st.markdown("""
<nav class="chart-nav" aria-label="Dashboard sections">
  <a href="#restaurant-performance">Restaurant performance</a>
  <a href="#customer-ratings-and-engagement">Ratings &amp; engagement</a>
  <a href="#cuisine-and-city-insights">Cuisine &amp; cities</a>
  <a href="#food-item-and-price-insights">Food &amp; prices</a>
</nav>
""", unsafe_allow_html=True)

# -------------------- Data loading --------------------
@st.cache_data
def load_data(file_bytes):
    from io import BytesIO
    data = pd.read_csv(BytesIO(file_bytes))
    data.columns = data.columns.astype(str).str.strip()

    # Convert fields used in analysis to numeric values.
    numeric_columns = [
        "Dining Rating", "Delivery Rating", "Dining Votes",
        "Delivery Votes", "Votes", "Prices"
    ]
    for col in numeric_columns:
        if col in data.columns:
            cleaned = (
                data[col].astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("₹", "", regex=False)
                .str.replace("Rs.", "", regex=False)
                .str.strip()
            )
            data[col] = pd.to_numeric(cleaned, errors="coerce")

    # Match the main cleaning approach used in the accompanying notebook.
    # Missing rating/vote values are filled with their column median.
    for col in ["Dining Rating", "Delivery Rating", "Dining Votes", "Delivery Votes"]:
        if col in data.columns and data[col].notna().any():
            data[col] = data[col].fillna(data[col].median())

    # In the notebook, zero delivery ratings are treated as missing values.
    if "Delivery Rating" in data.columns:
        positive = data.loc[data["Delivery Rating"] > 0, "Delivery Rating"]
        if not positive.empty:
            data["Delivery Rating"] = data["Delivery Rating"].replace(0, positive.median())

    return data


with st.sidebar:
    st.markdown(
        f'<div class="sidebar-logo-wrap"><img class="sidebar-logo" src="data:image/png;base64,{sidebar_logo_data}" alt="Zomato"></div>',
        unsafe_allow_html=True,
    )
    st.subheader("Dashboard controls")
    uploaded_file = st.file_uploader("Upload your Zomato CSV file", type=["csv"])
    st.markdown("---")
    st.caption("Upload the CSV used in your EDA notebook. The dashboard will update automatically.")

if uploaded_file is None:
    st.info("Please upload your **zomato_dataset.csv** file in the sidebar to open the dashboard.")
    st.markdown("""
    ### Expected columns
    `Restaurant Name`, `Dining Rating`, `Delivery Rating`, `Dining Votes`,
    `Delivery Votes`, `Cuisine`, `Place Name`, `City`, `Item Name`, `Votes`, `Prices`
    """)
    st.stop()

try:
    df = load_data(uploaded_file.getvalue())
except Exception as exc:
    st.error(f"Could not read this CSV file: {exc}")
    st.stop()

if df.empty:
    st.warning("The uploaded CSV contains no rows.")
    st.stop()

# Use only columns that are actually available in the uploaded file.
required_for_dashboard = ["Restaurant Name", "City", "Cuisine"]
missing = [c for c in required_for_dashboard if c not in df.columns]
if missing:
    st.error("The CSV is missing these required columns: " + ", ".join(missing))
    st.stop()

# -------------------- Sidebar filters --------------------
with st.sidebar:
    st.subheader("Explore data")
    cities = sorted(df["City"].dropna().astype(str).unique().tolist())
    cuisines = sorted(df["Cuisine"].dropna().astype(str).unique().tolist())

    selected_cities = st.multiselect("Select city", cities, default=cities)
    selected_cuisines = st.multiselect("Select cuisine", cuisines, default=cuisines)

    restaurant_names = sorted(df["Restaurant Name"].dropna().astype(str).unique().tolist())
    selected_restaurants = st.multiselect(
        "Select restaurant (optional)", restaurant_names, default=[]
    )

    if "Prices" in df.columns and df["Prices"].notna().any():
        min_price = float(df["Prices"].min())
        max_price = float(df["Prices"].max())
        if min_price < max_price:
            price_range = st.slider(
                "Price range",
                min_value=min_price,
                max_value=max_price,
                value=(min_price, max_price),
            )
        else:
            price_range = (min_price, max_price)
    else:
        price_range = None

filtered = df[
    df["City"].astype(str).isin(selected_cities)
    & df["Cuisine"].astype(str).isin(selected_cuisines)
].copy()

if selected_restaurants:
    filtered = filtered[filtered["Restaurant Name"].astype(str).isin(selected_restaurants)]

if price_range is not None and "Prices" in filtered.columns:
    filtered = filtered[
        filtered["Prices"].isna()
        | filtered["Prices"].between(price_range[0], price_range[1])
    ]

if filtered.empty:
    st.warning("No records match the selected filters. Please change your filters.")
    st.stop()

# -------------------- KPI cards --------------------
def mean_if_available(frame, column):
    if column in frame.columns and frame[column].notna().any():
        return frame[column].mean()
    return None


def style_chart(fig, height, **layout):
    fig.update_layout(
        height=height,
        font=dict(family="DM Sans, Segoe UI, sans-serif", color="#eadbdd", size=12),
        title_font=dict(family="DM Sans, Segoe UI, sans-serif", color="#fff4f2", size=16),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#24171b",
        margin=dict(l=16, r=18, t=60, b=22),
        **layout,
    )
    fig.update_xaxes(showgrid=True, gridcolor="#432a31", zerolinecolor="#63343e", tickfont_color="#cdbabd", title_font_color="#d9c6c9")
    fig.update_yaxes(showgrid=False, zerolinecolor="#63343e", tickfont_color="#cdbabd", title_font_color="#d9c6c9")
    return fig

total_restaurants = filtered["Restaurant Name"].nunique()
total_cities = filtered["City"].nunique()
avg_dining = mean_if_available(filtered, "Dining Rating")
avg_delivery = mean_if_available(filtered, "Delivery Rating")
avg_price = mean_if_available(filtered, "Prices")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Restaurants", f"{total_restaurants:,}")
k2.metric("Cities", f"{total_cities:,}")
k3.metric("Avg. dining rating", f"{avg_dining:.2f}" if avg_dining is not None else "N/A")
k4.metric("Avg. delivery rating", f"{avg_delivery:.2f}" if avg_delivery is not None else "N/A")
k5.metric("Avg. price", f"₹{avg_price:,.0f}" if avg_price is not None else "N/A")

st.markdown("---")

# -------------------- Restaurant performance --------------------
st.subheader("Restaurant performance")
left, right = st.columns(2)

with left:
    if "Dining Rating" in filtered.columns:
        top_dining = (
            filtered.groupby("Restaurant Name", as_index=False)["Dining Rating"]
            .mean().dropna().nlargest(10, "Dining Rating")
        )
        fig = px.bar(
            top_dining.sort_values("Dining Rating"),
            x="Dining Rating", y="Restaurant Name", orientation="h",
            title="Top 10 restaurants by average dining rating",
            labels={"Dining Rating": "Average dining rating", "Restaurant Name": ""},
            color="Dining Rating", color_continuous_scale="Reds",
        )
        style_chart(fig, 420, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Dining Rating column not found.")

with right:
    if "Delivery Rating" in filtered.columns:
        top_delivery = (
            filtered.groupby("Restaurant Name", as_index=False)["Delivery Rating"]
            .mean().dropna().nlargest(10, "Delivery Rating")
        )
        fig = px.bar(
            top_delivery.sort_values("Delivery Rating"),
            x="Delivery Rating", y="Restaurant Name", orientation="h",
            title="Top 10 restaurants by average delivery rating",
            labels={"Delivery Rating": "Average delivery rating", "Restaurant Name": ""},
            color="Delivery Rating", color_continuous_scale="Reds",
        )
        style_chart(fig, 420, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Delivery Rating column not found.")

# -------------------- Ratings and votes --------------------
st.subheader("Customer ratings and engagement")
left, right = st.columns(2)

with left:
    if {"Dining Rating", "Delivery Rating"}.issubset(filtered.columns):
        scatter_df = filtered.dropna(subset=["Dining Rating", "Delivery Rating"])
        fig = px.scatter(
            scatter_df, x="Dining Rating", y="Delivery Rating",
            color="Cuisine", hover_name="Restaurant Name",
            title="Dining rating vs delivery rating",
            labels={"Dining Rating": "Dining rating", "Delivery Rating": "Delivery rating"},
            opacity=0.65,
        )
        style_chart(fig, 430)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Dining Rating and Delivery Rating columns are needed for this chart.")

with right:
    if "Dining Votes" in filtered.columns:
        top_votes = (
            filtered.groupby("Restaurant Name", as_index=False)["Dining Votes"]
            .sum().nlargest(10, "Dining Votes")
        )
        fig = px.bar(
            top_votes.sort_values("Dining Votes"),
            x="Dining Votes", y="Restaurant Name", orientation="h",
            title="Top 10 restaurants by dining votes",
            labels={"Dining Votes": "Total dining votes", "Restaurant Name": ""},
            color="Dining Votes", color_continuous_scale="Reds",
        )
        style_chart(fig, 430, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Dining Votes column not found.")

# -------------------- Cuisine and city insights --------------------
st.subheader("Cuisine and city insights")
left, right = st.columns(2)

with left:
    cuisine_counts = filtered["Cuisine"].value_counts().head(10).rename_axis("Cuisine").reset_index(name="Records")
    fig = px.bar(
        cuisine_counts.sort_values("Records"),
        x="Records", y="Cuisine", orientation="h",
        title="Top 10 most common cuisines",
        labels={"Records": "Number of records", "Cuisine": ""},
        color="Records", color_continuous_scale="Reds",
    )
    style_chart(fig, 430, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with right:
    city_counts = (
        filtered.groupby("City")["Restaurant Name"].nunique()
        .sort_values(ascending=False).head(10)
        .rename("Restaurants").reset_index()
    )
    fig = px.bar(
        city_counts.sort_values("Restaurants"),
        x="Restaurants", y="City", orientation="h",
        title="Top 10 cities by number of restaurants",
        labels={"Restaurants": "Unique restaurants", "City": ""},
        color="Restaurants", color_continuous_scale="Reds",
    )
    style_chart(fig, 430, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# -------------------- Food item and price insights --------------------
st.subheader("Food item and price insights")
left, right = st.columns(2)

with left:
    if {"Item Name", "Votes"}.issubset(filtered.columns):
        popular_items = (
            filtered.groupby("Item Name", as_index=False)["Votes"]
            .sum().nlargest(10, "Votes")
        )
        fig = px.bar(
            popular_items.sort_values("Votes"),
            x="Votes", y="Item Name", orientation="h",
            title="Top 10 popular food items",
            labels={"Votes": "Total votes", "Item Name": ""},
            color="Votes", color_continuous_scale="Reds",
        )
        style_chart(fig, 430, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Item Name and Votes columns are needed for this chart.")

with right:
    if "Prices" in filtered.columns:
        cuisine_prices = (
            filtered.groupby("Cuisine", as_index=False)["Prices"]
            .mean().dropna().nlargest(10, "Prices")
        )
        fig = px.bar(
            cuisine_prices.sort_values("Prices"),
            x="Prices", y="Cuisine", orientation="h",
            title="10 cuisines with highest average price",
            labels={"Prices": "Average price (₹)", "Cuisine": ""},
            color="Prices", color_continuous_scale="Reds",
        )
        style_chart(fig, 430, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Prices column not found.")

# -------------------- Data preview and download --------------------
with st.expander("View filtered data"):
    st.dataframe(filtered, use_container_width=True, height=350)
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered data as CSV",
        data=csv,
        file_name="zomato_filtered_data.csv",
        mime="text/csv",
    )

st.caption("Note: Restaurant rating charts use average ratings, not sums. Filters apply to all charts and KPI cards.")
