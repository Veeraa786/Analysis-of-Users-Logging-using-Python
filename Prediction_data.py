import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

takehome_users = pd.read_csv("F:\\GUVI\\Task 5\\takehome_users.csv", encoding='latin-1')
takehome_user_engagement = pd.read_csv("F:\\GUVI\\Task 5\\takehome_user_engagement.csv", encoding='latin-1')

#print(takehome_users)
#takehome_users.info()

takehome_users.describe().T

#takehome_user_engagement.info()

takehome_user_engagement.describe().T

takehome_user_engagement.user_id.nunique()

#print(takehome_users['last_session_creation_time'])

takehome_users['last_session_creation_time'] = pd.to_datetime(takehome_users['last_session_creation_time'], unit='s')

#print(takehome_users['last_session_creation_time'])
#takehome_users.last_session_creation_time.dtypes
#print(takehome_users.head(4))

takehome_users['last_session_creation_time'].min(),takehome_users['last_session_creation_time'].max()
df = takehome_user_engagement.copy()
df['date'] = pd.to_datetime(df.time_stamp)

#print(df['date'])

def rolling_count(df_group,frequency):
  return df_group.rolling(frequency, on='date')['user_id'].count()

df['visits_7_days'] = df.groupby('user_id', as_index=False, group_keys=False).apply(rolling_count, '7D')

#df.describe().T
#print(df['visits_7_days'])

df[df.visits_7_days >= 3.0]

adopted = df.groupby('user_id')['visits_7_days'].max().reset_index()

adopted['adopted_user'] = adopted['visits_7_days'].apply(lambda x: 1 if x>=3 else 0)

adopted.head()

adopted.drop(['visits_7_days'], axis=1, inplace=True)
adopted.rename(columns={"user_id": "object_id"}, inplace=True)

adopted.set_index("object_id", inplace = True)

application_users = takehome_users.join(adopted, on = 'object_id', how='left')

application_users.head()

application_users['last_session_creation_time'].fillna(0, inplace = True)

application_users['adopted_user'].fillna(0, inplace = True)

application_users.describe().T

application_users['email_domain'] = application_users.email.apply(lambda x: x.split('@')[1])
application_users['email_domain'].value_counts()

application_users[~application_users.invited_by_user_id.isnull()].creation_source.unique()

application_users.drop(['object_id', 'name', 'email', 'email_domain'], axis = 1, inplace = True)

