from operator import index

import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "http://localhost:8000"

def analytics():
    col1,col2=st.columns(2)
    with col1:
        start_date=st.date_input("Start Date",datetime(2024,8,1),label_visibility='collapsed')
    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5), label_visibility='collapsed')

    if st.button("Get Analytics"):
        payload ={
            "start_date":start_date.strftime('%Y-%m-%d'),
            "end_date": end_date.strftime('%Y-%m-%d'),
        }

        response =requests.post(f"{API_URL}/analytics/",json=payload)
        response=response.json()

        # st.write(response)

        df=pd.DataFrame({
            "Category":list(response.keys()),
            "Total_expenses":[response[category]['total'] for category in response],
            "Percentage":[response[category]['percentage'] for category in response]
        })

        df_sorted= df.sort_values(by='Percentage',ascending=False).reset_index(drop=True)
        st.subheader("Expense Breakdown By Category")
        st.bar_chart(df_sorted.set_index("Category")['Percentage'],height=400,use_container_width=True)
        df_sorted['Total_expenses'] = df_sorted['Total_expenses'].apply(lambda x: "{:.2f}".format(x))
        df_sorted['Percentage'] = df_sorted['Percentage'].apply(lambda x: "{:.2f}".format(x))
        st.table(df_sorted)
