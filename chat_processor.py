import os
import re
import pandas as pd
from textblob import TextBlob
import seaborn as sns
import matplotlib.pyplot as plt


# 🔹 Correct the file path (Replace "chat.txt" with your actual file name)
file_path = r"C:\Users\Piyush Joshi\PycharmProjects\firstprog\pythonProject\WhatsApp Chat Analyzer\chat.txt"

# 🔹 Check if file exists
if not os.path.isfile(file_path):
    print("🚨 Error: Chat file not found! Check the file path.")
else:
    print(f"✅ File found at: {file_path}")
    print(f"📏 File size: {os.path.getsize(file_path)} bytes")

    # 🔹 Read the chat file
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            chat_data = file.read()
        print("✅ Chat file loaded successfully!")
    except Exception as e:
        print(f"❌ Error reading file: {e}")

    # 🔹 Process Chat Data
    def chatprocess(data):
        pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APMapm]{2}\s-\s'
        messages = re.split(pattern, data)[1:]  # Extract messages
        dates = re.findall(pattern, data)  # Extract dates

        if len(messages) == 0 or len(dates) == 0:
            print("🚨 Error: No messages or dates found. Check the file format!")
            return None

        df = pd.DataFrame({'user_message': messages, 'message_date': dates})
        df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ')
        df.rename(columns={'message_date': 'date'}, inplace=True)

        users, messages = [], []
        for message in df['user_message']:
            entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)
            if len(entry) > 1:
                users.append(entry[1])
                messages.append(entry[2])
            else:
                users.append('group_notification')
                messages.append(entry[0])

        df['user'] = users
        df['message'] = messages
        def get_sentiment(text):
            analysis = TextBlob(text)
            if analysis.sentiment.polarity > 0:
                return "Positive"
            elif analysis.sentiment.polarity < 0:
                return "Negative"
            else:
                return "Neutral"

        df.drop(columns=['user_message'], inplace=True)

        df['only_date'] = df['date'].dt.date
        df['year'] = df['date'].dt.year
        df['month_num'] = df['date'].dt.month
        df['month'] = df['date'].dt.month_name()
        df['day'] = df['date'].dt.day
        df['day_name'] = df['date'].dt.day_name()
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute

        df['hour_12'] = df['date'].dt.strftime('%I')
        df['am_pm'] = df['date'].dt.strftime('%p')
        df['period'] = df.apply(
            lambda row: f"{row['hour_12']} {row['am_pm']} - {(int(row['hour_12']) % 12 + 1)} {row['am_pm']}", axis=1)
        df['sentiment'] = df['message'].apply(get_sentiment)

        print("🔄 Processed Data Sample:")
        print(df.head())  # Show first few rows
        print("📝 Available Columns:", df.columns)  # Show column names
        plt.figure(figsize=(6, 4))
        sns.countplot(x=df['sentiment'], palette="coolwarm")
        plt.title("Sentiment Analysis of Messages")
        plt.xlabel("Sentiment Category")
        plt.ylabel("Message Count")
        plt.show()

        return df

    # 🔹 Call function to process chat
    chat_df = chatprocess(chat_data)

    # 🔹 Save processed data to CSV
    if chat_df is not None:
        output_file = os.path.join(os.path.dirname(file_path), "processed_chat.csv")
        chat_df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"✅ Processed chat saved to: {output_file}")
