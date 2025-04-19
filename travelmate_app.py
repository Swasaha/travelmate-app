# Generate a final clean version of the travel recommendation app with styled layout, explanations, and real system feel

final_app_code = '''
import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(page_title="TravelMate: Travel Recommendation System", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("travel_data.csv")

df = load_data()

# Title and Introduction
st.markdown("<h1 style='text-align: center; color: #009999;'>🌐 TravelMate: Intelligent Travel Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>An interactive system that recommends Indian destinations based on your budget, preferences, and trip duration.</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar inputs
st.sidebar.header("🧭 Plan Your Journey")
budget = st.sidebar.slider("💸 Your Total Budget (₹)", 500, 5000, 1500)
trip_type = st.sidebar.selectbox("🏖️ Select Trip Type", ['any', 'beach', 'mountain', 'heritage', 'hill station'])
days = st.sidebar.slider("📆 Number of Days", 1, 10, 3)

# Calculate total cost for days
df['food_total'] = df['food_cost'] * days
df['stay_total'] = df['stay_cost'] * days
df['total_cost'] = df['food_total'] + df['stay_total'] + df['activity_cost']

# Filter logic
filtered_df = df[df['total_cost'] <= budget]
if trip_type != 'any':
    filtered_df = filtered_df[filtered_df['type'] == trip_type]

# Main recommendations
st.markdown(f"<h3 style='color: #336699;'>🎯 Recommended Destinations under ₹{budget} for {days} day(s)</h3>", unsafe_allow_html=True)

if not filtered_df.empty:
    cols = st.columns(3)
    for idx, (_, row) in enumerate(filtered_df.iterrows()):
        with cols[idx % 3]:
            st.markdown(f"<h4>{row['destination']}</h4>", unsafe_allow_html=True)
            st.write(f"📍 **State**: {row['state']}")
            st.write(f"🧳 **Type**: {row['type']}")
            st.write(f"💰 **Total Estimated Cost**: ₹{int(row['total_cost'])}")
            st.write(f"🍛 Food ({row['food_cost']} per day): ₹{int(row['food_total'])}")
            st.write(f"🏨 Stay ({row['stay_cost']} per day): ₹{int(row['stay_total'])}")
            st.write(f"🎟️ Activities: ₹{row['activity_cost']}")
            st.markdown("---")
else:
    st.warning("⚠️ No destinations match your current selection. Try adjusting your budget or trip type.")

    # Show fallback suggestions
    st.markdown("### 🧠 Closest Matches")
    fallback_df = df[df['total_cost'] <= budget + 500]
    if trip_type != 'any':
        fallback_df = fallback_df[fallback_df['type'] == trip_type]
    fallback_df = fallback_df.head(3)

    if not fallback_df.empty:
        cols = st.columns(3)
        for idx, (_, row) in enumerate(fallback_df.iterrows()):
            with cols[idx % 3]:
                st.markdown(f"<h4>{row['destination']}</h4>", unsafe_allow_html=True)
                st.write(f"📍 **State**: {row['state']}")
                st.write(f"🧳 **Type**: {row['type']}")
                st.write(f"💸 **Estimated Cost**: ₹{int(row['total_cost'])}")
                st.markdown("---")
    else:
        st.info("🚫 No similar places found even with a ₹500 stretch.")

# Footer
st.markdown("---")
st.markdown("<small>🔗 Built with ❤️ using Streamlit · Explore India smartly</small>", unsafe_allow_html=True)
'''

# Save to file
file_path = "/mnt/data/travelmate_final_recommendation_app.py"
with open(file_path, "w") as f:
    f.write(final_app_code)

file_path
