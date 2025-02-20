import pandas as pd
from datetime import datetime
import pytz

# Load the CSV file
df = pd.read_csv('/Users/miamccarrick/screenTime.csv')

#Used ChatGPT to help convert to EST
# Define a function to convert UTC to EST
def convert_utc_to_est(timestamp):
    # Convert the timestamp to a datetime object (UTC)
    dt_utc = datetime.utcfromtimestamp(timestamp)

    # Define the EST timezone
    est = pytz.timezone('US/Eastern')

    # Localize the datetime to UTC and convert to EST
    dt_est = pytz.utc.localize(dt_utc).astimezone(est)

    # Return formatted EST time as a string
    return dt_est.strftime('%Y-%m-%d %H:%M:%S')


# Assuming the timestamps are in columns 'timestamp1' and 'timestamp2', update these columns
df['start_time'] = df['start_time'].apply(lambda x: convert_utc_to_est(x) if pd.notnull(x) else x)
df['end_time'] = df['end_time'].apply(lambda x: convert_utc_to_est(x) if pd.notnull(x) else x)
df['created_at'] = df['created_at'].apply(lambda x: convert_utc_to_est(x) if pd.notnull(x) else x)

# Save the updated DataFrame back to a CSV
df.to_csv('new_updated_screentime.csv', index=False)

print("CSV file updated successfully!")
