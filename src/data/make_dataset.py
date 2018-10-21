import pandas as pd



# We read the csv
df118 = pd.read_csv("../../data/raw/0118.csv")
df218 = pd.read_csv("../../data/raw/0218.csv")
df318 = pd.read_csv("../../data/raw/0318.csv")
df418 = pd.read_csv("../../data/raw/0418.csv")
df417 = pd.read_csv("../../data/raw/0417.csv")
df518 = pd.read_csv("../../data/raw/0518.csv")
df517 = pd.read_csv("../../data/raw/0517.csv")
df617 = pd.read_csv("../../data/raw/0617.csv")
df717 = pd.read_csv("../../data/raw/0717.csv")
df817 = pd.read_csv("../../data/raw/0817.csv")
df917 = pd.read_csv("../../data/raw/0917.csv")
df1017 = pd.read_csv("../../data/raw/1017.csv")
df1117 = pd.read_csv("../../data/raw/1117.csv")
df1217 = pd.read_csv("../../data/raw/1217.csv")


# We new Create a new dataframe adding everything
df = df118.append([df218, df318, df418, df518, df417, df517, df617, df717, df817, df917, df1017, df1117, df1217])

print(df.columns)

df = df.drop('Unnamed: 29', axis = 1)

df.to_csv('../../data/interim/vuelos.csv', index=False)