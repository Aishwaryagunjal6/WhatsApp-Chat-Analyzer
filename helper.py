from urlextract import URLExtract
extract =URLExtract()
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
def fetch_stats(selected_user, df):
    # if selected_user == 'Overall':
    #     # Fetch the Number of Messages
    #     num_messages = df.shape[0]
    #     # Fetch the number of words
    #     words = []
    #     for message in df['messages']:
    #         words.extend(message.split())
    #     return num_messages,len(words)  #this will return the overall msg count and number of words
    # else:
    #     new_df = df[df['users']==selected_user]
    #     # Fetch the Number of Messages
    #     num_messages = new_df.shape[0]
    #     # Fetch the number of words
    #     words = []
    #     for message in new_df['messages']:
    #         words.extend(message.split())
    #     return num_messages,len(words)   #this will return the count of the msg and words sent by a particular user

    #the above code was written earlier but seems so ig hence i am writing am optimized code by just replacing the contents in the dataframe df if the selected user is not overall
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    #fetch number of messages sent
    num_messages = df.shape[0]

    #fetch the totall number of words
    words= []
    for message in df['messages']:
        words.extend(message.split())

    #fetcb the media count
    #here where the media is shared a message is arrived as "<media omitted>" we have to just calculate how many times this message is arrived in the chat data
    num_media = df[df['messages'] == '<Media omitted>\n'].shape[0]

    #fetch the links shared
    links = []
    for message in df['messages']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media,len(links)


def most_busy_users(df):
    x = df['users'].value_counts().head()
    df=round((df['users'].value_counts() / df.shape[0])*100 , 2).reset_index().rename(columns={'index':'name', 'user':'percentage'})
    #reset_index() is used to convert the data into dataframe
    return x,df


#creating World Cloud
def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    def remove_stopwords(message):     #function to remove stopword and media omiitted from the cloud
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=400, height=400, min_font_size=10 , background_color='white')
    temp['messages']=temp['messages'].apply(remove_stopwords)  #storing the remaining words after removing the stop words into temp dataframe
    df_wc= wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc

#Function to find most common words
def most_common_words(selected_user, df):

    f=open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    temp=df[df['users']!='group_notification']
    temp=temp[temp['messages']!='<Media omitted>\n']

    words =[]

    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

import emoji
import pandas as pd
from collections import Counter

def emoji_helper(selected_user, df):  # function to analyze emojis
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month', 'month_num']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time']=time

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()
    return daily_timeline

def Weekly_activity(selected_user, df):  # function to analyze emojis
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()

def Monthly_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

def Activity_heatmap(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    activity_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)
    return activity_heatmap