from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
from emoji import is_emoji
import matplotlib.pyplot as plt

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = sum(len(message.split()) for message in df['message'])
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    num_links = sum(len(extract.find_urls(message)) for message in df['message'])
    return num_messages, words, num_media_messages, num_links

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df_percent = (df['user'].value_counts(normalize=True) * 100).reset_index()
    df_percent.columns = ['name', 'percent']
    return x, df_percent

def create_wordcloud(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>\n')]
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(lambda msg: ' '.join([word for word in msg.lower().split() if word not in stop_words]))
    return wc.generate(temp['message'].str.cat(sep=' '))

def most_common_words(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>\n')]
    words = [word for message in temp['message'] for word in message.lower().split() if word not in stop_words]
    return pd.DataFrame(Counter(words).most_common(20))

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = [char for message in df['message'] for char in message if is_emoji(char)]
    return pd.DataFrame(Counter(emojis).most_common())

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline['month'] + '-' + timeline['year'].astype(str)
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df.groupby('only_date').count()['message'].reset_index()

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
