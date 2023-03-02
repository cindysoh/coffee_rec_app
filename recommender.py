import streamlit as st
import requests
import json
from model import main_recommender
import pandas as pd
import numpy as np

country_list = pd.read_csv('data/country.csv')
country_list = country_list['0'].sort_values().tolist()
country_list.insert(0, 'None')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    header = st.container()
    tasting_notes = st.container()
    taste_input = st.container()
    origin = st.container()

    with header:
        st.title("Coffee Recommender")

    with st.form(key='my_form'):

        with tasting_notes:
            st.title("Tasting Notes")
            st.text("Type your preference")
            notes = st.text_input("Example: juicy, sweet, bright")

        with taste_input:
            st.title("Taste Rating")
            aroma = st.select_slider(
                'Aroma',
                options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
            acid = st.select_slider(
                'Acid',
                options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
            body = st.select_slider(
                'Body',
                options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
            flavor = st.select_slider(
                'Flavor',
                options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
            aftertaste = st.select_slider(
                'After Taste',
                options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

        with origin:
            st.title("Country Origin")
            st.text("Optional")
            origin_input = st.selectbox('Select country of origin(optional)', country_list)
            if origin_input == 'None':
                origin_input = None

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        recommendation = main_recommender(notes, [[aroma, acid, body, flavor, aftertaste]], origin=origin_input, no_rec=3)
        tab1, tab2, tab3 = st.tabs(["Coffee 1", "Coffee 2", "Coffee 3"])
        tab1.header(recommendation['name'].iloc[0])
        tab1.caption('By ' + recommendation['roaster'].iloc[0])
        tab1.text('Origin: ' + recommendation['origin_country'].iloc[0])
        col1, col2, col3, col4, col5 = tab1.columns(5)
        col1.metric(label="Aroma" , value=recommendation['aroma'].iloc[0])
        col2.metric(label="Acidity", value=recommendation['acid'].iloc[0])
        col3.metric(label="Body", value=recommendation['body'].iloc[0])
        col4.metric(label="Flavor", value=recommendation['flavor'].iloc[0])
        col5.metric(label="After Taste", value=recommendation['aftertaste'].iloc[0])
        tab1.subheader('Information')
        tab1.caption('Origin: ' + recommendation['desc_2'].iloc[0])
        tab1.subheader('Description')
        tab1.caption('Origin: ' + recommendation['desc_1'].iloc[0])

        tab2.header(recommendation['name'].iloc[1])
        tab2.caption('By ' + recommendation['roaster'].iloc[1])
        tab2.text('Origin: ' + recommendation['origin_country'].iloc[1])
        col6, col7, col8, col9, col10 = tab2.columns(5)
        col6.metric(label="Aroma", value=recommendation['aroma'].iloc[1])
        col7.metric(label="Acidity", value=recommendation['acid'].iloc[1])
        col8.metric(label="Body", value=recommendation['body'].iloc[1])
        col9.metric(label="Flavor", value=recommendation['flavor'].iloc[1])
        col10.metric(label="After Taste", value=recommendation['aftertaste'].iloc[1])
        tab2.subheader('Information')
        tab2.caption('Origin: ' + recommendation['desc_2'].iloc[0])
        tab2.subheader('Description')
        tab2.caption('Origin: ' + recommendation['desc_1'].iloc[0])

        tab3.header(recommendation['name'].iloc[2])
        tab3.caption('By ' + recommendation['roaster'].iloc[2])
        tab3.text('Origin: ' + recommendation['origin_country'].iloc[2])
        col11, col12, col13, col14, col15 = tab3.columns(5)
        col11.metric(label="Aroma", value=recommendation['aroma'].iloc[2])
        col12.metric(label="Acidity", value=recommendation['acid'].iloc[2])
        col13.metric(label="Body", value=recommendation['body'].iloc[2])
        col14.metric(label="Flavor", value=recommendation['flavor'].iloc[2])
        col15.metric(label="After Taste", value=recommendation['aftertaste'].iloc[2])
        tab3.subheader('Information')
        tab3.caption('Origin: ' + recommendation['desc_2'].iloc[0])
        tab3.subheader('Description')
        tab3.caption('Origin: ' + recommendation['desc_1'].iloc[0])
        # st.dataframe(recommendation)