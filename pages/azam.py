import streamlit as st
import pandas as pd
import os

# Set up the page configuration
st.set_page_config(page_title="Get Location", page_icon=":world_map:")

# JavaScript to get location
get_location_js = """
<script>
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    window.location.search = "?latitude=" + latitude + "&longitude=" + longitude;
}

getLocation();
</script>
"""

# Execute the JavaScript
st.components.v1.html(get_location_js)

# Get the query parameters
query_params = st.experimental_get_query_params()
latitude = query_params.get("latitude", [None])[0]
longitude = query_params.get("longitude", [None])[0]

# Check if latitude and longitude are available
if latitude and longitude:
    st.write(f"Latitude: {latitude}, Longitude: {longitude}")

    # Save the data to a local file
    data_file = "location_data.csv"
    new_data = pd.DataFrame([[latitude, longitude]], columns=["Latitude", "Longitude"])

    if os.path.exists(data_file):
        existing_data = pd.read_csv(data_file)
        data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        data = new_data

    data.to_csv(data_file, index=False)
    st.success("Location data saved successfully!")
else:
    st.write("Click the button to get your location.")
