import pandas as pd
import matplotlib.pyplot as plt

df_one = pd.read_csv("Plant_1_Generation_Data.csv")
df_two = pd.read_csv("Plant_2_Generation_Data.csv")

df = pd.concat((df_one, df_two))

# print(df.isnull().sum())
df.dropna(inplace=True)
# print(df.isnull().sum())

df["DATE_TIME"] = pd.to_datetime(df["DATE_TIME"])
df_first_week = df.loc[(df["DATE_TIME"] >= "15-05-2020 00:00") & (df["DATE_TIME"] < "22-05-2020 23:45")].reset_index()
df_first_week_one_generator = df_first_week.loc[(df_first_week["SOURCE_KEY"] == "xoJJ8DcxJEcupym")]

df_first_week_average = df_first_week.groupby('DATE_TIME')['AC_POWER'].mean().reset_index()

plt.plot(df_first_week_one_generator["DATE_TIME"], df_first_week_one_generator["AC_POWER"], label="xoJJ8DcxJEcupym")
plt.plot(df_first_week_average["DATE_TIME"], df_first_week_average["AC_POWER"], label="AllGenerators")
plt.legend()
plt.show()

df_merged = df_first_week.merge(df_first_week_average, on="DATE_TIME")
df_week_generators = df_merged.loc[(df_merged["AC_POWER_x"] < 0.8 * df_merged["AC_POWER_y"])]
print(df_week_generators[["SOURCE_KEY", "AC_POWER_x", "AC_POWER_y"]].head(10))
