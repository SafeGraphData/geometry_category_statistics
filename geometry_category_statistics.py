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
# Keep-alive comment: 2025-04-04 00:24:17.525002
# Keep-alive comment: 2025-04-04 11:23:48.903859
# Keep-alive comment: 2025-04-04 22:23:00.387107
# Keep-alive comment: 2025-04-05 09:22:50.551589
# Keep-alive comment: 2025-04-05 20:24:05.929003
# Keep-alive comment: 2025-04-06 07:23:35.597712
# Keep-alive comment: 2025-04-06 18:23:07.297673
# Keep-alive comment: 2025-04-07 05:23:31.069257
# Keep-alive comment: 2025-04-07 16:24:30.333618
# Keep-alive comment: 2025-04-08 03:23:47.249111
# Keep-alive comment: 2025-04-08 14:24:06.025270
# Keep-alive comment: 2025-04-09 01:23:30.432626
# Keep-alive comment: 2025-04-09 12:23:11.586700
# Keep-alive comment: 2025-04-09 23:23:30.835834
# Keep-alive comment: 2025-04-10 10:22:41.034233
# Keep-alive comment: 2025-04-10 21:23:04.291934
# Keep-alive comment: 2025-04-11 08:25:15.085274
# Keep-alive comment: 2025-04-11 19:25:36.290419
# Keep-alive comment: 2025-04-12 06:23:11.093344
# Keep-alive comment: 2025-04-12 17:23:24.612451
# Keep-alive comment: 2025-04-13 04:22:43.607154
# Keep-alive comment: 2025-04-13 15:23:38.872965
# Keep-alive comment: 2025-04-14 02:24:00.083525
# Keep-alive comment: 2025-04-14 13:23:24.224184
# Keep-alive comment: 2025-04-15 00:23:09.214576
# Keep-alive comment: 2025-04-15 11:23:31.316289
# Keep-alive comment: 2025-04-15 22:23:14.922201
# Keep-alive comment: 2025-04-16 09:23:54.141311
# Keep-alive comment: 2025-04-16 20:23:44.358361
# Keep-alive comment: 2025-04-17 07:23:15.395532
# Keep-alive comment: 2025-04-17 18:25:38.995038
# Keep-alive comment: 2025-04-18 05:22:59.665763
# Keep-alive comment: 2025-04-18 16:23:05.138054
# Keep-alive comment: 2025-04-19 03:23:29.996900
# Keep-alive comment: 2025-04-19 14:22:40.855641
# Keep-alive comment: 2025-04-20 01:22:39.449722
# Keep-alive comment: 2025-04-20 12:23:34.395136
# Keep-alive comment: 2025-04-20 23:23:09.095869
# Keep-alive comment: 2025-04-21 10:23:55.380467
# Keep-alive comment: 2025-04-21 21:23:19.137399
# Keep-alive comment: 2025-04-22 08:23:30.050947
# Keep-alive comment: 2025-04-22 19:23:30.365149
# Keep-alive comment: 2025-04-23 06:23:04.045654
# Keep-alive comment: 2025-04-23 17:23:07.586641
# Keep-alive comment: 2025-04-24 04:23:10.129312
# Keep-alive comment: 2025-04-24 15:24:06.531325
# Keep-alive comment: 2025-04-25 02:22:44.029129
# Keep-alive comment: 2025-04-25 13:24:05.150691
# Keep-alive comment: 2025-04-25 16:08:16.322047
# Keep-alive comment: 2025-04-25 16:18:11.136564
# Keep-alive comment: 2025-04-26 00:23:45.385609
# Keep-alive comment: 2025-04-26 11:23:40.820132
# Keep-alive comment: 2025-04-26 22:22:39.890058
# Keep-alive comment: 2025-04-27 09:23:10.730182
# Keep-alive comment: 2025-04-27 20:23:05.448051
# Keep-alive comment: 2025-04-28 07:23:19.541332
# Keep-alive comment: 2025-04-28 18:23:55.539597
# Keep-alive comment: 2025-04-29 05:23:25.652052
# Keep-alive comment: 2025-04-29 16:24:09.451521
# Keep-alive comment: 2025-04-30 03:23:00.141005
# Keep-alive comment: 2025-04-30 14:23:10.893420
# Keep-alive comment: 2025-05-01 01:23:39.538552
# Keep-alive comment: 2025-05-01 12:23:10.103644
# Keep-alive comment: 2025-05-01 23:22:43.358254
# Keep-alive comment: 2025-05-02 10:23:29.584161
# Keep-alive comment: 2025-05-02 21:22:39.900314
# Keep-alive comment: 2025-05-03 08:23:04.340954
# Keep-alive comment: 2025-05-03 19:23:24.019940
# Keep-alive comment: 2025-05-04 06:23:29.431031
# Keep-alive comment: 2025-05-04 17:22:38.801424
# Keep-alive comment: 2025-05-05 04:23:48.963117
# Keep-alive comment: 2025-05-05 15:23:06.500484
# Keep-alive comment: 2025-05-06 02:23:59.670659
# Keep-alive comment: 2025-05-06 13:23:00.112838
# Keep-alive comment: 2025-05-07 00:22:59.967929
# Keep-alive comment: 2025-05-07 11:22:59.912637
# Keep-alive comment: 2025-05-07 22:23:10.611911
# Keep-alive comment: 2025-05-08 09:23:02.975853
# Keep-alive comment: 2025-05-08 20:22:59.671084
# Keep-alive comment: 2025-05-09 07:23:10.285623
# Keep-alive comment: 2025-05-09 18:23:31.406033
# Keep-alive comment: 2025-05-10 05:23:09.247315
# Keep-alive comment: 2025-05-10 16:23:03.460493
# Keep-alive comment: 2025-05-11 03:23:03.731889
# Keep-alive comment: 2025-05-11 14:22:55.570232
# Keep-alive comment: 2025-05-12 01:23:00.867540
# Keep-alive comment: 2025-05-12 12:23:30.332763
# Keep-alive comment: 2025-05-12 23:23:04.090916
# Keep-alive comment: 2025-05-13 10:24:00.687078
# Keep-alive comment: 2025-05-13 21:23:04.427076
# Keep-alive comment: 2025-05-14 08:23:29.939336
# Keep-alive comment: 2025-05-14 19:23:29.632127
# Keep-alive comment: 2025-05-15 06:23:30.825600
# Keep-alive comment: 2025-05-15 17:23:54.982404
# Keep-alive comment: 2025-05-16 04:23:16.336910
# Keep-alive comment: 2025-05-16 15:22:18.734963
# Keep-alive comment: 2025-05-17 02:22:37.922689
# Keep-alive comment: 2025-05-17 13:23:11.631037
# Keep-alive comment: 2025-05-18 00:22:36.477704
# Keep-alive comment: 2025-05-18 11:23:04.574501
# Keep-alive comment: 2025-05-18 22:23:01.868171
# Keep-alive comment: 2025-05-19 09:23:36.580157
# Keep-alive comment: 2025-05-19 20:22:36.236980
# Keep-alive comment: 2025-05-20 07:22:52.331790
# Keep-alive comment: 2025-05-20 18:24:04.511415
# Keep-alive comment: 2025-05-21 05:22:36.950744
# Keep-alive comment: 2025-05-21 16:22:45.323431
# Keep-alive comment: 2025-05-22 03:22:39.437091
# Keep-alive comment: 2025-05-22 14:22:36.007262
# Keep-alive comment: 2025-05-23 01:22:42.260322
# Keep-alive comment: 2025-05-23 12:22:42.205704
# Keep-alive comment: 2025-05-23 23:22:46.744942
# Keep-alive comment: 2025-05-24 10:22:44.904358
# Keep-alive comment: 2025-05-24 21:22:41.496716
# Keep-alive comment: 2025-05-25 08:22:41.082280
# Keep-alive comment: 2025-05-25 19:22:46.689342
# Keep-alive comment: 2025-05-26 06:22:31.718173
# Keep-alive comment: 2025-05-26 17:22:36.181410
# Keep-alive comment: 2025-05-27 04:22:41.790533
# Keep-alive comment: 2025-05-27 15:22:45.545443
# Keep-alive comment: 2025-05-28 02:22:55.557348
# Keep-alive comment: 2025-05-28 13:22:44.032870
# Keep-alive comment: 2025-05-29 00:22:39.993890
# Keep-alive comment: 2025-05-29 11:22:34.714944
# Keep-alive comment: 2025-05-29 22:22:49.484972
# Keep-alive comment: 2025-05-30 09:22:34.112838
# Keep-alive comment: 2025-05-30 20:22:35.046925
# Keep-alive comment: 2025-05-31 07:22:46.895751
# Keep-alive comment: 2025-05-31 18:22:42.426781
# Keep-alive comment: 2025-06-01 05:22:40.839753
# Keep-alive comment: 2025-06-01 16:22:54.326320
# Keep-alive comment: 2025-06-02 03:22:55.740128
# Keep-alive comment: 2025-06-02 14:22:45.841770
# Keep-alive comment: 2025-06-03 01:22:36.731137
# Keep-alive comment: 2025-06-03 12:22:50.511265
# Keep-alive comment: 2025-06-03 23:22:45.076597
# Keep-alive comment: 2025-06-04 10:22:45.976856
# Keep-alive comment: 2025-06-04 21:22:24.552900
# Keep-alive comment: 2025-06-05 08:22:47.466870
# Keep-alive comment: 2025-06-05 19:22:37.514838
# Keep-alive comment: 2025-06-06 06:22:36.450419
# Keep-alive comment: 2025-06-06 17:22:19.476664
# Keep-alive comment: 2025-06-07 04:22:21.334871
# Keep-alive comment: 2025-06-07 15:22:30.868713
# Keep-alive comment: 2025-06-08 02:22:36.097108
# Keep-alive comment: 2025-06-08 13:22:37.660218
# Keep-alive comment: 2025-06-09 00:22:20.526527
# Keep-alive comment: 2025-06-09 11:22:34.963935
# Keep-alive comment: 2025-06-09 22:22:42.921796
# Keep-alive comment: 2025-06-10 09:22:45.990756
# Keep-alive comment: 2025-06-10 20:22:39.321141
# Keep-alive comment: 2025-06-11 07:22:40.404463
# Keep-alive comment: 2025-06-11 18:24:26.931702
# Keep-alive comment: 2025-06-12 05:22:37.573759
# Keep-alive comment: 2025-06-12 16:22:40.694300
# Keep-alive comment: 2025-06-13 03:22:41.971599
# Keep-alive comment: 2025-06-13 14:22:30.930397
# Keep-alive comment: 2025-06-14 01:22:50.839491
# Keep-alive comment: 2025-06-14 12:22:38.429106
# Keep-alive comment: 2025-06-14 23:22:29.525769
# Keep-alive comment: 2025-06-15 10:22:15.246910
# Keep-alive comment: 2025-06-15 21:22:50.292189
# Keep-alive comment: 2025-06-16 08:22:46.538462
# Keep-alive comment: 2025-06-16 19:22:30.669473
# Keep-alive comment: 2025-06-17 06:23:07.544825
# Keep-alive comment: 2025-06-17 17:22:35.348671
# Keep-alive comment: 2025-06-18 04:22:42.218628
# Keep-alive comment: 2025-06-18 15:22:38.664880
# Keep-alive comment: 2025-06-19 02:22:39.604026
# Keep-alive comment: 2025-06-19 13:22:38.443080