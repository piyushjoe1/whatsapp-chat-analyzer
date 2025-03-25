# app.py
import streamlit as st
import chat_helper
import chat_processor
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")
st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp Chat File (txt)")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = chat_processor.chatprocess(data)

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Analyze messages for", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_links = chat_helper.fetch_stats(selected_user, df)
        st.title("📊 Chat Summary")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Messages", num_messages)
        with col2:
            st.metric("Total Words", words)
        with col3:
            st.metric("Media Shared", num_media_messages)
        with col4:
            st.metric("Links Shared", num_links)

        st.title("📅 Monthly & Daily Timeline")
        timeline = chat_helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        daily_timeline = chat_helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        st.title("🗓 Activity Analysis")
        col1, col2 = st.columns(2)
        with col1:
            busy_day = chat_helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            st.pyplot(fig)
        with col2:
            busy_month = chat_helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            st.pyplot(fig)

        user_heatmap = chat_helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        sns.heatmap(user_heatmap, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

        if selected_user == 'Overall':
            st.title("🏆 Most Active Users")
            x, new_df = chat_helper.most_busy_users(df)
            fig, ax = plt.subplots()
            ax.bar(x.index, x.values, color='red')
            st.pyplot(fig)
            st.dataframe(new_df)

        st.title("☁️ WordCloud & Common Words")
        df_wc = chat_helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc, interpolation='bilinear')
        st.pyplot(fig)

        most_common_df = chat_helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='blue')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        st.title("😀 Emoji Analysis")
        emoji_df = chat_helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(5), labels=emoji_df[0].head(5), autopct="%0.2f%%",
                   colors=['gold', 'blue', 'red', 'green', 'purple'])
            st.pyplot(fig)
