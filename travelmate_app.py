
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv("travel_data.csv")

df = load_data()

# 💫 TITLE + INTRO
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🌍 TravelMate: Explore India on a Budget</h1>", unsafe_allow_html=True)
st.markdown("##### 🎒 Plan your next trip based on your budget and travel style.")
st.markdown("---")

# 📋 Sidebar Input Section
st.sidebar.header("🧳 Enter Your Travel Preferences")
budget = st.sidebar.slider("💰 Select your total budget (in ₹)", 500, 5000, 1500)
trip_type = st.sidebar.selectbox("🌄 Choose type of destination", ['any', 'beach', 'mountain', 'heritage', 'hill station'])

# 🔍 Filter based on input
filtered_df = df[df['total_cost'] <= budget]
if trip_type != 'any':
    filtered_df = filtered_df[filtered_df['type'] == trip_type]

# 📊 Show Results
st.subheader(f"📌 Places you can visit under ₹{budget}")
if not filtered_df.empty:
    st.dataframe(filtered_df[['destination', 'state', 'type', 'total_cost']])
else:
    st.warning("😔 No destinations found within this budget. Try increasing it or choosing another type.")

# 📈 Cost Breakdown Chart
if not filtered_df.empty:
    st.markdown("### 🧾 Cost Breakdown per Destination")
    chart_df = filtered_df[['destination', 'food_cost', 'stay_cost', 'activity_cost']]
    st.bar_chart(chart_df.set_index('destination'))

# 🗺️ Show Map
if not filtered_df.empty:
    st.markdown("### 🗺️ Explore on Map")
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=4)
    for _, row in filtered_df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"{row['destination']} - ₹{row['total_cost']}",
            tooltip=row['destination']
        ).add_to(m)
    folium_static(m)

# 📌 Footer
st.markdown("---")
st.markdown("💡 Made with ❤️ using Streamlit · [View Source on GitHub](https://github.com/yourusername/travelmate-app)")
