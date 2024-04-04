import streamlit as st
import pydeck as pdk
import pandas as pd

st.set_page_config(page_title='Pothole Detection', page_icon="🚧", layout="wide")


df = pd.read_csv("sydney_suburbs.csv")

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

# Predefined markers for future integration with detection model
markers_data = [
    {"Suburb": "Bondi Beach", "Latitude": -33.89388, "Longitude": 151.2635},
    {"Suburb": "Dundas", "Latitude": -33.800, "Longitude": 151.053},
    {"Suburb": "Parramatta", "Latitude": -33.7952747, "Longitude": 151.0116649},
]

# Convert marker data to pandas DataFrame
markers_df = pd.DataFrame(markers_data)

st.title('Pothole Map')
st.write('No hole left unplugged')

tabs = ["Home", "Map", "Report Pothole"]
selected_tab = st.sidebar.radio("Navigation", tabs)

if selected_tab == "Home":
    st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .small-font {
        font-size:20px !important;
    }
    </style>
    """, unsafe_allow_html=True)


    # Main content
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<div class="big-font">Welcome to Pothole Detection 🚧</div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="small-font">
            Our mission is to make roads safer and smoother by detecting and reporting potholes in your neighborhood. 
            Navigate through our app to explore the map, search for potholes, and even report new ones!
            </div>
        """, unsafe_allow_html=True)
    
        st.markdown('---') 
    
        st.markdown("""
            ## 🗺️ Explore
            Discover and navigate the map to see all reported potholes in the area.
        
            ## 📝 Report
            Found a new pothole? Head over to the Report tab and let us know!
        
            ## 🛠️ Contribute
            Your reports help us improve road safety for everyone. Thank you for your contribution!
        """)

    with col2:
        st.image('./Pothole.jpeg', caption="Together, let's make our roads better!")

    # Add more customisation later

    # Footer
    st.markdown('---')
    st.markdown("""
        <div style="text-align: center;">
            <p>Developed by Xavier Ensor</p>
        </div>
    """, unsafe_allow_html=True)


elif selected_tab == "Map":

    st.markdown("""
    <style>
    .css-18e3th9 {
        padding: 0.5rem 1rem 0.5rem 0;
    }
    .css-1d391kg {
        padding-top: 0;
        padding-bottom: 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Introduction
    st.markdown("""
    ## 🌏 Pothole Detection Map
    Enter a suburb name in the search box below to locate potholes in the area or simply explore the map to view potholes across Sydney.
    """)

    col1, col2 = st.columns([2, 3])

    with col1:
        st.subheader("Suburb Search")
        # Search bar
        search_term = st.text_input("Enter a suburb name:", "")

    if search_term:
        selected_suburb = df[df['Suburb'].str.contains(search_term, case=False)]
        if not selected_suburb.empty:
            selected_lat = selected_suburb['Latitude'].values[0]
            selected_lon = selected_suburb['Longitude'].values[0]
            initial_view_state = pdk.ViewState(latitude=selected_lat, longitude=selected_lon, zoom=14)
            st.success(f"Found {search_term}! Latitude: {selected_lat}, Longitude: {selected_lon}")
        else:
            st.error("Suburb not found.")
            initial_view_state = pdk.ViewState(latitude=-33.8688, longitude=151.2093, zoom=9)
    else:
        initial_view_state = pdk.ViewState(latitude=-33.8688, longitude=151.2093, zoom=9)

    with col2:
        st.subheader("Map")
        # Define a PyDeck view state for map
        view_state = pdk.ViewState(latitude=-33.8688, longitude=151.2093, zoom=10, pitch=0)

        # Define layers for PyDeck map
        layer = pdk.Layer(
            'ScatterplotLayer',
            data=markers_df,
            get_position='[Longitude, Latitude]',
            get_color='[200, 30, 0, 160]',
            get_radius=100,
        )

        # Show PyDeck map
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=initial_view_state,
            layers=[layer],
            tooltip={"html": "<b>Suburb:</b> {Suburb}<br><b>Latitude:</b> {Latitude}<br><b>Longitude:</b> {Longitude}"}
        ))

elif selected_tab == "Report Pothole":
    st.header("Report a Pothole 🕳️")
    st.write("Help improve the community by reporting potholes in your area.")

    # Instructions
    st.subheader("Instructions:")
    st.markdown("""
    1. Enter the suburb where the pothole is located.
    2. Provide the latitude and longitude coordinates of the pothole.
    3. Describe the pothole in detail.
    4. Click the 'Report Pothole' button to submit your report.
    """)

    # Simple form for reporting potholes (improve later)
    with st.form(key='pothole_report_form'):
        st.subheader("Pothole Details:")
        col1, col2 = st.columns(2)
        with col1:
            suburb = st.text_input("Suburb", placeholder="Enter suburb name")
        with col2:
            latitude = st.number_input("Latitude", format="%.5f", help="Enter latitude coordinate")
            longitude = st.number_input("Longitude", format="%.5f", help="Enter longitude coordinate")

        description = st.text_area("Description", placeholder="Describe the pothole (optional)")

        # Submit button
        submit_button = st.form_submit_button(label='Report Pothole')

        if submit_button:
            # Validate inputs
            if not suburb:
                st.error("Please enter the suburb.")
            elif not latitude or not longitude:
                st.error("Please enter both latitude and longitude coordinates.")
            else:
                # Save the report
                st.success(f"Thank you for reporting! A pothole in {suburb} has been logged for review.")
