# Generate the updated Streamlit code that resembles the "MakeMyTrip"-style layout with destination cards and images

travelmate_mmt_style = '''
import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("travel_data.csv")
    return df

df = load_data()

# Streamlit page config
st.set_page_config(page_title="TravelMate - Explore India", layout="wide")

# UI Title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🌍 TravelMate: Explore India on a Budget</h1>", unsafe_allow_html=True)
st.markdown("##### 🔒 Plan your next trip based on your budget and travel style.")
st.markdown("---")

# Sidebar filters
st.sidebar.header("📘 Enter Your Travel Preferences")
budget = st.sidebar.slider("💰 Select your total budget (in ₹)", 500, 5000, 1500)
trip_type = st.sidebar.selectbox("🏝️ Choose type of destination", ['any', 'beach', 'mountain', 'heritage', 'hill station'])
days = st.sidebar.slider("📅 Number of travel days", 1, 10, 3)

# Cost scaling
df['food_total'] = df['food_cost'] * days
df['stay_total'] = df['stay_cost'] * days
df['total_cost'] = df['food_total'] + df['stay_total'] + df['activity_cost']

# Filter
filtered_df = df[df['total_cost'] <= budget]
if trip_type != 'any':
    filtered_df = filtered_df[filtered_df['type'] == trip_type]

# Main Output
if not filtered_df.empty:
    st.subheader(f"📌 Recommended Trips under ₹{budget} for {days} day(s)")
    cols = st.columns(3)
    for index, (_, row) in enumerate(filtered_df.iterrows()):
        with cols[index % 3]:
            st.image(row.get('image_url', 'https://via.placeholder.com/300x200?text=Image+Not+Available'), use_column_width=True)
            st.markdown(f"<h4>{row['destination']}, <span style='font-weight:normal'>{row['state']}</span></h4>", unsafe_allow_html=True)
            st.markdown(f"🧳 **Total Cost:** ₹{int(row['total_cost'])}")
            st.markdown(f"🍽️ **Food** (₹{row['food_cost']}/day): ₹{int(row['food_total'])}")
            st.markdown(f"🏨 **Stay** (₹{row['stay_cost']}/day): ₹{int(row['stay_total'])}")
            st.markdown(f"🎡 **Activities**: ₹{int(row['activity_cost'])}")
            st.markdown("---")
else:
    st.warning("😕 No destinations match your preferences.")
    
    st.markdown("### 🧠 Suggestions:")
    min_cost = int(df[df['type'] == trip_type]['total_cost'].min()) if trip_type != 'any' else int(df['total_cost'].min())
    extra_needed = min_cost - budget
    if extra_needed > 0:
        st.info(f"💡 Try increasing your budget by ₹{extra_needed} to unlock more destinations.")

    st.markdown("### 🔎 Nearby Matches You Can Consider:")
    fallback_df = df[df['total_cost'] <= budget + 500]
    if trip_type != 'any':
        fallback_df = fallback_df[fallback_df['type'] == trip_type]
    fallback_df = fallback_df.head(3)

    if not fallback_df.empty:
        cols = st.columns(3)
        for index, (_, row) in enumerate(fallback_df.iterrows()):
            with cols[index % 3]:
                st.image(row.get('image_url', 'https://via.placeholder.com/300x200?text=Image+Not+Available'), use_column_width=True)
                st.markdown(f"<h4>{row['destination']}, <span style='font-weight:normal'>{row['state']}</span></h4>", unsafe_allow_html=True)
                st.markdown(f"💵 **Total Cost:** ₹{int(row['total_cost'])}")
                st.markdown(f"🍽️ **Food**: ₹{row['food_cost']}/day")
                st.markdown(f"🏨 **Stay**: ₹{row['stay_cost']}/day")
                st.markdown(f"🎡 **Activities**: ₹{row['activity_cost']}")
                st.markdown("---")
    else:
        st.info("🧳 No close matches found even with a ₹500 stretch.")

# Footer
st.markdown("---")
st.markdown("🔖 <small>Made with ❤️ using Streamlit · <a href='https://github.com/Swasaha/travelmate-app' target='_blank'>View Source on GitHub</a></small>", unsafe_allow_html=True)
'''

# Save this version as a new file
path = "/mnt/data/travelmate_app_makemytrip_style.py"
with open(path, "w") as f:
    f.write(travelmate_mmt_style)

path
