import pandas as pd

# Load
df = pd.read_csv('before.csv')

# Remove duplicates
df = df.drop_duplicates()

# Drop missing emails
df = df.dropna(subset=['email'])

# Save
df.to_csv('after.csv', index=False)
