import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# Create a sample dataframe
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [24, 27, 22, 32],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
}
df = pd.DataFrame(data)

# Set up the page
st.title("Streamlit AgGrid Example")
st.write("This is an example of displaying a dataframe using st_aggrid.")

# Configure AgGrid options
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination()
gb.configure_default_column(groupable=True)
grid_options = gb.build()

# Display the dataframe using AgGrid
AgGrid(df, gridOptions=grid_options)





# df = pd.read_csv(
#     'https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv')
# AgGrid(df)
