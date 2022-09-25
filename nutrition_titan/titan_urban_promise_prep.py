from dfcleanup import df_stripper


df = pd.read_excel('Urban Promise.xls', dtype=str, skiprows=1, header=None)
df = df_stripper(df)
df = df.loc[df[0] == '5544']

df[5] = pd.to_datetime(df[5])
df[5] = df[5].dt.strftime('%m/%d/%Y')
df[1] = df[1].str.zfill(6)
df[4] = df[4].str.zfill(2)
df[4] = df[4].str.replace('0K','KN')