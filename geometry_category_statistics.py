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
# Keep-alive comment: 2025-06-20 00:22:36.080446
# Keep-alive comment: 2025-06-20 11:23:25.089960
# Keep-alive comment: 2025-06-20 22:22:45.088326
# Keep-alive comment: 2025-06-21 09:22:30.637654
# Keep-alive comment: 2025-06-21 20:22:42.414312
# Keep-alive comment: 2025-06-22 07:22:35.586785
# Keep-alive comment: 2025-06-22 18:22:26.071683
# Keep-alive comment: 2025-06-23 05:22:42.608216
# Keep-alive comment: 2025-06-23 16:22:35.425748
# Keep-alive comment: 2025-06-24 03:22:42.105341
# Keep-alive comment: 2025-06-24 14:22:20.647493
# Keep-alive comment: 2025-06-25 01:22:15.512474
# Keep-alive comment: 2025-06-25 12:22:36.969589
# Keep-alive comment: 2025-06-25 23:22:40.216274
# Keep-alive comment: 2025-06-26 10:22:47.516795
# Keep-alive comment: 2025-06-26 21:24:11.210812
# Keep-alive comment: 2025-06-27 08:22:40.683050
# Keep-alive comment: 2025-06-27 19:22:37.668494
# Keep-alive comment: 2025-06-28 06:22:45.197270
# Keep-alive comment: 2025-06-28 17:22:35.520492
# Keep-alive comment: 2025-06-29 04:22:24.354393
# Keep-alive comment: 2025-06-29 15:22:15.219310
# Keep-alive comment: 2025-06-30 02:22:36.544672
# Keep-alive comment: 2025-06-30 13:22:17.095274
# Keep-alive comment: 2025-07-01 00:24:22.269836
# Keep-alive comment: 2025-07-01 11:22:37.070330
# Keep-alive comment: 2025-07-01 22:22:41.724350
# Keep-alive comment: 2025-07-02 09:22:35.285513
# Keep-alive comment: 2025-07-02 20:24:24.076189
# Keep-alive comment: 2025-07-03 07:22:50.029712
# Keep-alive comment: 2025-07-03 18:22:14.512841
# Keep-alive comment: 2025-07-04 05:22:38.983189
# Keep-alive comment: 2025-07-04 16:22:35.025324
# Keep-alive comment: 2025-07-05 03:22:34.303393
# Keep-alive comment: 2025-07-05 14:22:39.429204
# Keep-alive comment: 2025-07-06 01:22:36.126606
# Keep-alive comment: 2025-07-06 12:22:33.941277
# Keep-alive comment: 2025-07-06 23:22:35.049945
# Keep-alive comment: 2025-07-07 10:22:35.234580
# Keep-alive comment: 2025-07-07 21:22:33.843949
# Keep-alive comment: 2025-07-08 08:22:39.133666
# Keep-alive comment: 2025-07-08 19:22:34.515947
# Keep-alive comment: 2025-07-09 06:22:46.044212
# Keep-alive comment: 2025-07-09 17:23:18.870955
# Keep-alive comment: 2025-07-10 04:22:34.600708
# Keep-alive comment: 2025-07-10 15:22:39.355534
# Keep-alive comment: 2025-07-11 02:22:33.639931
# Keep-alive comment: 2025-07-11 13:22:34.051614
# Keep-alive comment: 2025-07-12 00:22:20.786083
# Keep-alive comment: 2025-07-12 11:22:39.220768
# Keep-alive comment: 2025-07-12 22:22:35.250414
# Keep-alive comment: 2025-07-13 09:22:35.125050
# Keep-alive comment: 2025-07-13 20:22:19.507873
# Keep-alive comment: 2025-07-14 07:22:30.823330
# Keep-alive comment: 2025-07-14 18:22:54.066402
# Keep-alive comment: 2025-07-15 05:22:45.012217
# Keep-alive comment: 2025-07-15 16:22:39.067364
# Keep-alive comment: 2025-07-16 03:22:39.271510
# Keep-alive comment: 2025-07-16 14:22:39.304242
# Keep-alive comment: 2025-07-17 01:22:34.625354
# Keep-alive comment: 2025-07-17 12:22:40.425661
# Keep-alive comment: 2025-07-17 23:22:33.211762
# Keep-alive comment: 2025-07-18 10:22:54.162772
# Keep-alive comment: 2025-07-18 21:22:34.158659
# Keep-alive comment: 2025-07-19 08:23:14.948121
# Keep-alive comment: 2025-07-19 19:22:19.649766
# Keep-alive comment: 2025-07-20 06:22:44.370613
# Keep-alive comment: 2025-07-20 17:22:50.025009
# Keep-alive comment: 2025-07-21 04:22:44.561156
# Keep-alive comment: 2025-07-21 15:22:30.452400
# Keep-alive comment: 2025-07-22 02:22:53.937187
# Keep-alive comment: 2025-07-22 13:23:06.528237
# Keep-alive comment: 2025-07-23 00:22:41.126833
# Keep-alive comment: 2025-07-23 11:22:30.032236
# Keep-alive comment: 2025-07-23 22:22:33.779999
# Keep-alive comment: 2025-07-24 09:22:49.595893
# Keep-alive comment: 2025-07-24 20:22:35.432914
# Keep-alive comment: 2025-07-25 07:22:29.713272
# Keep-alive comment: 2025-07-25 18:22:34.618955
# Keep-alive comment: 2025-07-26 05:22:30.095255
# Keep-alive comment: 2025-07-26 16:22:34.391604
# Keep-alive comment: 2025-07-27 03:22:29.544225
# Keep-alive comment: 2025-07-27 14:22:19.989136
# Keep-alive comment: 2025-07-28 01:22:40.676422
# Keep-alive comment: 2025-07-28 12:22:35.571098
# Keep-alive comment: 2025-07-28 23:22:34.106929
# Keep-alive comment: 2025-07-29 10:22:08.937067
# Keep-alive comment: 2025-07-29 21:22:39.933492
# Keep-alive comment: 2025-07-30 08:22:36.020995
# Keep-alive comment: 2025-07-30 19:22:44.117643
# Keep-alive comment: 2025-07-31 06:22:49.376467
# Keep-alive comment: 2025-07-31 17:22:34.979326
# Keep-alive comment: 2025-08-01 04:22:33.648984
# Keep-alive comment: 2025-08-01 15:22:44.186134
# Keep-alive comment: 2025-08-02 02:22:29.487963
# Keep-alive comment: 2025-08-02 13:22:39.769338
# Keep-alive comment: 2025-08-03 00:22:35.436444
# Keep-alive comment: 2025-08-03 11:22:40.290938
# Keep-alive comment: 2025-08-03 22:22:34.960607
# Keep-alive comment: 2025-08-04 09:22:31.246366
# Keep-alive comment: 2025-08-04 20:22:34.824460
# Keep-alive comment: 2025-08-05 07:22:37.888552
# Keep-alive comment: 2025-08-05 18:22:39.173640
# Keep-alive comment: 2025-08-06 05:22:34.478875
# Keep-alive comment: 2025-08-06 16:24:24.763088
# Keep-alive comment: 2025-08-07 03:22:39.056057
# Keep-alive comment: 2025-08-07 14:22:39.980598
# Keep-alive comment: 2025-08-08 01:22:29.295178
# Keep-alive comment: 2025-08-08 12:22:40.112337
# Keep-alive comment: 2025-08-08 23:22:40.661663
# Keep-alive comment: 2025-08-09 10:22:34.519336
# Keep-alive comment: 2025-08-09 21:22:56.411148
# Keep-alive comment: 2025-08-10 08:22:40.724129
# Keep-alive comment: 2025-08-10 19:22:40.645507
# Keep-alive comment: 2025-08-11 06:22:34.841853
# Keep-alive comment: 2025-08-11 17:22:39.883774
# Keep-alive comment: 2025-08-12 04:22:39.230466
# Keep-alive comment: 2025-08-12 15:22:30.953748
# Keep-alive comment: 2025-08-13 02:22:40.207031
# Keep-alive comment: 2025-08-13 13:22:35.238615
# Keep-alive comment: 2025-08-14 00:22:33.671760
# Keep-alive comment: 2025-08-14 11:22:40.808787
# Keep-alive comment: 2025-08-14 22:22:34.786903
# Keep-alive comment: 2025-08-15 09:22:34.298774
# Keep-alive comment: 2025-08-15 20:22:24.027917
# Keep-alive comment: 2025-08-16 07:22:49.029684
# Keep-alive comment: 2025-08-16 18:22:34.495968
# Keep-alive comment: 2025-08-17 05:22:38.623756
# Keep-alive comment: 2025-08-17 16:22:33.724117
# Keep-alive comment: 2025-08-18 03:22:34.833439
# Keep-alive comment: 2025-08-18 14:22:35.365484
# Keep-alive comment: 2025-08-19 01:22:34.959412
# Keep-alive comment: 2025-08-19 12:22:40.019341
# Keep-alive comment: 2025-08-19 23:23:01.837965
# Keep-alive comment: 2025-08-20 10:22:35.852385
# Keep-alive comment: 2025-08-20 21:22:39.567011
# Keep-alive comment: 2025-08-21 08:22:36.346314
# Keep-alive comment: 2025-08-21 19:22:40.292153
# Keep-alive comment: 2025-08-22 06:22:40.111549
# Keep-alive comment: 2025-08-22 17:22:35.137713
# Keep-alive comment: 2025-08-23 04:22:44.599916
# Keep-alive comment: 2025-08-23 15:22:33.721962
# Keep-alive comment: 2025-08-24 02:22:33.871063
# Keep-alive comment: 2025-08-24 13:22:34.815823
# Keep-alive comment: 2025-08-25 00:22:41.172973
# Keep-alive comment: 2025-08-25 11:22:39.757704
# Keep-alive comment: 2025-08-25 22:22:34.719292
# Keep-alive comment: 2025-08-26 09:22:35.197341
# Keep-alive comment: 2025-08-26 20:22:39.405770
# Keep-alive comment: 2025-08-27 07:22:44.578784
# Keep-alive comment: 2025-08-27 18:22:14.674264
# Keep-alive comment: 2025-08-28 05:22:44.808315
# Keep-alive comment: 2025-08-28 16:22:34.743553
# Keep-alive comment: 2025-08-29 03:22:19.021814
# Keep-alive comment: 2025-08-29 14:22:24.611571
# Keep-alive comment: 2025-08-30 01:22:24.154362
# Keep-alive comment: 2025-08-30 12:22:19.784504
# Keep-alive comment: 2025-08-30 23:22:23.464715
# Keep-alive comment: 2025-08-31 10:22:19.209283
# Keep-alive comment: 2025-08-31 21:22:30.641999
# Keep-alive comment: 2025-09-01 08:22:32.211560
# Keep-alive comment: 2025-09-01 19:22:30.850251
# Keep-alive comment: 2025-09-02 06:22:19.209214
# Keep-alive comment: 2025-09-02 17:22:30.365077
# Keep-alive comment: 2025-09-03 04:22:23.536352
# Keep-alive comment: 2025-09-03 15:22:25.457991
# Keep-alive comment: 2025-09-04 02:22:29.191385
# Keep-alive comment: 2025-09-04 13:22:34.055216
# Keep-alive comment: 2025-09-05 00:22:20.202322
# Keep-alive comment: 2025-09-05 11:22:14.975385
# Keep-alive comment: 2025-09-05 22:22:24.302399
# Keep-alive comment: 2025-09-06 09:22:20.682234
# Keep-alive comment: 2025-09-06 20:22:19.431235
# Keep-alive comment: 2025-09-07 07:22:25.193251
# Keep-alive comment: 2025-09-07 18:22:25.456446
# Keep-alive comment: 2025-09-08 05:22:21.424649
# Keep-alive comment: 2025-09-08 16:22:25.569553
# Keep-alive comment: 2025-09-09 03:22:50.746499
# Keep-alive comment: 2025-09-09 14:22:25.710888
# Keep-alive comment: 2025-09-10 01:22:18.839532
# Keep-alive comment: 2025-09-10 12:22:30.365178
# Keep-alive comment: 2025-09-10 23:22:19.645972
# Keep-alive comment: 2025-09-11 10:22:22.320369
# Keep-alive comment: 2025-09-11 21:22:20.109001
# Keep-alive comment: 2025-09-12 08:22:34.729926
# Keep-alive comment: 2025-09-12 19:22:25.165417
# Keep-alive comment: 2025-09-13 06:22:14.157725
# Keep-alive comment: 2025-09-13 17:22:20.694266
# Keep-alive comment: 2025-09-14 04:22:10.651169
# Keep-alive comment: 2025-09-14 15:22:21.861806
# Keep-alive comment: 2025-09-15 02:22:19.267219
# Keep-alive comment: 2025-09-15 13:22:20.949183
# Keep-alive comment: 2025-09-16 00:22:19.807244
# Keep-alive comment: 2025-09-16 11:22:25.292937
# Keep-alive comment: 2025-09-16 22:22:19.244191
# Keep-alive comment: 2025-09-17 09:22:21.207629
# Keep-alive comment: 2025-09-17 20:22:30.421503
# Keep-alive comment: 2025-09-18 07:22:26.911006
# Keep-alive comment: 2025-09-18 18:22:26.209738
# Keep-alive comment: 2025-09-19 05:22:20.989894
# Keep-alive comment: 2025-09-19 16:22:55.128717
# Keep-alive comment: 2025-09-20 03:22:25.125223
# Keep-alive comment: 2025-09-20 14:22:25.979220
# Keep-alive comment: 2025-09-21 01:22:25.472518
# Keep-alive comment: 2025-09-21 12:22:25.104514
# Keep-alive comment: 2025-09-21 23:22:20.673798
# Keep-alive comment: 2025-09-22 10:22:22.840353
# Keep-alive comment: 2025-09-22 21:22:19.343674
# Keep-alive comment: 2025-09-23 08:22:20.787265
# Keep-alive comment: 2025-09-23 19:22:26.132179
# Keep-alive comment: 2025-09-24 06:22:20.189130
# Keep-alive comment: 2025-09-24 17:22:24.689028
# Keep-alive comment: 2025-09-25 15:22:30.056498
# Keep-alive comment: 2025-09-26 02:22:25.823638
# Keep-alive comment: 2025-09-26 13:22:29.713994
# Keep-alive comment: 2025-09-26 19:30:57.300528
# Keep-alive comment: 2025-09-27 05:31:03.056152
# Keep-alive comment: 2025-09-27 15:30:57.259422
# Keep-alive comment: 2025-09-28 01:31:01.458879
# Keep-alive comment: 2025-09-28 11:31:02.334509
# Keep-alive comment: 2025-09-28 21:31:01.677166
# Keep-alive comment: 2025-09-29 07:31:07.973253
# Keep-alive comment: 2025-09-29 17:31:17.949661
# Keep-alive comment: 2025-09-30 03:30:56.514529
# Keep-alive comment: 2025-09-30 13:31:02.526630
# Keep-alive comment: 2025-09-30 23:31:21.961778
# Keep-alive comment: 2025-10-01 09:31:28.037060
# Keep-alive comment: 2025-10-01 19:31:01.930326
# Keep-alive comment: 2025-10-02 05:31:31.001763
# Keep-alive comment: 2025-10-02 15:31:28.179065
# Keep-alive comment: 2025-10-03 01:31:01.584003
# Keep-alive comment: 2025-10-03 11:31:22.561456
# Keep-alive comment: 2025-10-03 21:30:56.805502
# Keep-alive comment: 2025-10-04 07:30:57.157776
# Keep-alive comment: 2025-10-04 17:31:06.940352
# Keep-alive comment: 2025-10-05 03:31:01.954566
# Keep-alive comment: 2025-10-05 13:31:06.831886
# Keep-alive comment: 2025-10-05 23:31:27.218306
# Keep-alive comment: 2025-10-06 09:31:32.699002
# Keep-alive comment: 2025-10-06 19:31:03.553050
# Keep-alive comment: 2025-10-07 05:31:04.093839
# Keep-alive comment: 2025-10-07 15:31:25.035031
# Keep-alive comment: 2025-10-08 01:31:02.520219
# Keep-alive comment: 2025-10-08 11:31:03.483437
# Keep-alive comment: 2025-10-08 21:31:03.282410
# Keep-alive comment: 2025-10-09 07:31:05.272378
# Keep-alive comment: 2025-10-09 17:31:04.458553
# Keep-alive comment: 2025-10-10 03:30:52.974814
# Keep-alive comment: 2025-10-10 13:30:43.857715
# Keep-alive comment: 2025-10-10 23:30:57.238949
# Keep-alive comment: 2025-10-11 09:31:03.336305
# Keep-alive comment: 2025-10-11 19:30:56.958825
# Keep-alive comment: 2025-10-12 05:30:59.993092
# Keep-alive comment: 2025-10-12 15:31:04.479392
# Keep-alive comment: 2025-10-13 01:30:58.910924
# Keep-alive comment: 2025-10-13 11:31:30.255203
# Keep-alive comment: 2025-10-13 21:30:53.036689
# Keep-alive comment: 2025-10-14 07:30:56.897911
# Keep-alive comment: 2025-10-14 17:30:59.725332
# Keep-alive comment: 2025-10-15 03:30:57.156252
# Keep-alive comment: 2025-10-15 13:30:58.845394
# Keep-alive comment: 2025-10-15 23:31:02.568933
# Keep-alive comment: 2025-10-16 09:30:58.488428
# Keep-alive comment: 2025-10-16 19:31:04.066153
# Keep-alive comment: 2025-10-17 05:31:03.084903
# Keep-alive comment: 2025-10-17 15:31:19.521677
# Keep-alive comment: 2025-10-18 01:30:58.568840
# Keep-alive comment: 2025-10-18 11:31:23.488563
# Keep-alive comment: 2025-10-18 21:31:33.151621
# Keep-alive comment: 2025-10-19 07:30:52.985325
# Keep-alive comment: 2025-10-19 17:31:28.121909
# Keep-alive comment: 2025-10-20 03:31:25.310198
# Keep-alive comment: 2025-10-20 13:31:03.620708
# Keep-alive comment: 2025-10-20 23:30:58.368924
# Keep-alive comment: 2025-10-21 09:31:03.747129
# Keep-alive comment: 2025-10-21 19:33:03.937864
# Keep-alive comment: 2025-10-22 05:30:59.139162
# Keep-alive comment: 2025-10-22 15:32:04.031134
# Keep-alive comment: 2025-10-23 01:30:58.175828
# Keep-alive comment: 2025-10-23 11:31:10.530461
# Keep-alive comment: 2025-10-23 21:30:59.369744
# Keep-alive comment: 2025-10-24 07:32:19.411978
# Keep-alive comment: 2025-10-24 17:31:09.016479
# Keep-alive comment: 2025-10-25 03:31:03.670714
# Keep-alive comment: 2025-10-25 13:31:27.686776
# Keep-alive comment: 2025-10-25 23:30:59.226894
# Keep-alive comment: 2025-10-26 09:30:52.900707
# Keep-alive comment: 2025-10-26 19:31:29.712225
# Keep-alive comment: 2025-10-27 05:31:09.755729
# Keep-alive comment: 2025-10-27 15:31:24.367997
# Keep-alive comment: 2025-10-28 01:31:02.608547
# Keep-alive comment: 2025-10-28 11:31:04.685835
# Keep-alive comment: 2025-10-28 21:30:53.002475
# Keep-alive comment: 2025-10-29 07:30:59.969052
# Keep-alive comment: 2025-10-29 17:31:08.392179
# Keep-alive comment: 2025-10-30 03:30:58.825597
# Keep-alive comment: 2025-10-30 13:31:29.903591
# Keep-alive comment: 2025-10-30 23:31:04.590841
# Keep-alive comment: 2025-10-31 09:32:19.292943
# Keep-alive comment: 2025-10-31 19:30:54.489730
# Keep-alive comment: 2025-11-01 05:31:03.269446
# Keep-alive comment: 2025-11-01 15:30:52.441148
# Keep-alive comment: 2025-11-02 01:31:03.712422
# Keep-alive comment: 2025-11-02 11:31:05.517484
# Keep-alive comment: 2025-11-02 21:31:19.534144
# Keep-alive comment: 2025-11-03 07:30:59.693823
# Keep-alive comment: 2025-11-03 17:31:03.193713
# Keep-alive comment: 2025-11-04 03:31:03.770125
# Keep-alive comment: 2025-11-04 13:31:30.966094
# Keep-alive comment: 2025-11-04 23:31:22.854117
# Keep-alive comment: 2025-11-05 09:31:34.476105
# Keep-alive comment: 2025-11-05 19:31:03.728645
# Keep-alive comment: 2025-11-06 05:31:29.203000
# Keep-alive comment: 2025-11-06 15:31:16.645005
# Keep-alive comment: 2025-11-07 01:31:01.862416
# Keep-alive comment: 2025-11-07 11:31:05.880529
# Keep-alive comment: 2025-11-07 21:31:05.473918
# Keep-alive comment: 2025-11-08 07:30:53.648852
# Keep-alive comment: 2025-11-08 17:31:09.475882
# Keep-alive comment: 2025-11-09 03:31:43.571664
# Keep-alive comment: 2025-11-09 13:31:04.421022
# Keep-alive comment: 2025-11-09 23:30:54.106554
# Keep-alive comment: 2025-11-10 09:30:59.356737
# Keep-alive comment: 2025-11-10 19:31:15.434515
# Keep-alive comment: 2025-11-11 05:31:00.923066
# Keep-alive comment: 2025-11-11 15:30:58.030471
# Keep-alive comment: 2025-11-12 01:31:06.149039
# Keep-alive comment: 2025-11-12 11:31:07.639189
# Keep-alive comment: 2025-11-12 21:31:24.568093
# Keep-alive comment: 2025-11-13 07:30:47.922099
# Keep-alive comment: 2025-11-13 17:30:59.781602
# Keep-alive comment: 2025-11-14 03:31:06.503595
# Keep-alive comment: 2025-11-14 13:31:27.712904
# Keep-alive comment: 2025-11-14 23:30:59.444050
# Keep-alive comment: 2025-11-15 09:31:03.566858
# Keep-alive comment: 2025-11-15 19:31:08.837632
# Keep-alive comment: 2025-11-16 05:31:00.154775
# Keep-alive comment: 2025-11-16 15:31:05.117134
# Keep-alive comment: 2025-11-17 01:30:54.588763
# Keep-alive comment: 2025-11-17 11:31:28.422351
# Keep-alive comment: 2025-11-17 21:30:54.495624
# Keep-alive comment: 2025-11-18 07:30:58.618251
# Keep-alive comment: 2025-11-18 17:30:59.109595
# Keep-alive comment: 2025-11-19 03:31:02.988814
# Keep-alive comment: 2025-11-19 13:30:54.932510
# Keep-alive comment: 2025-11-19 23:30:57.473820
# Keep-alive comment: 2025-11-20 09:31:04.762763
# Keep-alive comment: 2025-11-20 19:32:54.204611
# Keep-alive comment: 2025-11-21 05:31:00.071030
# Keep-alive comment: 2025-11-21 15:31:04.562038
# Keep-alive comment: 2025-11-22 01:31:08.950460
# Keep-alive comment: 2025-11-22 11:30:54.090630
# Keep-alive comment: 2025-11-22 21:31:04.481322
# Keep-alive comment: 2025-11-23 07:31:05.325805
# Keep-alive comment: 2025-11-23 17:31:05.688544
# Keep-alive comment: 2025-11-24 03:30:58.783140
# Keep-alive comment: 2025-11-24 13:30:54.528746
# Keep-alive comment: 2025-11-24 23:31:04.876247
# Keep-alive comment: 2025-11-25 09:31:26.280210
# Keep-alive comment: 2025-11-25 19:31:00.271513
# Keep-alive comment: 2025-11-26 05:31:08.859356
# Keep-alive comment: 2025-11-26 15:31:07.837107
# Keep-alive comment: 2025-11-27 01:31:03.876594
# Keep-alive comment: 2025-11-27 11:31:00.584196
# Keep-alive comment: 2025-11-27 21:30:55.023520
# Keep-alive comment: 2025-11-28 07:30:53.727837
# Keep-alive comment: 2025-11-28 17:31:04.882489
# Keep-alive comment: 2025-11-29 03:30:59.768566
# Keep-alive comment: 2025-11-29 13:31:09.987578
# Keep-alive comment: 2025-11-29 23:30:59.353343
# Keep-alive comment: 2025-11-30 09:31:01.786747
# Keep-alive comment: 2025-11-30 19:30:49.984091
# Keep-alive comment: 2025-12-01 05:30:49.458148
# Keep-alive comment: 2025-12-01 15:30:55.522063
# Keep-alive comment: 2025-12-02 01:30:39.514167
# Keep-alive comment: 2025-12-02 11:31:01.482478
# Keep-alive comment: 2025-12-02 21:31:03.322346
# Keep-alive comment: 2025-12-03 07:31:01.084846
# Keep-alive comment: 2025-12-03 17:31:08.547463
# Keep-alive comment: 2025-12-04 03:30:58.483804
# Keep-alive comment: 2025-12-04 13:30:56.080462
# Keep-alive comment: 2025-12-04 23:30:59.018884
# Keep-alive comment: 2025-12-05 09:30:58.958418
# Keep-alive comment: 2025-12-05 19:30:53.876523
# Keep-alive comment: 2025-12-06 05:30:59.967642
# Keep-alive comment: 2025-12-06 15:30:46.866576
# Keep-alive comment: 2025-12-07 01:30:56.035254
# Keep-alive comment: 2025-12-07 11:30:59.447964
# Keep-alive comment: 2025-12-07 21:30:55.767344
# Keep-alive comment: 2025-12-08 07:31:09.140425
# Keep-alive comment: 2025-12-08 17:30:53.883844
# Keep-alive comment: 2025-12-09 03:30:59.153020
# Keep-alive comment: 2025-12-09 13:30:57.558901
# Keep-alive comment: 2025-12-09 23:30:59.507554
# Keep-alive comment: 2025-12-10 09:31:00.540170
# Keep-alive comment: 2025-12-10 19:31:05.157275
# Keep-alive comment: 2025-12-11 05:30:39.996935
# Keep-alive comment: 2025-12-11 15:31:01.253297
# Keep-alive comment: 2025-12-12 01:30:59.145895
# Keep-alive comment: 2025-12-12 11:30:45.181879
# Keep-alive comment: 2025-12-12 21:31:04.658487
# Keep-alive comment: 2025-12-13 07:30:58.872980
# Keep-alive comment: 2025-12-13 17:31:00.596649
# Keep-alive comment: 2025-12-14 03:31:02.875000
# Keep-alive comment: 2025-12-14 13:30:58.572086
# Keep-alive comment: 2025-12-14 23:30:53.524732
# Keep-alive comment: 2025-12-15 09:30:58.603599
# Keep-alive comment: 2025-12-15 19:30:58.311569
# Keep-alive comment: 2025-12-16 05:31:06.450602
# Keep-alive comment: 2025-12-16 15:30:53.478510
# Keep-alive comment: 2025-12-17 01:31:24.511709
# Keep-alive comment: 2025-12-17 11:30:53.694606
# Keep-alive comment: 2025-12-17 21:34:08.798949
# Keep-alive comment: 2025-12-18 07:30:59.987667
# Keep-alive comment: 2025-12-18 17:31:07.475095
# Keep-alive comment: 2025-12-19 03:31:02.661401
# Keep-alive comment: 2025-12-19 13:30:57.747872
# Keep-alive comment: 2025-12-19 23:31:38.375909
# Keep-alive comment: 2025-12-20 09:30:44.108805
# Keep-alive comment: 2025-12-20 19:30:59.562041
# Keep-alive comment: 2025-12-21 05:30:58.113908
# Keep-alive comment: 2025-12-21 15:30:42.972629
# Keep-alive comment: 2025-12-22 01:30:57.419810
# Keep-alive comment: 2025-12-22 11:31:00.215957
# Keep-alive comment: 2025-12-22 21:30:43.937266
# Keep-alive comment: 2025-12-23 07:31:01.020960
# Keep-alive comment: 2025-12-23 17:31:03.024614
# Keep-alive comment: 2025-12-24 03:30:49.678690
# Keep-alive comment: 2025-12-24 13:30:44.659577
# Keep-alive comment: 2025-12-24 23:30:51.886612
# Keep-alive comment: 2025-12-25 09:31:05.210642
# Keep-alive comment: 2025-12-25 19:30:58.826039
# Keep-alive comment: 2025-12-26 05:30:59.016123
# Keep-alive comment: 2025-12-26 15:30:58.097533
# Keep-alive comment: 2025-12-27 01:30:52.323891
# Keep-alive comment: 2025-12-27 11:30:57.604901
# Keep-alive comment: 2025-12-27 21:30:58.618333
# Keep-alive comment: 2025-12-28 07:30:58.180215
# Keep-alive comment: 2025-12-28 17:31:05.333524
# Keep-alive comment: 2025-12-29 03:30:53.062171
# Keep-alive comment: 2025-12-29 13:30:59.680433
# Keep-alive comment: 2025-12-29 23:30:53.886406
# Keep-alive comment: 2025-12-30 09:30:44.072609
# Keep-alive comment: 2025-12-30 19:31:02.539250
# Keep-alive comment: 2025-12-31 05:30:54.949024
# Keep-alive comment: 2025-12-31 15:30:55.900827
# Keep-alive comment: 2026-01-01 01:31:04.766004
# Keep-alive comment: 2026-01-01 11:31:00.017772
# Keep-alive comment: 2026-01-01 21:31:11.300234
# Keep-alive comment: 2026-01-02 07:31:01.372242
# Keep-alive comment: 2026-01-02 17:30:58.463125
# Keep-alive comment: 2026-01-03 03:30:56.059919
# Keep-alive comment: 2026-01-03 13:31:00.822682
# Keep-alive comment: 2026-01-03 23:31:02.560260
# Keep-alive comment: 2026-01-04 09:30:54.754263
# Keep-alive comment: 2026-01-04 19:31:00.972793
# Keep-alive comment: 2026-01-05 05:30:59.635552
# Keep-alive comment: 2026-01-05 15:31:04.444390
# Keep-alive comment: 2026-01-06 01:30:54.075080
# Keep-alive comment: 2026-01-06 11:30:55.428986
# Keep-alive comment: 2026-01-06 21:30:54.901093
# Keep-alive comment: 2026-01-07 07:30:54.370475
# Keep-alive comment: 2026-01-07 17:30:53.362643
# Keep-alive comment: 2026-01-08 03:31:02.160683
# Keep-alive comment: 2026-01-08 13:30:55.567640
# Keep-alive comment: 2026-01-08 23:30:54.027746
# Keep-alive comment: 2026-01-09 09:30:54.779345
# Keep-alive comment: 2026-01-09 19:30:59.335519
# Keep-alive comment: 2026-01-10 05:31:03.530283
# Keep-alive comment: 2026-01-10 15:30:48.730083
# Keep-alive comment: 2026-01-11 01:30:55.839111
# Keep-alive comment: 2026-01-11 11:31:04.379814
# Keep-alive comment: 2026-01-11 21:30:58.873984
# Keep-alive comment: 2026-01-12 07:31:00.862473
# Keep-alive comment: 2026-01-12 17:30:58.094247
# Keep-alive comment: 2026-01-13 03:30:56.145778
# Keep-alive comment: 2026-01-13 13:30:50.195475
# Keep-alive comment: 2026-01-13 23:31:03.025234
# Keep-alive comment: 2026-01-14 09:30:55.647470
# Keep-alive comment: 2026-01-14 19:30:59.405945
# Keep-alive comment: 2026-01-15 05:30:59.105615
# Keep-alive comment: 2026-01-15 15:31:00.935543
# Keep-alive comment: 2026-01-16 01:31:02.958446
# Keep-alive comment: 2026-01-16 11:31:10.203452
# Keep-alive comment: 2026-01-16 21:30:57.877256
# Keep-alive comment: 2026-01-17 07:30:43.319541
# Keep-alive comment: 2026-01-17 17:30:58.463950
# Keep-alive comment: 2026-01-18 03:30:59.537783
# Keep-alive comment: 2026-01-18 13:30:54.341788
# Keep-alive comment: 2026-01-18 23:31:03.770879
# Keep-alive comment: 2026-01-19 09:31:02.167052
# Keep-alive comment: 2026-01-19 19:30:57.560411