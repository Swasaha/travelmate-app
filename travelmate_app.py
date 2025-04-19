%%writefile travelmate_app.py
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

@st.cache_data
def load_data():
    return pd.read_csv("travel_data.csv")

df = load_data()

st.title("🌏 TravelMate: Budget-Friendly Travel Recommender")

st.sidebar.header("🧳 Enter Your Travel Preferences")
budget = st.sidebar.slider("Select your total budget (₹)", 500, 5000, 1500)
trip_type = st.sidebar.selectbox("Choose the type of trip", ['any', 'beach', 'mountain', 'heritage', 'hill station'])

filtered_df = df[df['total_cost'] <= budget]
if trip_type != 'any':
    filtered_df = filtered_df[filtered_df['type'] == trip_type]

st.subheader(f"🔍 Recommendations within ₹{budget}")
if not filtered_df.empty:
    st.dataframe(filtered_df[['destination', 'state', 'type', 'total_cost']])
else:
    st.warning("No destinations found. Try increasing your budget or changing the type.")

if not filtered_df.empty:
    st.subheader("📊 Cost Breakdown of Recommended Places")
    chart_df = filtered_df[['destination', 'food_cost', 'stay_cost', 'activity_cost']]
    st.bar_chart(chart_df.set_index('destination'))

    st.subheader("🗺️ Destination Map")
    map = folium.Map(location=[20.5937, 78.9629], zoom_start=4)
    for _, row in filtered_df.iterrows():
        popup_text = f"{row['destination']} - ₹{row['total_cost']}"
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup_text,
            tooltip=row['destination']
        ).add_to(map)
    folium_static(map)
