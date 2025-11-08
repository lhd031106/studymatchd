import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="StudyMatch", page_icon="📚", layout="wide")

# Initialize session state
if 'sessions' not in st.session_state:
    st.session_state.sessions = [
        {"id": 1, "course": "CS1", "host": "Emma", "spot": "Berry Library", "time": "Today 7pm", "spots": 3, "members": ["Emma"]},
        {"id": 2, "course": "MATH3", "host": "Maya", "spot": "Novak Café", "time": "Tomorrow 2pm", "spots": 2, "members": ["Maya"]},
    ]

if 'user_profile' not in st.session_state:
    st.session_state.user_profile = None

st.title("📚 StudyMatch – Find Your Study Crew")

# Sidebar for profile
with st.sidebar:
    st.header("Your Profile")
    name = st.text_input("Your name", value=st.session_state.user_profile["name"] if st.session_state.user_profile else "")
    year = st.selectbox("Class year", ["25", "26", "27", "28"])
    courses = st.multiselect("Your courses", ["CS1","MATH3","BIO11","CHEM5","ECON1","PSYC6","ENGS21"])
    style = st.radio("Study style", ["quiet", "talk"])
    spot = st.selectbox("Favorite campus spot", ["Berry Library","Novak Café","Sanborn","East Wheelock Lounge"])
    
    if st.button("💾 Save Profile"):
        st.session_state.user_profile = {
            "name": name, 
            "year": year, 
            "courses": courses, 
            "style": style, 
            "spot": spot
        }
        st.success("Profile saved!")

# Main area - tabs
tab1, tab2, tab3 = st.tabs(["🔍 Find Study Buddies", "📅 Active Sessions", "➕ Start a Session"])

# Fake database
data = pd.DataFrame([
    {"name":"Emma","year":"27","courses":["CS1","MATH3"],"style":"quiet","spot":"Berry Library"},
    {"name":"Noah","year":"26","courses":["CS1","ECON1"],"style":"talk","spot":"Novak Café"},
    {"name":"Lily","year":"25","courses":["BIO11","CHEM5"],"style":"quiet","spot":"Sanborn"},
    {"name":"Maya","year":"26","courses":["MATH3","PSYC6"],"style":"quiet","spot":"Berry Library"},
    {"name":"Alex","year":"27","courses":["CS1","ENGS21"],"style":"talk","spot":"Novak Café"},
    {"name":"Sophie","year":"27","courses":["CS1","BIO11"],"style":"quiet","spot":"Berry Library"},
])

with tab1:
    st.subheader("Find Your Study Matches")
    
    if not st.session_state.user_profile or not st.session_state.user_profile.get("courses"):
        st.info("👈 Create your profile in the sidebar first!")
    else:
        user = st.session_state.user_profile
        
        # Filter by class year option
        same_year_only = st.checkbox("Only show classmates (same year)", value=True)
        
        results = []
        for _, r in data.iterrows():
            # Skip self
            if r["name"] == user["name"]:
                continue
                
            # Check year filter
            if same_year_only and r["year"] != user["year"]:
                continue
            
            # Calculate matches
            shared_courses = set(user["courses"]).intersection(r["courses"])
            if not shared_courses:
                continue
                
            score = len(shared_courses) * 2  # Weight courses higher
            if r["style"] == user["style"]:
                score += 1
            if r["spot"] == user["spot"]:
                score += 1
                
            results.append({
                "name": r["name"],
                "year": r["year"],
                "score": score,
                "shared_courses": list(shared_courses),
                "style": r["style"],
                "spot": r["spot"]
            })
        
        if results:
            results.sort(key=lambda x: -x["score"])
            st.success(f"Found {len(results)} potential study buddies!")
            
            for match in results:
                with st.expander(f"✅ **{match['name']}** (Class of '{match['year']}) – Match Score: {match['score']}"):
                    st.write(f"**Shared courses:** {', '.join(match['shared_courses'])}")
                    st.write(f"**Study style:** {match['style']}")
                    st.write(f"**Prefers:** {match['spot']}")
        else:
            st.warning("No matches found. Try adjusting your filters or adding more courses!")

with tab2:
    st.subheader("Active Study Sessions")
    
    if not st.session_state.sessions:
        st.info("No active sessions right now. Start one in the next tab!")
    else:
        for session in st.session_state.sessions:
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.markdown(f"### 📖 {session['course']}")
                    st.write(f"**Host:** {session['host']}")
                    st.write(f"**Members:** {', '.join(session['members'])}")
                
                with col2:
                    st.write(f"📍 {session['spot']}")
                    st.write(f"🕐 {session['time']}")
                
                with col3:
                    st.write(f"**{session['spots']} spots left**")
                    if st.session_state.user_profile and st.session_state.user_profile["name"] not in session['members']:
                        if st.button(f"Join", key=f"join_{session['id']}"):
                            if session['spots'] > 0:
                                session['members'].append(st.session_state.user_profile["name"])
                                session['spots'] -= 1
                                st.rerun()
                
                st.divider()

with tab3:
    st.subheader("Start a New Study Session")
    
    if not st.session_state.user_profile:
        st.info("👈 Create your profile first!")
    else:
        with st.form("new_session"):
            session_course = st.selectbox("Course", st.session_state.user_profile["courses"] if st.session_state.user_profile["courses"] else ["CS1","MATH3","BIO11","CHEM5","ECON1","PSYC6","ENGS21"])
            session_spot = st.selectbox("Location", ["Berry Library","Novak Café","Sanborn","East Wheelock Lounge"])
            session_time = st.selectbox("When", ["Today 2pm", "Today 5pm", "Today 7pm", "Tomorrow 10am", "Tomorrow 2pm", "Tomorrow 7pm"])
            max_people = st.slider("Max group size", 2, 8, 4)
            
            submitted = st.form_submit_button("🚀 Create Session")
            
            if submitted:
                new_session = {
                    "id": len(st.session_state.sessions) + 1,
                    "course": session_course,
                    "host": st.session_state.user_profile["name"],
                    "spot": session_spot,
                    "time": session_time,
                    "spots": max_people - 1,
                    "members": [st.session_state.user_profile["name"]]
                }
                st.session_state.sessions.append(new_session)
                st.success(f"✅ Session created for {session_course}!")