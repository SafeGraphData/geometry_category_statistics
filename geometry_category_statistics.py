import streamlit as st
from read_data import read_from_gsheets
import altair as alt
from datetime import datetime, timedelta
import pandas as pd
import streamlit.components.v1 as components
import plotly.express as px

st.set_page_config(
    page_title="Geometry Summary Statistics - Latest Release",
    layout="wide"
)

#### Geometry Category Stats ####


category_stats_df = read_from_gsheets("Category stats")\
    [["Country", "naics_2", "naics_code", "safegraph_category", "safegraph_subcategory", "industry_title", "total_poi_count", "poi_with_polygon_count", "Polygon coverage"]]\
    .astype({'total_poi_count': int,"poi_with_polygon_count":int, "Polygon coverage":float })

category_stats_df['safegraph_subcategory'] = category_stats_df['safegraph_subcategory'].astype(str).replace("NaN", " ")
category_stats_df['safegraph_category'] = category_stats_df['safegraph_category'].astype(str).replace("NaN", " ")

global_df = category_stats_df.groupby(['naics_2', 'industry_title'])\
    .agg(total_poi_count=('total_poi_count', 'sum'), poi_with_polygon_count=("poi_with_polygon_count", "sum"))\
    .sort_values('poi_with_polygon_count', ascending=False)\
    .reset_index()\
    .rename(columns={"naics_2": "2-digit NAICS", "industry_title": "Industry Title", "total_poi_count": "Total POI", "poi_with_polygon_count":"POI with polygon count"})
global_df['Overall Polygon Coverage'] = (global_df['POI with polygon count'] /global_df['Total POI']) * 100

global_df_styled = global_df.drop(["Total POI"], axis=1).style.apply(lambda x: ['background-color: #D7E8ED' if i % 2 == 0 else '' for i in range(len(x))], axis=0)\
    .format({"POI with polygon count": "{:,}",
              "Overall Polygon Coverage": "{:.01f}%"})

countries = ['US', 'UK', 'CA']
dfs = []

for country in countries:
    df = (
        category_stats_df[category_stats_df['Country'] == country]
        [["naics_code", "safegraph_category", "safegraph_subcategory", "poi_with_polygon_count", "Polygon coverage"]]
        .rename(columns={"naics_code": "NAICS Code", "safegraph_category": "SafeGraph Category",\
                         "safegraph_subcategory": "SafeGraph Subcategory", "poi_with_polygon_count": "POI with Polygon Count"})
        .assign(**{
            "Polygon coverage": lambda df: ((df["Polygon coverage"]) * 100).astype(float)
    }).sort_values('POI with Polygon Count', ascending=False)
        .reset_index(drop=True)
    )

    df['POI with Polygon Count'] = df['POI with Polygon Count'].astype(int).apply(lambda x: "{:,}".format(x))
    df['Polygon coverage'] = df['Polygon coverage'].astype(float).apply(lambda x: "{:.01f}%".format(x))
    dfs.append(df)

naics_possible_df = dfs[0]
naics_possible_df['Category'] = naics_possible_df['NAICS Code'].astype(str) + " " + naics_possible_df['SafeGraph Category']\
      + " " + naics_possible_df['SafeGraph Subcategory'] 


possible_naics_codes = naics_possible_df['Category'].astype(str).unique()

tabs = st.tabs(["Global"] + countries)
with tabs[0]:
    # st.write("Global POI Count")
    st.dataframe(global_df_styled, use_container_width=True, hide_index=True)

for i, tab in enumerate(tabs[1:]):
    with tab:
        if i < len(dfs):
            naics_list = st.selectbox("NAICS Code:", [""] + possible_naics_codes.tolist(), key = i)
            if naics_list:
                styled_dfs = (
                    dfs[i][dfs[i]['NAICS Code'].astype(str).str.startswith(naics_list.split(" ")[0])]\
                        .style.apply(lambda x: ['background-color: #D7E8ED' if i % 2 == 0 else '' for i in range(len(x))], axis=0)
                    )
                # st.write(f"{countries[i]} POI Count")
                st.dataframe(styled_dfs, use_container_width=True, hide_index=True)
            else:
                styled_dfs = (
                    dfs[i].style.apply(lambda x: ['background-color: #D7E8ED' if i % 2 == 0 else '' for i in range(len(x))], axis=0)
                    )
                # st.write(f"{countries[i]} POI Count")
                st.dataframe(styled_dfs, use_container_width=True, hide_index=True)



hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

css = '''
<style>
section.main > div:has(~ footer ) {
    padding-top: 0px;
    padding-bottom: 0px;
}

[data-testid="ScrollToBottomContainer"] {
    overflow: hidden;
}
</style>
'''

st.markdown(css, unsafe_allow_html=True)

# Keep-alive comment: 2025-03-29 14:27:19.042722
# Keep-alive comment: 2025-03-31 15:59:18.313979
# Keep-alive comment: 2025-03-31 19:24:56.196057
# Keep-alive comment: 2025-04-01 06:22:37.148309
# Keep-alive comment: 2025-04-01 17:23:31.285294
# Keep-alive comment: 2025-04-02 04:23:16.632942
# Keep-alive comment: 2025-04-02 15:23:15.869611
# Keep-alive comment: 2025-04-03 02:22:50.191419
# Keep-alive comment: 2025-04-03 13:23:56.197234