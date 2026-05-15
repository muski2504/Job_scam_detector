import pandas as pd

df = pd.read_csv('data/scam_posts_v2.csv')
print(f"Before: {len(df)} rows")

df.drop_duplicates(subset=['text'], inplace=True)
df = df[df['text'].str.strip() != '']
df = df[df['is_scam'].isin([0, 1])]
df['text'] = df['text'].str.strip()

df.to_csv('data/scam_posts_clean.csv', index=False)
print(f"After: {len(df)} rows")
print(f"Scam: {df['is_scam'].sum()}")
print(f"Legit: {len(df) - df['is_scam'].sum()}")
print("Done! scam_posts_clean.csv saved.")