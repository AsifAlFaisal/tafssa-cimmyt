#%%
import pandas as pd
import plotly.express as px
# %%
file_name = "C:/Users/A.FAISAL/OneDrive - CIMMYT/ASIF BACKUP/TAFSSA/Anton Data Requirements/Final DB/221220_south_asia_merged_Ag_diversity_TAFSSA.csv"
df = pd.read_csv(file_name, encoding="ISO-8859-1")
df = df.apply(lambda x: x.astype(str).str.title())
df['uid'] = df['uid'].apply(lambda x: x.upper())
df['GID_2'] = df['GID_2'].apply(lambda x: x.upper())
df['production'] = df['production'].apply(lambda x: float(x.replace('\n','')))
df['area'] = df['area'].apply(lambda x: float(x.replace('\n','')))
df = df[df['production'] !=0]
# %% Check Unique Years
print(df.groupby(by=['country']).agg({'year':'unique'}).reset_index())
# %%
data1 = pd.read_csv("221221_ag_diversity_crop_category_summary.csv",encoding="ISO-8859-1")

data2 = pd.read_csv("221221_ag_diversity_crop_summary.csv",encoding="ISO-8859-1")

data3 = df.groupby(["country","division/state","district","year"]).agg({"crop":"count","GID_2":"first","area":"sum","production":"sum"}).reset_index()

data4 = df.groupby(["country","year",'crop']).agg({"area":"sum","production":"sum"}).reset_index()
data4['production'] = data4['production'].apply(lambda x: round(x/1000, 2))

data5 = df.groupby(["country","year",'crop_category2']).agg({"area":"sum","production":"sum"}).reset_index()
data5['production'] = data5['production'].apply(lambda x: round(x/1000, 2))
data5 = data5[data5['crop_category2'] !="Unknown"]
# %%

color_dict = {
    'Dark Green Leafy Vegetables ':'rgb(15,133,84)',
    'Grains, White Roots And Tubers, And Plantains ':'rgb(115, 175, 72)',
    'Non Food Crops':'rgb(95, 70, 144)',
    'Non Healthy Cash Crops':'rgb(29, 105, 150)',
    'Nuts And Seeds ':'rgb(56, 166, 165)',
    'Other Fruits':'rgb(237, 173, 8)',
    'Other Vegetables':'rgb(225, 124, 5)',
    'Other Vitamin A-Rich Fruits And Vegetables':'rgb(204, 80, 62)',
    'Pulses (Beans, Peas And Lentils)':'rgb(148, 52, 110)',
    'Spices':'rgb(102, 102, 102)'
}

def country_filter(data, country, year):
    return data.query(f"country=='{country}' and year=='{year}'").reset_index(drop=True)

def ranking_barchart(data, country, year, sort_col, x_col, y_col, title, x_label, y_label, top10="Top"):
    data = country_filter(data, country, year)
    data = data.sort_values(by=[sort_col], ascending=False).reset_index(drop=True)
    df = data.head(10) if top10=="Top" else data.tail(10)

    color_scale = "Blugrn" if top10=="Top" else "Burg"
    fig = px.bar(df, x=x_col, y=y_col, text=y_col, color=y_col,
                height=600, width=800,
                color_continuous_scale=color_scale)
    fig.update_layout(
        title={"text":f"{title}", "x":0.5, "font_size":20},
        font_family="Arial",
        font_size = 15,
        title_font_family="Times New Roman"
    )
    fig.update_xaxes(title={"text":f"{x_label}", "font_size":18})
    fig.update_yaxes(title={"text":f"{y_label}", "font_size":18})
    fig.update_coloraxes(showscale=False, reversescale=False if top10=="Top" else True)

    return fig


def custom_barchart(data, country, year, sort_col, x_col, y_col, title, x_label, y_label):
    data = country_filter(data, country, year)
    data = data.sort_values(by=[sort_col], ascending=False).reset_index(drop=True)
    #color_scale = px.colors.sequential.Viridis
    fig = px.bar(data, x=x_col, y=y_col, text=y_col, color=x_col,
                height=600, width=800,
                #color_discrete_sequence=color_scale
                color_discrete_map=color_dict)
    fig.update_layout(
        title={"text":f"{title}", "x":0.5, "font_size":20},
        font_family="Arial",
        font_size = 15,
        title_font_family="Times New Roman"
    )
    fig.update_xaxes(title={"text":f"{x_label}", "font_size":18})
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(title={"text":f"{y_label}", "font_size":18})
    fig.update_layout(legend=dict(
        title={"text":f"{x_label}"},
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.42
    ))

    return fig

# %% Top 10 district by crop cultivated
for country in data3['country'].unique():
    for year in data3.query(f"country=='{country}'")['year'].unique():
        top = "Top"
        fname = f"221221_{country}_{year}_{top}10Crop.png"
        title = f"{top} 10 Districts in {country} by Number of Crops Cultivated (Year: {year})"
        fig = ranking_barchart(data3, country, year,'crop', 'district','crop', title, 'District', 'Number of Crops', top)
        fig.write_image(f"../output/{fname}")

# %%
# %% Top 10 district by richness index (diversity)
for country in data1['country'].unique():
    for year in data1.query(f"country=='{country}'")['year'].unique():
        top = "Top"
        fname = f"221221_{country}_{year}_{top}10_RichnessIndex.png"
        title = f"{top} 10 Districts in {country} by Diverse Crop Category (Year: {year})"
        fig = ranking_barchart(data1, country, year,'richness_index', 'district','richness_index', title, 'District', 'Number of Crop Category', top)
        fig.write_image(f"../output/{fname}")
# %% Top 10 crops by production
for country in data4['country'].unique():
    for year in data4.query(f"country=='{country}'")['year'].unique():
        top = "Bottom"
        fname = f"221221_{country}_{year}_{top}10_crop_production.png"
        title = f"{top} 10 Growing Crops in {country} (Year: {year})"
        fig = ranking_barchart(data4, country, year,'production', 'crop','production', title, 'Crop', "Production ('000 tonnes)", top)
        fig.write_image(f"../output/{fname}")

# %% Top 10 crop category by production
for country in data5['country'].unique():
    for year in data5.query(f"country=='{country}'")['year'].unique():
        top = "Top"
        fname = f"221221_{country}_{year}_crop_category_production.png"
        title = f"Production by Major Crop Category in {country} (Year: {year})"
        fig = custom_barchart(data5, country, year, 'production', 'crop_category2','production', title, 'Crop Category', "Production ('000 tonnes)")
        fig.write_image(f"../output/{fname}")
        #fig.show()

# %%
