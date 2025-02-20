import pandas as pd

# Read the data
df = pd.read_csv('all_time_gaps.csv')

df['state'] = 'neither'

time_gap_condition = df['time_gap'] > 5

df['previous_end_time'] = df['end_time'].shift()
df['previous_end_time'] = pd.to_datetime(df['previous_end_time'])
df['previous_end_time_at_night'] = (
    (df['previous_end_time'].dt.hour >= 20) | (df['previous_end_time'].dt.hour < 4)
)

df.loc[time_gap_condition & df['previous_end_time_at_night'], 'state'] = 'wake up'

df.loc[df['state'].shift(-1) == 'wake up', 'state'] = 'sleep'

df.drop(columns=['previous_end_time', 'previous_end_time_at_night'], inplace=True)

df.to_csv('sleep classified.csv', index=False)




