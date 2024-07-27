import streamlit as st
import PreProcessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp-Chat-Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    #here the uploaded file is stream of byte data we have to convert it into the string datatype
    data = bytes_data.decode("utf-8")  #converted into string and stored into the data variable
    df = PreProcessor.preprocess(data)  #preprocessing the data to convert it into the desired form

    #st.dataframe(df)        #this is to display the messages inside thedataframe

    #fetch unique users to display the dropdown list of users
    user_list = df['users'].unique().tolist()

    user_list.remove('group_notification')  #to remove group notification from unique user list
    user_list.sort()  #sort the user list alphabetically
    user_list.insert(0,"Overall")    #inserted an unique user ooverall at 0th index which will show theoverall analysis of chat

    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    #Adding an button to start the Analysis
    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        num_messages, words, num_media, links = helper.fetch_stats(selected_user, df)   #function to fetch the total number of messages and words

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media)

        with col4:
            st.header("Links Shared")
            st.title(links)

#Most Busy Users
    if selected_user=='Overall':
        st.title("Most Busy users")
        x, new_df= helper.most_busy_users(df)    # x will contain the name and the msg sent values of all the users
        #new_df will contain the dataframe consisting the activity of users in percentage along with user names
        fig, ax=plt.subplots()

        col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values , color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.dataframe(new_df)

 # Create wordColud
    st.title("Word Cloud")
    df_wc = helper.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

# Most common words
    st.title("Most Common Words")
    most_common_df = helper.most_common_words(selected_user, df)
    col1, col2 = st.columns(2)  # This will equally split the screen into two columns

    with col1:  # to show the graph
      st.dataframe(most_common_df)

    with col2:  # to show the dataframe of the graph
        fig, ax = plt.subplots(figsize=(12, 10))  # Adjust the width and height here
        ax.barh(most_common_df[0], most_common_df[1])  # barh is a kind of horizontal plot
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


#Emoji Analysis

    emoji_df = helper.emoji_helper(selected_user, df)
    st.title("Emoji Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig, ax = plt.subplots()
        ax.pie(emoji_df[1].head(7), labels=emoji_df[0].head(7), autopct="%0.2f")
        st.pyplot(fig)

#Monthly Timeline Analysis
    st.title("Monthly Timeline")
    timeline = helper.monthly_timeline(selected_user, df)
    fig,ax=plt.subplots()
    ax.plot(timeline['time'], timeline['messages'], color='green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

#Daily Timeline Analysis
    st.title("Daily Timeline")
    d_timeline = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(d_timeline['only_date'], d_timeline['messages'], color='black')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

#Activity Analysis
    st.title("Activity Map")
    col1, col2 = st.columns(2)

    with col1:
        st.header("Most Busy Day")
        busy_day = helper.Weekly_activity(selected_user, df)
        fig,ax=plt.subplots()
        ax.bar(busy_day.index, busy_day.values)
        plt.xticks(rotation='vertical', color='green')
        st.pyplot(fig)

    with col2:
        st.header("Most Busy Month")
        busy_month = helper.Monthly_activity(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values, color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

# Activity Heat Map
    st.title("Activity Heat Map")
    activity_heatmap=helper.Activity_heatmap(selected_user, df)
    fig, ax = plt.subplots()
    ax= sns.heatmap(activity_heatmap)
    st.pyplot(fig)