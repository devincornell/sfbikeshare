import pandas as pd

df = pd.read_csv('trip.csv')
df.info()

l = df.values.tolist()

print(l[0:3])
