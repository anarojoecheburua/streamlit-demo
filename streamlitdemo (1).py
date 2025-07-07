import streamlit as st
import pandas as pd
import numpy as np
import random
import time

# ─── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Streamlit Tutorial",
    page_icon="👋",
    layout="wide",
)

# ─── Title & Introduction ─────────────────────────────────────────────────────
st.title("Hello 👋")
st.markdown(
    """
    Welcome to this Streamlit Tutorial!  
    Explore interactive widgets, charts, DataFrames, and even build a simple chat interface.  
    This guide shows you how to combine Streamlit’s core APIs to create engaging apps.
    """
)

st.divider()

# ─── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.markdown(
    "<div style='text-align: center; font-size: 20px;'>Made with love by Ana</div>"
    "<div style='text-align: center; font-size: 20px;'>🤍</div>",
    unsafe_allow_html=True
)


# ─── Main Tabs for Each Section ────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🎈 Balloons", 
    "📊 Charts", 
    "🗃️ Data Editor", 
    "💬 Chatbot"
])

# ─── 1. Balloons Example ────────────────────────────────────────────────────────
with tab1:
    st.header("🎈 Interactive surprise")
    st.markdown("Press the button below to release a burst of balloons on the screen.")
    if st.button("Send balloons!"):
        st.balloons()

# ─── 2. Interactive Charts ─────────────────────────────────────────────────────
with tab2:
    st.header("📊 Interactive data visualisation")
    st.markdown(
        """
        Streamlit makes it super easy to connect widgets to charts.  
        - **Select users** whose data you want to plot  
        - **Toggle** a rolling average transformation  
        - **View** as a line chart or raw table
        """
    )

    all_users = ["Ana", "Maria", "Willow"]
    users = st.multiselect("Select users", all_users, default=all_users)
    rolling = st.checkbox("Apply 7-day rolling average", value=False)

    np.random.seed(42)
    df = pd.DataFrame(np.random.randn(20, len(users)), columns=users)
    if rolling:
        df = df.rolling(window=7).mean().dropna()

    chart_tab, table_tab = st.tabs(["Line Chart", "Data Table"])
    chart_tab.line_chart(df, height=300)
    table_tab.dataframe(df, height=300, use_container_width=True)

# ─── 3. Data Editor & Large Tables ─────────────────────────────────────────────
with tab3:
    st.header("🗃️ DataFrame explorer & editor")
    st.markdown(
        """
        Streamlit can handle large tables and even let users edit data in-place.  
        - **Slider** to pick row count  
        - **Checkbox** to toggle edit mode  
        - **Custom columns** like images & progress bars
        """
    )

    num_rows = st.slider("Rows to generate", min_value=1, max_value=10_000, value=500)
    np.random.seed(42)
    data = pd.DataFrame({
        "Preview": [f"https://picsum.photos/400/200?lock={i}" for i in range(num_rows)],
        "Views": np.random.randint(0, 1000, size=num_rows),
        "Active": np.random.choice([True, False], size=num_rows),
        "Category": np.random.choice(["🤖 LLM", "📊 Data", "⚙️ Tool"], size=num_rows),
        "Progress": np.random.randint(1, 100, size=num_rows),
    })

    col_config = {
        "Preview": st.column_config.ImageColumn(),
        "Progress": st.column_config.ProgressColumn(),
    }

    if st.checkbox("Enable editing"):
        st.data_editor(data, column_config=col_config, use_container_width=True)
    else:
        st.dataframe(data, column_config=col_config, use_container_width=True)

# ─── 4. Simple Chat UI ─────────────────────────────────────────────────────────
with tab4:
    st.header("💬 Build a chatbot")
    st.markdown(
        """
        Simulate a chat interface in Streamlit.  
        This demo uses canned responses—swap in an LLM for real conversations!
        """
    )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Let's start chatting! 👇"}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Type your message…")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            reply = random.choice([
                "Hello there! How can I assist you today?",
                "Hi! What would you like to talk about?",
                "Need help with Streamlit or something else?"
            ])
            text = ""
            for word in reply.split():
                text += word + " "
                time.sleep(0.05)
                placeholder.markdown(text + "▌")
            placeholder.markdown(text)

        st.session_state.messages.append({"role": "assistant", "content": text})

