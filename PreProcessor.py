import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create DataFrame
    df = pd.DataFrame({'user_messages': messages, 'message_date': dates})

    # Function to convert date strings with mixed formats
    def convert_date(date_str):
        try:
            # Try to parse with day/month/year format
            return pd.to_datetime(date_str, format='%d/%m/%y, %H:%M - ')
        except ValueError:
            try:
                # If it fails, try to parse with month/day/year format
                return pd.to_datetime(date_str, format='%m/%d/%y, %H:%M - ')
            except ValueError:
                return pd.NaT  # If both fail, return NaT

    # Apply conversion function to the date column
    df['message_date'] = df['message_date'].apply(convert_date)

    # Rename the column
    df.rename(columns={'message_date': 'date'}, inplace=True)



    # separate username and the message
    users = []
    messages = []
    for message in df['user_messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['users'] = users
    df['messages'] = messages
    df.drop(columns='user_messages', inplace=True)

    df['year'] = df['date'].dt.year  # extracted the year
    df['month'] = df['date'].dt.month_name()  # extracted the month name from date
    df['month_num'] = df['date'].dt.month   # extracted the month number from date
    df['day'] = df['date'].dt.day  # Extracted day
    df['hour'] = df['date'].dt.hour  # Extracted the hour from date column
    df['minute'] = df['date'].dt.minute  # Extracted the minute
    df['only_date'] = df['date'].dt.date  #Gives the date only
    df['day_name'] = df['date'].dt.day_name()   #Extracted the names of the days

    period= []
    for hour in df[['day_name','hour']]['hour']:
        if hour==23:
            period.append(str(hour)+"-"+str('00'))
        elif hour==0:
            period.append(str(00)+"-"+str(hour+1))
        else :
            period.append(str(hour) + "-" + str(hour + 1))

    df['period']=period

    return df

#here the above function is used for the data preprocessing purpose
#when we give textual data as an input then the above function will convert that data into the desired format
