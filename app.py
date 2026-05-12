
import streamlit as st
import pandas as pd
import random
from datetime import datetime, date
import bcrypt
from supabase import create_client

# ── PAGE CONFIG ──────────────────────────────
st.set_page_config(
    page_title="Soft Life System",
    page_icon="🌸",
    layout="centered"
)

# ── CONNECT TO SUPABASE ───────────────────────
SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── STYLING ───────────────────────────────────
st.markdown("""
<style>
.stApp { background-color: #fffafc; }
h1, h2, h3 { color: #5c3b52; font-family: Georgia, serif; }
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
[data-testid="stMetric"] {
    background-color: #fff0f5;
    padding: 15px;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "page" not in st.session_state:
    st.session_state.page = "home"

# ── HELPER FUNCTIONS ──────────────────────────
def hash_password(password):
    return bcrypt.hashpw(
        password.encode(), bcrypt.gensalt()
    ).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(
        password.encode(), hashed.encode()
    )

def register_user(name, email, password):
    try:
        result = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {"name": name}
            }
        })
        if result.user:
            return True, "Account created successfully"
        return False, "Could not create account"
    except Exception as e:
        return False, str(e)

def login_user(email, password):
    try:
        result = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if result.user:
            return True, {
                "id": result.user.id,
                "name": result.user.user_metadata.get(
                    "name", email
                ),
                "email": email
            }
        return False, "Could not sign in"
    except Exception as e:
        return False, str(e)

def calculate_score(energy, habits, sleep, water, mood):
    score = (energy * 5) + (habits * 5) + (sleep * 4) + (water * 2)
    mood_scores = {
        "Happy": 10, "Calm": 8, "Peaceful": 10,
        "Motivated": 9, "Grateful": 8, "Tired": -5,
        "Sad": -7, "Anxious": -8, "Lonely": -6,
        "Burnt Out": -12, "Overwhelmed": -12,
        "Emotionally Drained": -10
    }
    score += mood_scores.get(mood, 0)
    return max(0, min(100, score))

# ── ONBOARDING PAGE ───────────────────────────
def show_onboarding():
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #fce7f3, #fdf2f8);
        padding: 40px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 20px;
    ">
        <h1 style="color:#5c3b52;">🌸 Soft Life System</h1>
        <p style="font-size:18px; color:#6b4c63;">
            Your daily wellness companion
        </p>
        <p style="color:#6b4c63;">
            Track your emotions · Build gentle habits ·
            Protect your peace
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### How it works")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background:#fff0f5;padding:20px;
        border-radius:15px;text-align:center;">
            <h2>1️⃣</h2>
            <b>Check In Daily</b>
            <p style="font-size:13px;">Track your mood,
            energy, sleep and habits</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:#f0fff4;padding:20px;
        border-radius:15px;text-align:center;">
            <h2>2️⃣</h2>
            <b>See Your Patterns</b>
            <p style="font-size:13px;">Understand your
            energy and emotional trends</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background:#fff8f0;padding:20px;
        border-radius:15px;text-align:center;">
            <h2>3️⃣</h2>
            <b>Build Your Soft Life</b>
            <p style="font-size:13px;">Use insights to
            design routines that actually work</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌸 Create Account", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()
    with col2:
        if st.button("✨ Sign In", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

# ── LOGIN PAGE ────────────────────────────────
def show_login():
    st.markdown("""
    <div style="text-align:center;margin-bottom:30px;">
        <h1>🌸 Welcome Back</h1>
        <p style="color:#6b4c63;">
            Sign in to your soft life space
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Email address")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button(
            "Sign In", use_container_width=True
        )
        if submit:
            if email and password:
                success, result = login_user(email, password)
                if success:
                    st.session_state.user = result["name"]
                    st.session_state.user_id = result["id"]
                    st.session_state.page = "app"
                    st.rerun()
                else:
                    st.error(result)
            else:
                st.warning("Please fill in all fields")

    if st.button("No account yet? Create one"):
        st.session_state.page = "register"
        st.rerun()

# ── REGISTER PAGE ─────────────────────────────
def show_register():
    st.markdown("""
    <div style="text-align:center;margin-bottom:30px;">
        <h1>🌸 Join the Soft Life</h1>
        <p style="color:#6b4c63;">
            Create your private wellness space
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("register_form"):
        name = st.text_input("Your name")
        email = st.text_input("Email address")
        password = st.text_input("Password", type="password")
        confirm = st.text_input(
            "Confirm password", type="password"
        )
        submit = st.form_submit_button(
            "Create Account", use_container_width=True
        )
        if submit:
            if name and email and password and confirm:
                if password != confirm:
                    st.error("Passwords do not match")
                elif len(password) < 6:
                    st.error(
                        "Password must be at least 6 characters"
                    )
                else:
                    success, msg = register_user(
                        name, email, password
                    )
                    if success:
                        st.success(msg)
                        st.info("Please sign in now")
                        st.session_state.page = "login"
                        st.rerun()
                    else:
                        st.error(msg)
            else:
                st.warning("Please fill in all fields")

    if st.button("Already have an account? Sign in"):
        st.session_state.page = "login"
        st.rerun()

# ── MAIN APP ──────────────────────────────────
def show_app():
    user_name = st.session_state.user
    user_id = st.session_state.user_id

    # Sidebar
    st.sidebar.markdown(
        f"### 🌸 Hello, {user_name}!"
    )
    st.sidebar.markdown("---")

    page = st.sidebar.radio("Navigate", [
        "🏠 Daily Check-In",
        "🌅 Morning Ritual",
        "🌙 Evening Wind-Down",
        "✨ Habit Stacks",
        "📊 My Insights",
        "📋 Weekly Reset",
        "📖 Module Progress",
    ])

    tips = [
        "Drink more water today 💧",
        "Rest is productive 🌸",
        "Protect your peace 🕊️",
        "Small progress matters 💫",
        "Take deep breaths 🌿",
        "You are enough 💛",
        "Slow down and breathe 🌸",
    ]
    st.sidebar.info(random.choice(tips))
    st.sidebar.markdown("---")

    if st.sidebar.button("Sign Out"):
        st.session_state.user = None
        st.session_state.user_id = None
        st.session_state.page = "home"
        st.rerun()

    # ── DAILY CHECK-IN ────────────────────────
    if page == "🏠 Daily Check-In":
        st.markdown("""
        <div style="
            background:linear-gradient(135deg,#fce7f3,#fdf2f8);
            padding:30px;border-radius:25px;
            margin-bottom:20px;">
            <h1 style="color:#5c3b52;">🌸 Daily Check-In</h1>
            <p style="color:#6b4c63;">
                How are you showing up today, beautiful? 💛
            </p>
        </div>
        """, unsafe_allow_html=True)

        affirmations = [
            "Peace is productive.",
            "You are allowed to rest.",
            "Softness is strength.",
            "You do not have to rush your life.",
            "Your feelings are valid.",
            "You are doing better than you think.",
        ]
        st.info("✨ " + random.choice(affirmations))

        with st.form("checkin_form"):
            st.subheader("How are you feeling today?")
            mood = st.selectbox("Mood", [
                "Happy", "Calm", "Peaceful", "Motivated",
                "Grateful", "Tired", "Sad", "Anxious",
                "Lonely", "Burnt Out", "Overwhelmed",
                "Emotionally Drained"
            ])
            col1, col2 = st.columns(2)
            with col1:
                energy = st.slider("Energy Level", 1, 10, 5)
                sleep = st.slider("Hours Slept", 0, 12, 7)
                water = st.slider("Water Intake (cups)", 0, 10, 4)
            with col2:
                habits = st.slider("Habits Completed", 0, 5, 0)
                cycle = st.selectbox("Cycle Phase", [
                    "Not Tracking", "Menstrual",
                    "Follicular", "Ovulation", "Luteal"
                ])
            journal = st.text_area(
                "Your reflection for today 🌿",
                placeholder=(
                    "How are you really feeling? "
                    "What do you need today?"
                ),
                height=120
            )
            submit = st.form_submit_button(
                "Save My Day 🌸", use_container_width=True
            )

            if submit:
                score = calculate_score(
                    energy, habits, sleep, water, mood
                )
                supabase.table("wellness_data").insert({
                    "user_id": user_id,
                    "date": str(date.today()),
                    "mood": mood,
                    "energy": energy,
                    "sleep": sleep,
                    "water": water,
                    "habits": habits,
                    "cycle": cycle,
                    "score": score,
                    "journal": journal
                }).execute()

                if score >= 75:
                    st.success(
                        f"Wellness Score: {score}/100 — "
                        "You are in a strong place today 💫"
                    )
                elif score >= 55:
                    st.info(
                        f"Wellness Score: {score}/100 — "
                        "You are doing okay. Keep going gently."
                    )
                elif score >= 35:
                    st.warning(
                        f"Wellness Score: {score}/100 — "
                        "Take things slow today."
                    )
                else:
                    st.error(
                        f"Wellness Score: {score}/100 — "
                        "You may need deep rest today. "
                        "That is okay."
                    )

    # ── MORNING RITUAL ────────────────────────
    elif page == "🌅 Morning Ritual":
        st.markdown("""
        <div style="
            background:linear-gradient(135deg,#fff8e7,#fffdf0);
            padding:30px;border-radius:25px;
            margin-bottom:20px;">
            <h1 style="color:#5c3b52;">🌅 Morning Ritual</h1>
            <p style="color:#6b4c63;">
                How did you begin your day? 🌸
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.info(
            "Your morning ritual has 5 pillars. "
            "Tick what you completed today."
        )

        with st.form("morning_form"):
            st.subheader("The 5 Pillars")
            col1, col2 = st.columns(2)
            with col1:
                silence = st.checkbox(
                    "🤫 Silence — no screens for first 20 min"
                )
                body = st.checkbox(
                    "🌿 Body — water, movement, nourishment"
                )
                mind = st.checkbox(
                    "🧠 Mind — journaling, reading, intentions"
                )
            with col2:
                spirit = st.checkbox(
                    "✨ Spirit — prayer, meditation, gratitude"
                )
                presence = st.checkbox(
                    "🌸 Presence — one moment of sensory joy"
                )

            menu = st.selectbox(
                "Which morning menu did you use?",
                ["10 min — Minimum", "30 min — Balanced",
                 "60 min — Full Nourishment", "Custom"]
            )
            notes = st.text_area(
                "How did your morning feel?",
                placeholder=(
                    "Describe how your morning went today..."
                )
            )
            submit = st.form_submit_button(
                "Save Morning Ritual 🌅",
                use_container_width=True
            )

            if submit:
                pillars = sum([
                    silence, body, mind, spirit, presence
                ])
                supabase.table("morning_rituals").insert({
                    "user_id": user_id,
                    "date": str(date.today()),
                    "silence": silence,
                    "body": body,
                    "mind": mind,
                    "spirit": spirit,
                    "presence": presence,
                    "menu_used": menu,
                    "notes": notes
                }).execute()

                if pillars == 5:
                    st.success(
                        "All 5 pillars completed! "
                        "Your morning was full 🌟"
                    )
                elif pillars >= 3:
                    st.success(
                        f"{pillars}/5 pillars — "
                        "A nourishing morning 🌸"
                    )
                elif pillars >= 1:
                    st.info(
                        f"{pillars}/5 pillars — "
                        "You showed up. That counts 💛"
                    )
                else:
                    st.warning(
                        "Tomorrow is a new morning. "
                        "It starts tonight 🌙"
                    )

    # ── EVENING WIND-DOWN ─────────────────────
    elif page == "🌙 Evening Wind-Down":
        st.markdown("""
        <div style="
            background:linear-gradient(135deg,#f0e6ff,#fdf2f8);
            padding:30px;border-radius:25px;
            margin-bottom:20px;">
            <h1 style="color:#5c3b52;">🌙 Evening Wind-Down</h1>
            <p style="color:#6b4c63;">
                Close your day with intention 🌸
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("evening_form"):
            col1, col2 = st.columns(2)
            with col1:
                digital_sunset = st.checkbox(
                    "📵 Digital Sunset — screens off"
                )
                body_care = st.checkbox(
                    "🛁 Body Care — skincare, stretching"
                )
            with col2:
                sleep_quality = st.slider(
                    "Expected sleep quality tonight", 1, 10, 7
                )

            brain_dump = st.text_area(
                "🧠 Brain Dump — offload everything here",
                placeholder=(
                    "Tasks for tomorrow, worries to release, "
                    "anything on your mind..."
                ),
                height=120
            )
            gratitude = st.text_area(
                "💛 Gratitude — one specific thing today",
                placeholder=(
                    "Be specific — not just 'my family' "
                    "but what exactly..."
                )
            )
            intention = st.text_input(
                "🌅 Intention for tomorrow",
                placeholder="Tomorrow I will focus on..."
            )

            submit = st.form_submit_button(
                "Close My Day 🌙", use_container_width=True
            )

            if submit:
                supabase.table("evening_rituals").insert({
                    "user_id": user_id,
                    "date": str(date.today()),
                    "digital_sunset": digital_sunset,
                    "body_care": body_care,
                    "brain_dump": brain_dump,
                    "gratitude": gratitude,
                    "tomorrow_intention": intention,
                    "sleep_quality": sleep_quality
                }).execute()
                st.success(
                    "Your day is closed. Rest well 🌙"
                )
                st.info(
                    '"The day is closed. I did enough. '
                    'I am enough. I rest."'
                )

    # ── HABIT STACKS ──────────────────────────
    elif page == "✨ Habit Stacks":
        st.markdown("""
        <div style="
            background:linear-gradient(135deg,#e6fff0,#f0fff8);
            padding:30px;border-radius:25px;
            margin-bottom:20px;">
            <h1 style="color:#5c3b52;">✨ My Habit Stacks</h1>
            <p style="color:#6b4c63;">
                After I [anchor], I will [new habit] 🌿
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Show existing stacks
        existing = supabase.table("habit_stacks").select(
            "*"
        ).eq("user_id", user_id).execute()

        if existing.data:
            st.subheader("Your current stacks")
            for stack in existing.data:
                col1, col2, col3 = st.columns([3, 3, 1])
                with col1:
                    st.info(
                        f"🔗 After: {stack['anchor_habit']}"
                    )
                with col2:
                    st.success(
                        f"✨ I will: {stack['new_habit']}"
                    )
                with col3:
                    st.metric(
                        "Streak", f"{stack['streak']}🔥"
                    )
        else:
            st.info(
                "No habit stacks yet. "
                "Create your first one below! 🌿"
            )

        st.markdown("---")
        st.subheader("Add a new habit stack")

        with st.form("habit_form"):
            anchor = st.text_input(
                "After I... (existing habit)",
                placeholder="make my morning tea"
            )
            new_habit = st.text_input(
                "I will... (new habit)",
                placeholder="write 3 lines in my journal"
            )
            submit = st.form_submit_button(
                "Add Stack ✨", use_container_width=True
            )

            if submit:
                if anchor and new_habit:
                    supabase.table("habit_stacks").insert({
                        "user_id": user_id,
                        "anchor_habit": anchor,
                        "new_habit": new_habit,
                        "streak": 0,
                        "last_completed": str(date.today())
                    }).execute()
                    st.success(
                        "Habit stack added! 🌸 "
                        "Come back tomorrow to mark it done."
                    )
                    st.rerun()
                else:
                    st.warning("Please fill in both fields")

    # ── MY INSIGHTS ───────────────────────────
    elif page == "📊 My Insights":
        st.markdown("""
        <div style="
            background:linear-gradient(135deg,#fce7f3,#fdf2f8);
            padding:30px;border-radius:25px;
            margin-bottom:20px;">
            <h1 style="color:#5c3b52;">📊 My Soft Life Insights</h1>
            <p style="color:#6b4c63;">
                Take a gentle look at your patterns 💛
            </p>
        </div>
        """, unsafe_allow_html=True)

        data = get_wellness_data(user_id)

        if data.empty:
            st.info(
                "No data yet. Complete your first "
                "daily check-in to see insights! 🌸"
            )
        else:
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(
                    "Days Tracked", len(data)
                )
            with col2:
                st.metric(
                    "Avg Wellness",
                    f"{data['score'].mean():.0f}/100"
                )
            with col3:
                st.metric(
                    "Avg Energy",
                    f"{data['energy'].mean():.1f}/10"
                )
            with col4:
                st.metric(
                    "Avg Sleep",
                    f"{data['sleep'].mean():.1f}hrs"
                )

            st.markdown("---")

            if len(data) >= 3:
                st.subheader("📈 Wellness Score Trend")
                st.line_chart(
                    data.set_index("date")[["score"]]
                )
                st.subheader("⚡ Energy Trend")
                st.line_chart(
                    data.set_index("date")[["energy"]]
                )
            else:
                st.info(
                    f"Track for {3-len(data)} more days "
                    "to see your trend charts 📈"
                )

            st.markdown("---")
            st.subheader("😊 Mood Distribution")
            mood_counts = data["mood"].value_counts()
            st.bar_chart(mood_counts)

            top_mood = data["mood"].mode()[0]
            st.info(f"Your most frequent mood: {top_mood} 🌸")

            st.markdown("---")

            # Burnout alert
            if len(data) >= 3:
                recent_score = data["score"].tail(3).mean()
                if recent_score < 40:
                    st.error(
                        "⚠️ Your recent wellness scores suggest "
                        "you may be heading toward burnout. "
                        "Please slow down and rest."
                    )
                elif recent_score >= 70:
                    st.success(
                        "🌟 Your recent wellness is strong. "
                        "Keep protecting this energy!"
                    )

            # Streak
            st.markdown("---")
            st.subheader("🔥 Wellness Streak")
            data["date"] = pd.to_datetime(data["date"])
            unique_dates = data[
                "date"
            ].dt.date.drop_duplicates().sort_values()
            streak = 1
            if len(unique_dates) > 1:
                for i in range(len(unique_dates)-1, 0, -1):
                    diff = (
                        unique_dates.iloc[i] -
                        unique_dates.iloc[i-1]
                    ).days
                    if diff == 1:
                        streak += 1
                    else:
                        break
            st.success(f"🔥 Current streak: {streak} day(s)")

    # ── WEEKLY RESET ──────────────────────────
    elif page == "📋 Weekly Reset":
        st.markdown("""
        <div style="
            background:linear-gradient(135deg,#e6f0ff,#f0f5ff);
            padding:30px;border-radius:25px;
            margin-bottom:20px;">
            <h1 style="color:#5c3b52;">📋 Weekly Reset</h1>
            <p style="color:#6b4c63;">
                Set your week with intention 🌸
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("weekly_form"):
            week_of = st.date_input("Week of")
            wins = st.text_area(
    "🏆 My 3 wins from last week",
    placeholder=(
        "1. \n"
        "2. \n"
        "3."
    )
)
            anchor_task = st.text_input(
                "⚓ My anchor task this week",
                placeholder=(
                    "The one most important thing..."
                )
            )
            intention = st.text_input(
                "🌸 My weekly intention",
                placeholder=(
                    "A quality or feeling, not a task..."
                )
            )
            rest_day = st.selectbox(
                "😴 My rest day this week",
                ["Monday", "Tuesday", "Wednesday",
                 "Thursday", "Friday", "Saturday", "Sunday"]
            )
            release = st.text_area(
                "🍃 What I am releasing from last week",
                placeholder="Let it go here..."
            )
            joy = st.text_input(
                "💛 One thing I will do purely for joy",
                placeholder="Something just for me..."
            )
            submit = st.form_submit_button(
                "Set My Week 🌸", use_container_width=True
            )

            if submit:
                supabase.table("weekly_resets").insert({
                    "user_id": user_id,
                    "week_of": str(week_of),
                    "wins": wins,
                    "anchor_task": anchor_task,
                    "weekly_intention": intention,
                    "rest_day": rest_day,
                    "release": release,
                    "joy_activity": joy
                }).execute()
                st.success("Your week is set with intention 🌸")
                st.balloons()

    # ── MODULE PROGRESS ───────────────────────
    elif page == "📖 Module Progress":
        st.markdown("""
        <div style="
            background:linear-gradient(135deg,#fff5e6,#fffaf0);
            padding:30px;border-radius:25px;
            margin-bottom:20px;">
            <h1 style="color:#5c3b52;">📖 Workbook Progress</h1>
            <p style="color:#6b4c63;">
                Track your journey through the
                Soft Life System workbook 🌸
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.info(
            "Working through the Soft Life System workbook? "
            "Track your module progress here!"
        )

        modules = [
            (1, "Know Your Foundation"),
            (2, "Emotional Wellness Framework"),
            (3, "Your Soft Morning Ritual"),
            (4, "Energy-Based Productivity"),
            (5, "Habit Building Without Overwhelm"),
            (6, "Self-Care Architecture"),
            (7, "Spiritual Consistency"),
            (8, "Evening Wind-Down Ritual"),
            (9, "Weekly Monthly and Seasonal Rhythms"),
            (10, "Your Complete Soft Life System"),
        ]

        existing = supabase.table("module_progress").select(
            "*"
        ).eq("user_id", user_id).execute()

        completed_modules = [
            m["module_number"]
            for m in existing.data
            if m["completed"]
        ] if existing.data else []

        total = len(completed_modules)
        st.progress(total/10)
        st.caption(f"{total}/10 modules completed 🌸")

        st.markdown("---")

        for num, name in modules:
            col1, col2, col3 = st.columns([1, 5, 2])
            with col1:
                st.markdown(f"**{num}**")
            with col2:
                if num in completed_modules:
                    st.success(f"✅ {name}")
                else:
                    st.markdown(f"⭕ {name}")
            with col3:
                if num not in completed_modules:
                    if st.button(
                        "Mark Done",
                        key=f"mod_{num}"
                    ):
                        supabase.table(
                            "module_progress"
                        ).insert({
                            "user_id": user_id,
                            "module_number": num,
                            "module_name": name,
                            "completed": True,
                            "completed_at": datetime.now(
                            ).isoformat()
                        }).execute()
                        st.rerun()
                else:
                    st.markdown("✨ Done!")

        if total == 10:
            st.balloons()
            st.success(
                "🎉 You completed the entire Soft Life System! "
                "You are extraordinary."
            )

# ── ROUTER ────────────────────────────────────
if st.session_state.page == "home":
    show_onboarding()
elif st.session_state.page == "login":
    show_login()
elif st.session_state.page == "register":
    show_register()
elif st.session_state.page == "app":
    show_app()
