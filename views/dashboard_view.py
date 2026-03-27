import streamlit as st
import pandas as pd
import plotly.express as px
from config.db_config import get_connection
from datetime import datetime

# -----------------------------
# FETCH DATA
# -----------------------------
def fetch_usecase():
    conn = get_connection()
    query = """
    SELECT 
        id,
        waba_number,
        mobile_number,
        recommend,
        impact,
        efficacy,
        performance,
        teaming,
        improve,
        created_at
    FROM usecase
    WHERE is_active = 1
    ORDER BY id DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    df["date"] = pd.to_datetime(df["created_at"]).dt.date
    df["time"] = pd.to_datetime(df["created_at"]).dt.time
    return df

# -----------------------------
# DASHBOARD
# -----------------------------
def show_dashboard():
    st.set_page_config(
        page_title="Wisely AI Feedback Survey Analytical Dashboard",
        layout="wide",
        page_icon="🚀"
    )

    # -----------------------------
    # Background & Style
    # -----------------------------
    st.markdown(
        """
        <style>
        /* Background Image with gradient overlay */
        .stApp {
            background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                        url('https://d2q4iodazzzt8b.cloudfront.net/tanlanps_1773206728.png');
            background-size: cover;
            background-position: center;
            min-height: 100vh;
            width: 100%;
            color: #ffffff;
        }


        /* Sidebar transparency */
        section[data-testid="stSidebar"] {
            background: rgba(0,0,0,0.45) !important;
            backdrop-filter: blur(1px);
        }
         

        /* Dataframe styling */
        .stDataFrame div.row_widget.stDataFrame {
            background: rgba(255, 255, 255, 0.05);
        }

        /* Hide Streamlit footer */
        footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("🚀 Wisely AI Feedback Survey Analytical Dashboard")

    df = fetch_usecase()
    if df.empty:
        st.warning("No records found")
        return

    # -----------------------------
    # Sidebar Filter
    # -----------------------------
    st.sidebar.header("Filters")

    # Mobile filter
    mobile_list = ["All"] + sorted(df["mobile_number"].unique())
    mobile_filter = st.sidebar.selectbox("Mobile Number", mobile_list)
    if mobile_filter != "All":
        df = df[df["mobile_number"] == mobile_filter]

    # Date range filter
    min_date = df["date"].min()
    max_date = df["date"].max()
    start_date, end_date = st.sidebar.date_input(
        "Select Date Range",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    if isinstance(start_date, datetime):
        start_date = start_date.date()
    if isinstance(end_date, datetime):
        end_date = end_date.date()

    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

    # -----------------------------
    # KPI CARDS
    # -----------------------------
    st.subheader("✨ Key Metrics")
    kpi1, kpi2 = st.columns(2)
    kpi_style = "background: rgba(255,255,255,0.1); padding: 20px; border-radius:15px; text-align:center;"
    kpi1.markdown(f"<div style='{kpi_style}'><h3>{len(df)}</h3><p>Total Records</p></div>", unsafe_allow_html=True)
    kpi2.markdown(f"<div style='{kpi_style}'><h3>{df.mobile_number.nunique()}</h3><p>Users</p></div>", unsafe_allow_html=True)

    # -----------------------------
    # Table View
    # -----------------------------
    st.subheader("📋 Usecase Records")
    table_df = df[[
        "id","waba_number","mobile_number","recommend","impact","efficacy",
        "performance","teaming","improve","date","time"
    ]]
    st.dataframe(table_df, use_container_width=True)

    # -----------------------------
    # Rating Analysis
    # -----------------------------
    st.subheader("🌟 Rating Analysis")
    rating_cols = ["recommend","impact","efficacy","performance","teaming"]

    # Normalize ratings
    rating_map = {"extremely":3,"highly":3,"fairly":2,"not":1}
    for col in rating_cols:
        df[col] = df[col].astype(str).str.lower().str.strip()
        df[col+"_score"] = df[col].map(rating_map).fillna(0)

    # Plot interactive bar charts
    for col in rating_cols:
        st.markdown(f"### {col.capitalize()} Ratings")
        count_df = df[col].value_counts(dropna=False).reset_index()
        count_df.columns = ["rating", "count"]  # safe column names

        fig = px.bar(
            count_df,
            x="rating",
            y="count",
            color="rating",
            text="count",
            color_discrete_sequence=px.colors.sequential.Viridis,
            title=f"{col.capitalize()} Ratings"
        )
        fig.update_traces(
            textposition="outside",
            marker_line_width=1.5,
            marker_line_color="black",
        )
        fig.update_layout(
            uniformtext_minsize=12,
            uniformtext_mode="hide",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff")
        )
        st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # Improvement Suggestions
    # -----------------------------
    st.subheader("📝 Improvement Suggestions")
    improve_df = df[df["improve"].notna() & (df["improve"] != "-")]
    if not improve_df.empty:
        st.dataframe(improve_df[["mobile_number","improve"]], use_container_width=True)
    else:
        st.info("No improvement suggestions available")