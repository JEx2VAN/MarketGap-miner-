
import streamlit as st
import pandas as pd
import plotly.express as px

#Config 
st.set_page_config(layout="wide", page_title="MarketGap Miner")

#File Paths (adjust to your Drive folder) 
PROJECT_PATH = '/content/drive/MyDrive/MarketGapMiner'
SCORES_FILE = f'{PROJECT_PATH}/gap_scores.csv'
REVIEWS_FILE = f'{PROJECT_PATH}/pain_reviews.csv'

#  Load Data
@st.cache_data
def load_data():
    """
    Loads the gap scores and review data from the CSV files.
    """
    try:
        df_scores = pd.read_csv(SCORES_FILE)
        df_reviews = pd.read_csv(REVIEWS_FILE)
        return df_scores, df_reviews
    except FileNotFoundError:
        st.error(f"ERROR: Data files not found. Make sure '{SCORES_FILE}' and '{REVIEWS_FILE}' exist.")
        return None, None

# Main App Logic
def main():
    df_scores, df_reviews = load_data()

    if df_scores is None or df_reviews is None:
        st.stop()

    # Header
    st.title("🚀 MarketGap Miner")
    st.markdown("This dashboard analyzes competitor reviews to find the biggest feature gaps and market opportunities.")

    # 1. Top Opportunities Chart
    st.header("🏆 Top Market Opportunities")
    st.markdown("This chart ranks complaint topics by the **Gap Score**. A high score means many people are very angry about this feature across multiple competitors.")

    fig = px.bar(
        df_scores,
        x='topic_name',
        y='Gap_Score',
        color='topic_name',
        title="Ranked Feature Gaps (Higher is a Bigger Opportunity)",
        labels={'topic_name': 'Complaint Topic', 'Gap_Score': 'Gap Score'}
    )
    fig.update_layout(xaxis_title=None, yaxis_title="Gap Score (Higher = More Pain)")
    st.plotly_chart(fig, use_container_width=True)

    # 2. Drill-Down "The Evidence"
    st.header("🔍 Drill-Down: The Evidence")
    st.markdown("Select a topic or competitor to read the *actual reviews* that generated the score.")

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        # Get topics from the scores file so it's pre-filtered
        topic_list = ["All Topics"] + df_scores['topic_name'].unique().tolist()
        selected_topic = st.selectbox("Filter by Topic:", topic_list)

    with col2:
        product_list = ["All Products"] + df_reviews['product'].unique().tolist()
        selected_product = st.selectbox("Filter by Product:", product_list)

    # Filter the "evidence" dataframe
    df_filtered_reviews = df_reviews.copy()

    if selected_topic != "All Topics":
        df_filtered_reviews = df_filtered_reviews[df_filtered_reviews['topic_name'] == selected_topic]

    if selected_product != "All Products":
        df_filtered_reviews = df_filtered_reviews[df_filtered_reviews['product'] == selected_product]

    # Display the filtered reviews
    st.dataframe(
        df_filtered_reviews[['product', 'review_text', 'sentiment_score', 'topic_name']],
        height=400,
        use_container_width=True
    )
    st.success(f"Showing {len(df_filtered_reviews)} of {len(df_reviews)} total pain point reviews.")

if __name__ == "
