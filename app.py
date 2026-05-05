import streamlit as st
import pandas as pd
import random
from datetime import datetime
import os

st.set_page_config(page_title="Soft Life System", page_icon="🌸")

st.title("🌸 Soft Life System")
st.write("Welcome back. Take a moment to check in with yourself 💛")

# Affirmations
affirmations = [
    "Peace is productive.",
    "You are allowed to rest.",
    "Softness is strength.",
    "You don’t have to rush your life.",
]
st.info("✨ " + random.choice(affirmations))

# Input
st.subheader("Daily Check-In")

mood = st.selectbox(
    "How are you feeling today?",
    ["Happy", "Calm", "Tired", "Anxious", "Overwhelmed"]
)

energy = st.slider("Energy Level", 1, 10, 5)
habits = st.slider("Habits Completed", 0, 5, 0)

journal = st.text_area("Reflection")

# Score logic
score = (energy * 7) + (habits * 6)

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
        "Habits": habits,
        "Score": score,
        "Journal": journal
    }])

    entry.to_csv("soft_life_data.csv", mode="a", header=False, index=False)
    st.success("Saved successfully 🌸")
    # Dashboard
st.subheader("🌿 Your Soft Life Insights")
st.markdown("Take a gentle look at your patterns 💛")

if os.path.exists("soft_life_data.csv"):
    data = pd.read_csv(
        "soft_life_data.csv",
        names=["Date","Mood","Energy","Habits","Score","Journal"]
    )

    # Charts
    st.subheader("📈 Energy Trend")
    st.line_chart(data.set_index("Date")["Energy"])

    st.subheader("📈 Wellness Score Trend")
    st.line_chart(data.set_index("Date")["Score"])

    st.markdown("---")

    # Weekly Summary
    st.subheader("📊 Weekly Summary")

    if len(data) >= 7:
        last_7 = data.tail(7)

        avg_energy = round(last_7["Energy"].mean(), 1)
        avg_score = round(last_7["Score"].mean(), 1)

        st.metric("Avg Energy (7 days)", avg_energy)
        st.metric("Wellness Score (7 days)", avg_score)
    else:
        st.info("Track at least 7 days to see weekly insights 🌿")

    st.markdown("---")

    # Mood Insight
    st.subheader("🧠 Mood Insights")

    top_mood = data["Mood"].mode()[0]
    st.success(f"Your most frequent mood: {top_mood} 🌸")

    st.markdown("---")

    # Burnout Warning
    if len(data) >= 3:
        if data["Score"].tail(3).mean() < 40:
            st.error("⚠️ You may be heading toward burnout. Slow down and rest.")

    st.markdown("---")

    # Growth Feedback
    if len(data) > 1:
        if data["Score"].iloc[-1] > data["Score"].iloc[0]:
            st.success("You're improving. Keep going 🌸")

else:
    st.info("No data yet. Start your first check-in 🌸")
