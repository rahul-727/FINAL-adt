import datetime

# Get today's date and time
now = datetime.datetime.now()

# Get the time delta for one day
one_day = datetime.timedelta(days=1)

# Calculate the next day
next_day = now + one_day

# Print the next day in YYYY-MM-DD format
print(next_day.strftime('%Y-%m-%d'))