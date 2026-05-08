import streamlit as st
import pandas as pd
import random
from datetime import datetime
import os

st.set_page_config(page_title="Soft Life System", page_icon="🌸")

# Premium Styling
st.markdown("""
<style>

.stApp {
    background-color: #fffafc;
}

h1, h2, h3 {
    color: #5c3b52;
    font-family: Georgia, serif;
}

.stButton > button {
    background-color: #f7d6e0;
    color: #5c3b52;
    border-radius: 12px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #efbdd0;
    color: #4a2f40;
}

textarea {
    border-radius: 12px !important;
}

[data-testid="stMetric"] {
    background-color: #fff0f5;
    padding: 15px;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style='
background: linear-gradient(135deg, #fce7f3, #fdf2f8);
padding: 30px;
border-radius: 25px;
margin-bottom: 20px;
box-shadow: 0px 4px 20px rgba(0,0,0,0.05);
'>

<h1 style='color:#5c3b52;'>
🌸 Soft Life System
</h1>

<p style='font-size:18px; color:#6b4c63;'>
Welcome back beautiful 💛<br>
Track your wellness, emotions, habits, and healing journey gently.
</p>

</div>
""", unsafe_allow_html=True)

# Affirmations
affirmations = [
    "Peace is productive.",
    "You are allowed to rest.",
    "Softness is strength.",
    "You don’t have to rush your life.",
]

st.info("✨ " + random.choice(affirmations))

# Daily Check-In
st.subheader("Daily Check-In")

mood = st.selectbox(
    "How are you feeling today?",
    ["Happy", "Calm", "Tired", "Anxious", "Overwhelmed"]
)

energy = st.slider("Energy Level", 1, 10, 5)

sleep = st.slider("Hours Slept", 0, 12, 7)

water = st.slider("Water Intake (cups)", 0, 10, 4)

habits = st.slider("Habits Completed", 0, 5, 0)

cycle = st.selectbox(
    "Cycle Phase",
    ["Not Tracking", "Menstrual", "Follicular", "Ovulation", "Luteal"]
)

journal = st.text_area("Reflection")

# Wellness Score
score = (
    (energy * 5)
    + (habits * 5)
    + (sleep * 4)
    + (water * 2)
)

if mood == "Happy":
    score += 10
elif mood == "Calm":
    score += 8
elif mood == "Tired":
    score -= 5
elif mood == "Anxious":
    score -= 8
elif mood == "Overwhelmed":
    score -= 12

score = max(0, min(100, score))

# Insight
if score >= 75:
    insight = "You are in a strong place today 💫"
elif score >= 55:
    insight = "You're doing okay. Keep going gently."
elif score >= 35:
    insight = "Take things slow today."
else:
    insight = "You may need deep rest today."

st.success(insight)

# Save
if st.button("Save My Day"):

    entry = pd.DataFrame([{
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Mood": mood,
        "Energy": energy,
        "Sleep": sleep,
        "Water": water,
        "Habits": habits,
        "Cycle": cycle,
        "Score": score,
        "Journal": journal
    }])

    file_exists = os.path.exists("soft_life_data.csv")

    entry.to_csv(
        "soft_life_data.csv",
        mode="a",
        header=not file_exists,
        index=False
    )

    st.success("Saved successfully 🌸")

# Dashboard
st.subheader("🌿 Your Soft Life Insights")
st.markdown("Take a gentle look at your patterns 💛")

if os.path.exists("soft_life_data.csv"):

    data = pd.read_csv("soft_life_data.csv")

    # Charts
    st.subheader("📈 Energy Trend")
    st.line_chart(data.set_index("Date")[["Energy"]])

    st.subheader("📈 Wellness Score Trend")
    st.line_chart(data.set_index("Date")[["Score"]])

    st.markdown("---")

    # Mood Insights
    st.subheader("🧠 Mood Insights")

    top_mood = data["Mood"].mode()[0]

    st.success(f"Your most frequent mood: {top_mood} 🌸")

    st.markdown("### Mood Distribution")

    mood_counts = data["Mood"].value_counts()

    st.bar_chart(mood_counts)

    st.caption("This shows how your emotions are distributed over time 💛")

    st.markdown("---")

    # Weekly Summary
    st.subheader("📊 Weekly Summary")

    latest_score = data["Score"].iloc[-1]
    latest_energy = data["Energy"].iloc[-1]
    latest_habits = data["Habits"].iloc[-1]

    col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="
    background:#fff0f5;
    padding:20px;
    border-radius:20px;
    text-align:center;
    box-shadow:0px 4px 15px rgba(0,0,0,0.05);
    ">
        <h3>🌸 Wellness Score</h3>
        <h1>{latest_score}</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
    background:#fef6e4;
    padding:20px;
    border-radius:20px;
    text-align:center;
    box-shadow:0px 4px 15px rgba(0,0,0,0.05);
    ">
        <h3>⚡ Energy Level</h3>
        <h1>{latest_energy}</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
    background:#edf7ed;
    padding:20px;
    border-radius:20px;
    text-align:center;
    box-shadow:0px 4px 15px rgba(0,0,0,0.05);
    ">
        <h3>✅ Habits Done</h3>
        <h1>{latest_habits}</h1>
    </div>
    """, unsafe_allow_html=True)
    if len(data) >= 7:

        last_7 = data.tail(7)

        avg_energy = round(last_7["Energy"].mean(), 1)
        avg_score = round(last_7["Score"].mean(), 1)

        st.metric("Avg Energy (7 days)", avg_energy)
        st.metric("Wellness Score (7 days)", avg_score)

    else:
        st.info("Track at least 7 days to see weekly insights 🌿")

    st.markdown("---")

    # Burnout Alert
    if len(data) >= 3:
        if data["Score"].tail(3).mean() < 40:
            st.error("⚠️ You may be heading toward burnout. Slow down and rest.")

    st.markdown("---")

    # Smart Wellness Feedback
    st.subheader("💛 Wellness Guidance")

    latest_mood = data["Mood"].iloc[-1]

    if latest_mood == "Overwhelmed":
        st.error("🌧️ You seem emotionally overwhelmed today. Try to slow down and protect your peace.")

    elif latest_mood == "Anxious":
        st.warning("🌿 Your mind may need calm today. Rest, hydrate, and avoid pressure.")

    elif latest_mood == "Tired":
        st.info("😴 Your body may be asking for rest. Give yourself permission to pause.")

    elif latest_mood == "Happy":
        st.success("✨ Your energy feels lighter today. Lean into what is making you feel good.")

    elif latest_mood == "Calm":
        st.success("🌸 You seem emotionally grounded today. Protect this peaceful energy.")

    if latest_energy <= 3:
        st.warning("⚡ Your energy level is very low. Prioritize rest and hydration today.")

    elif latest_energy >= 8:
        st.success("💫 Your energy is strong today. Use it gently and intentionally.")

    if latest_score >= 75:
        st.success("🌷 You're currently in a healthy wellness zone.")

    elif latest_score <= 35:
        st.error("💔 Your wellness score is low. Slow down and care for yourself gently.")

else:
    st.info("No data yet. Start your first check-in 🌸")
