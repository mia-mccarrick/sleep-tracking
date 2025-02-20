import pandas as pd

df = pd.read_csv('official screentime.csv')

df['start_time'] = pd.to_datetime(df['start_time'])
df['end_time'] = pd.to_datetime(df['end_time'])

df = df.sort_values(by='end_time')

df['time_gap'] = (df['start_time'] - df['end_time'].shift()).dt.total_seconds() / 3600

df.to_csv('all_time_gaps.csv', index=False)

