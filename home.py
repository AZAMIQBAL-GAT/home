from datetime import date, timedelta
import requests
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
from streamlit_option_menu import option_menu
import streamlit as st
import hvplot.pandas
import holoviews as hv
import matplotlib.pyplot as plt
import datetime as dt
from requests.auth import HTTPBasicAuth
from io import BytesIO
import pandas as pd
import io
import panel as pn
from bs4 import BeautifulSoup

pn.extension("tabulator", template="material", sizing_mode="stretch_width")

#   Page configuration
st.set_page_config(
    page_title="DAYWISE GRAPH",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)
# ya code sa uper wali space area hota ha wo remove ho jata ha
# reduce_header_height_style = """
#     <style>
#         div.block-container {padding-top:1rem;}
#     </style>
# """
# st.markdown(reduce_header_height_style, unsafe_allow_html=True)
# AZAM CODE Feature 1 Minimalize the Defaut (ap hide kar sakty ho header and footer jis pa streamlit likha hota ha)
hide_menu_style = """
    <style>
    MainMenue {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Define the URL
# url = 'https://r.udhaar.pk/u/Plpzwm'

# # Fetch the data from the URL
# response = requests.get(url)
# data = response.text

# # Display the raw data to inspect it
# st.text(data)

# # If the data is in CSV format, convert it to a pandas DataFrame
# try:
#     df = pd.read_csv(io.StringIO(data))
#     # Display the DataFrame in Streamlit
#     st.dataframe(df)
# except Exception as e:
#     st.error(f"Error loading data into DataFrame: {e}")


# Define the URL
url = 'https://r.udhaar.pk/u/Plpzwm'

# Fetch the data from the URL
response = requests.get(url)
html_data = response.text

# Parse the HTML data using BeautifulSoup
soup = BeautifulSoup(html_data, 'html.parser')

# Extract the data rows
rows = soup.find_all('tr', class_='clickable-row')

# Create a list to hold the extracted data
data = []

# Loop through each row and extract the relevant information
for row in rows:
    date_time_amount_divs = row.find_all(
        'div', class_='dateandTimeAmountColumnOne')
    balance_amount_divs = row.find_all('div', class_='balanceAmountColumnOne')
    note_box_divs = row.find_all('div', class_='noteBoxColumnOne')

    # Extract date, time, and amount
    date = date_time_amount_divs[0].find_all('div')[0].text.strip()
    time = date_time_amount_divs[0].find_all('div')[1].text.strip()
    balance = balance_amount_divs[0].find(
        'p', class_='orangeShade').text.strip()
    note = note_box_divs[0].find('p', class_='udhaar-note').text.strip()
    amount = row.find_all('td')[2].text.strip()

    # Append the extracted data to the list
    data.append([date, time, balance, note, amount])

# Create a DataFrame from the extracted data
df = pd.DataFrame(data, columns=['Date', 'Time', 'Balance', 'Note', 'Amount'])


# Clean the 'Amount' column (remove 'Rs.', commas, and whitespace)
df['Amount'] = df['Amount'].str.replace(
    'Rs.', '').str.replace(',', '').str.strip().astype(float)

# Filter rows where the note is 'Butt sab advance' and sum the 'Amount' column
# total_amount = df[df['Note'] == 'Butt sab advance']['Amount'].sum()
# Define the list of notes to sum the amounts for
notes_to_sum = ['Butt sab advance', 'Butt sab advance///Rakshwa go ka saman',
                'Butt sab advance/2.5/4905/5/8693']

# Sum the amounts for the specified notes
total_amount = df[df['Note'].isin(notes_to_sum)]['Amount'].sum()
# st.write(f"Total Amount for Butt sab advance: Rs. {total_amount}")
# Calculate the remaining amount
total_to_pay = 560000
st.write(f"Total Amount Butt sab: {total_to_pay}")
st.write(f"Advance Butt sab: {total_amount}")
remaining_amount = total_to_pay - total_amount
st.write(f"Remaining Amount to Pay: {remaining_amount}")

# Extract unique categories before the first slash ("/") in 'Note'
df['Category'] = df['Note'].str.split('/').str[0]


# Define the categories you want to filter
# categories_to_show = [
#     'Butt sab advance',
#     'Butt sab advance///Rakshwa go ka saman',
#     'Butt sab advance/2.5/4905/5/8693'
# ]

# Filter the DataFrame
# 1st method
# filtered_df = df[df['Category'].isin(categories_to_show)]
# 2nd method
# filtered_df = df[df['Category'].str.startswith('Butt sab advance', case=False)]
# 3rd method
filtered_df = df[df['Category'].str.contains(
    r'^butt sab advance', case=False, na=False)]


# Display the DataFrame in Streamlit
st.dataframe(filtered_df)

gb = GridOptionsBuilder.from_dataframe(filtered_df)
gb.configure_pagination(paginationAutoPageSize=True)  # Add pagination
gb.configure_side_bar()  # Add a sidebar
# gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
gridOptions = gb.build()

grid_response = AgGrid(
    filtered_df,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT',
    update_mode='MODEL_CHANGED',
    fit_columns_on_grid_load=False,
    # theme='blue', #Add theme color to the table
    enable_enterprise_modules=True,
    height=540,
    width='100%',
    reload_data=True
)
