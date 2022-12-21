#%%
import pandas as pd
# %%
file_name = "C:/Users/A.FAISAL/OneDrive - CIMMYT/ASIF BACKUP/TAFSSA/Anton Data Requirements/Final DB/221220_south_asia_merged_Ag_diversity_TAFSSA.csv"
df = pd.read_csv(file_name, encoding="ISO-8859-1")
df = df.apply(lambda x: x.astype(str).str.title())
df['uid'] = df['uid'].apply(lambda x: x.upper())
df['GID_2'] = df['GID_2'].apply(lambda x: x.upper())
#df[['area','production']] = df[['area','production']].apply(pd.to_numeric, errors='raise')
df['production'] = df['production'].apply(lambda x: float(x.replace('\n','')))
df['area'] = df['area'].apply(lambda x: float(x.replace('\n','')))
df = df[df['production'] !=0]
df
# %%
#df.groupby(["country","division/state","district"]).agg({"crop_category2":"count", "GID_2":"first","area":"sum","production":"sum"})
crop_summary = df.groupby(["country","division/state","district","year","crop_category2"]).agg({"crop":"count","GID_2":"first","area":"sum","production":"sum"}).reset_index()
crop_summary.rename(columns={"crop_category2":"major_crop_category","crop":"number_of_crops"}, inplace=True)
# %%
category_summary = df.groupby(["country","division/state","district","year"]).agg({"crop_category2":"unique","GID_2":"first","area":"sum","production":"sum"}).reset_index()
category_summary["richness_index"] = category_summary["crop_category2"].apply(lambda x: len(x))
category_summary.rename(columns={"crop_category2":"major_crop_category"}, inplace=True)
# %%
crop_summary.to_csv("221221_ag_diversity_crop_summary.csv", index=False)
category_summary.to_csv("221221_ag_diversity_crop_category_summary.csv", index=False)
# %%
