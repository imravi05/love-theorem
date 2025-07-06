# File: app.py

import streamlit as st
from chat_parser import parse_chat
from predictor import compute_metrics, calculate_interest_score
from visualizer import plot_message_frequency, plot_sender_distribution
from utils import get_top_senders

# App configuration
st.set_page_config(page_title="Love Theorem 💘", layout="centered")
st.title("🔮 Love Theorem – Interest Predictor")

# File uploader
uploaded_file = st.file_uploader("Upload your WhatsApp chat (.txt file)", type=["txt"])

if uploaded_file:
    with st.spinner("Analyzing your love life... 💬💘"):
        # Parse chat
        df = parse_chat(uploaded_file)

        # Exit if empty
        if df.empty:
            st.error("❌ Chat could not be parsed or contains no valid messages.")
            st.stop()

        # Get sender names
        user, crush = get_top_senders(df)
        st.success(f"✅ Detected chat between **{user}** and **{crush}**")

        # Compute metrics and interest score
        metrics = compute_metrics(df, user_name=user, crush_name=crush)
        score = calculate_interest_score(metrics)

        # Display result
        st.header("❤️ Interest Score")
        st.metric(label="Prediction", value=f"{score}%", delta="More talk = More sparks!")

        # Show metrics
        st.markdown("### 📊 Chat Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Reply Time", f"{metrics['avg_reply_time_min']} min")
        col2.metric("Msgs/Day", f"{metrics['avg_messages_per_day']}")
        col3.metric("Convo Length", f"{metrics['avg_convo_length']} turns")

        # Graphs
        st.markdown("---")
        st.subheader("🧁 Message Split")
        st.pyplot(plot_sender_distribution(df))

        st.subheader("📅 Messages Per Day")
        st.pyplot(plot_message_frequency(df))

        # Footer
        st.markdown("---")
        st.caption("Disclaimer: This tool analyzes message patterns only and is for fun purposes 😊. Real feelings need real conversations.")
