
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
# ⏳ Number of days input
days = st.sidebar.slider("📅 Number of travel days", 1, 10, 3)

# 💰 Scale cost by days
df['food_total'] = df['food_cost'] * days
df['stay_total'] = df['stay_cost'] * days
df['total_cost'] = df['food_total'] + df['stay_total'] + df['activity_cost']

# 🔍 Filter destinations
filtered_df = df[df['total_cost'] <= budget]
if trip_type != 'any':
    filtered_df = filtered_df[filtered_df['type'] == trip_type]

# 🎯 Display results
st.subheader(f"📌 Recommended Trips under ₹{budget} for {days} day(s)")

if not filtered_df.empty:
    for _, row in filtered_df.iterrows():
        st.markdown(f"### 🏞️ {row['destination']} ({row['state']})")
        
        st.markdown(f"""
        - 💵 **Total Cost**: ₹{int(row['total_cost'])}  
        - 🍽️ Food (₹{row['food_cost']}/day): ₹{int(row['food_total'])}  
        - 🏨 Stay (₹{row['stay_cost']}/day): ₹{int(row['stay_total'])}  
        - 🎡 Activities: ₹{int(row['activity_cost'])}  
        """)
        st.markdown("---")
else:
    st.warning("No destinations match your preferences. Try adjusting filters.")


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
