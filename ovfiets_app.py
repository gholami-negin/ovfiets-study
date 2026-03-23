"""
OV-fiets Prototype Testing App
Author: Negin Gholami — Block C

HOW TO RUN:
1. Put ovfiets_app.py and the 'screenshots' folder in the SAME folder
2. Open terminal, navigate to that folder
3. Run: streamlit run ovfiets_app.py

FOLDER STRUCTURE:
    my_folder/
        ovfiets_app.py
        screenshots/
            Journey_Planner.png
            Selected_Journey_Details.png
            OV-fiets_forecast.png
            other_options.png
"""

import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="OV-fiets Study", page_icon="🚲", layout="centered")

# ── Find screenshots folder ─────────────────────────────────────
def find_screenshots():
    for p in [Path(__file__).parent / "screenshots",
              Path(os.getcwd()) / "screenshots",
              Path("screenshots")]:
        if p.exists():
            return p
    return None

IMG = find_screenshots()

DARK  = "#001E5A"
BLUE  = "#003082"
GREEN = "#00875A"

st.markdown("""
<style>
    .block-container { max-width: 660px; padding-top: 1.5rem; }
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Session state ────────────────────────────────────────────────
if "step"      not in st.session_state: st.session_state.step = "welcome"
if "condition" not in st.session_state: st.session_state.condition = random.choice(["B","C"])
if "responses" not in st.session_state: st.session_state.responses = {}
if "pid"       not in st.session_state: st.session_state.pid = datetime.now().strftime("%Y%m%d_%H%M%S")

def save(data):
    row = pd.DataFrame([data])
    if os.path.exists("responses.csv"):
        row.to_csv("responses.csv", mode="a", header=False, index=False)
    else:
        row.to_csv("responses.csv", index=False)

def progress_bar(current):
    steps  = ["background","p1","p2","p3"]
    labels = ["About you","Concept 1","Concept 2","Concept 3"]
    pills = ""
    for s, lbl in zip(steps, labels):
        if s == current:
            pills += f"<span style='background:#FFC917;color:{DARK};border-radius:20px;padding:5px 14px;font-size:11px;font-weight:700;margin:0 3px;white-space:nowrap;'>{lbl}</span>"
        elif steps.index(s) < steps.index(current):
            pills += f"<span style='background:{BLUE};color:white;border-radius:20px;padding:5px 14px;font-size:11px;font-weight:700;margin:0 3px;white-space:nowrap;'>✓ {lbl}</span>"
        else:
            pills += f"<span style='background:#E0E7F0;color:#6B7A99;border-radius:20px;padding:5px 14px;font-size:11px;font-weight:700;margin:0 3px;white-space:nowrap;'>{lbl}</span>"
    st.markdown(
        f"<div style='display:flex;justify-content:center;flex-wrap:wrap;gap:4px;margin-top:50px;margin-bottom:20px;'>{pills}</div>",
        unsafe_allow_html=True
    )

def show_screen(filename):
    if IMG is None:
        st.error("📁 **Screenshots folder not found.** Make sure the `screenshots` folder is in the same folder as `ovfiets_app.py`.")
        return
    img_path = IMG / filename
    if img_path.exists():
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.image(str(img_path), use_container_width=True)
    else:
        st.error(f"Image `{filename}` not found in screenshots folder.")

def survey_box():
    st.markdown(
        f"<div style='background:#F8FAFF;border:1.5px solid #C8D4E8;border-radius:12px;"
        f"padding:14px 18px 4px;margin-top:16px;margin-bottom:8px;'>"
        f"<div style='font-size:15px;font-weight:700;color:{DARK};'>Your reaction</div>"
        f"<div style='font-size:12px;color:#6B7A99;margin-bottom:6px;'>No right or wrong answers — be honest.</div>"
        f"</div>", unsafe_allow_html=True
    )

# ══════════════════════════════════════════════════════════════
# WELCOME
# ══════════════════════════════════════════════════════════════
if st.session_state.step == "welcome":
    st.markdown(f"<h2 style='color:{DARK}'>🚲 OV-fiets Design Study</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
Thank you for participating in this study!

**What you will do:**
- Look at **3 design concepts** for the NS OV-fiets bike service
- Answer **a few short questions** after each one
- Takes about **8–10 minutes**

There are no right or wrong answers. Your responses are anonymous
and will only be used for this university research project.
    """)
    if st.button("Start →", type="primary", use_container_width=True):
        st.session_state.step = "background"
        st.rerun()

# ══════════════════════════════════════════════════════════════
# BACKGROUND
# ══════════════════════════════════════════════════════════════
elif st.session_state.step == "background":
    progress_bar("background")
    st.markdown(f"<h3 style='color:{DARK}'>About you</h3>", unsafe_allow_html=True)

    user_type = st.radio("How often do you use OV-fiets (NS shared bikes)?",
        ["Almost never / first time", "A few times a year", "Monthly", "Weekly or more"],
        index=None)
    language  = st.radio("What is your main language?",
        ["Dutch", "English", "Other"], index=None)
    age       = st.radio("Your age group",
        ["Under 18", "18–25", "26–35", "36–50", "Over 50"], index=None)

    if st.button("Continue →", type="primary", use_container_width=True):
        if not all([user_type, language, age]):
            st.warning("Please answer all questions before continuing.")
        else:
            exp  = "new" if user_type in ["Almost never / first time", "A few times a year"] else "experienced"
            lang = "dutch" if language == "Dutch" else "international"
            st.session_state.responses.update({
                "participant_id": st.session_state.pid,
                "p2_condition":   st.session_state.condition,
                "user_type":      exp,
                "language":       lang,
                "age_group":      age,
                "user_type_raw":  user_type,
            })
            st.session_state.step = "p1"
            st.rerun()

# ══════════════════════════════════════════════════════════════
# PROTOTYPE 1 — Journey Planner with OV-fiets integrated
# Tests: Principle 2 (Integrate don't isolate) + Principle 3 (Empower choice)
# ══════════════════════════════════════════════════════════════
elif st.session_state.step == "p1":
    progress_bar("p1")
    st.markdown(f"<div style='display:inline-block;background:{BLUE};color:white;font-size:11px;font-weight:700;text-transform:uppercase;padding:3px 12px;border-radius:20px;margin-bottom:8px;'>Concept 1 of 3</div>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{DARK};margin-top:4px;'>Journey planning with OV-fiets</h3>", unsafe_allow_html=True)
    st.markdown("**Scenario:** You are planning a trip from Amsterdam Amstel to Maximapark. Look at the journey options the NS app shows you:")

    show_screen("Journey_Planner.png")

    st.markdown("*The app shows two route options. One uses OV-fiets and is 10 minutes faster than walking. The app highlights this with a green banner.*")

    survey_box()
    SCALE = ["1 — Not at all","2","3 — Neutral","4","5 — Completely"]

    p1_notice = st.radio(
        "Did you notice the OV-fiets option in the journey list?",
        ["Yes, immediately", "Yes, after looking for it", "Not at first", "No"],
        index=None
    )
    p1_trust = st.radio(
        "\"I trust that the OV-fiets route shown is a realistic option for my journey\"",
        SCALE, index=None, horizontal=True
    )
    p1_control = st.radio(
        "\"I feel in control — I can choose whether to use OV-fiets or not\"",
        SCALE, index=None, horizontal=True
    )
    p1_useful = st.radio(
        "Showing OV-fiets alongside train options in the journey planner is...",
        ["Much less useful than keeping it separate",
         "Slightly less useful",
         "About the same",
         "More useful than keeping it separate",
         "Much more useful than keeping it separate"],
        index=None
    )
    p1_banner = st.radio(
        "The green banner 'OV-fiets saves 10 minutes of walking' felt...",
        ["Unnecessary", "Neutral", "Helpful but not essential", "Clearly helpful"],
        index=None
    )

    st.markdown("---")
    if st.button("Next concept →", type="primary", use_container_width=True):
        if not all([p1_notice, p1_trust, p1_control, p1_useful, p1_banner]):
            st.warning("Please answer all questions before continuing.")
        else:
            st.session_state.responses.update({
                "p1_notice":  p1_notice,
                "p1_trust":   SCALE.index(p1_trust) + 1,
                "p1_control": SCALE.index(p1_control) + 1,
                "p1_useful":  ["Much less useful than keeping it separate","Slightly less useful","About the same","More useful than keeping it separate","Much more useful than keeping it separate"].index(p1_useful) + 1,
                "p1_banner":  p1_banner,
            })
            st.session_state.step = "p2"
            st.rerun()

# ══════════════════════════════════════════════════════════════
# PROTOTYPE 2 — Arrival-time prediction in journey detail
# Tests: Principle 1 (Make uncertainty visible) + Principle 2 (Integrate)
# ══════════════════════════════════════════════════════════════
elif st.session_state.step == "p2":
    progress_bar("p2")
    st.markdown(f"<div style='display:inline-block;background:{BLUE};color:white;font-size:11px;font-weight:700;text-transform:uppercase;padding:3px 12px;border-radius:20px;margin-bottom:8px;'>Concept 2 of 3</div>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{DARK};margin-top:4px;'>Arrival-time bike forecast in journey detail</h3>", unsafe_allow_html=True)
    st.markdown("**Scenario:** You tapped on the OV-fiets route. This is the detailed journey view:")

    show_screen("Selected_Journey_Details.png")

    st.markdown("*The journey detail shows '5-10 Available at the time of arrival' directly in the route timeline — not just current availability.*")

    survey_box()
    SCALE2 = ["1 — Not at all","2","3 — Neutral","4","5 — Completely"]

    p2_understand = st.radio(
        "I understand what '5–10 Available at the time of arrival' means",
        SCALE2, index=None, horizontal=True
    )
    p2_trust = st.radio(
        "\"I trust this prediction about how many bikes will be there when I arrive\"",
        SCALE2, index=None, horizontal=True
    )
    p2_confidence = st.radio(
        "\"This information makes me feel confident enough to include OV-fiets in my journey plan\"",
        SCALE2, index=None, horizontal=True
    )
    p2_placement = st.radio(
        "Showing the bike availability prediction directly inside the journey timeline is...",
        ["Confusing — it doesn't belong here",
         "Neutral",
         "Useful but could be clearer",
         "Exactly the right place to show it"],
        index=None
    )
    p2_comp = st.radio(
        "What do you think '5–10 Available at the time of arrival' means?",
        ["There are exactly 5–10 bikes right now",
         "The app predicts 5–10 bikes will be there when my train arrives",
         "I need to reserve between 5 and 10 bikes",
         "I'm not sure"],
        index=None
    )

    st.markdown("---")
    if st.button("Next concept →", type="primary", use_container_width=True):
        if not all([p2_understand, p2_trust, p2_confidence, p2_placement, p2_comp]):
            st.warning("Please answer all questions before continuing.")
        else:
            correct = "predicts" in p2_comp.lower() or "when my train" in p2_comp.lower()
            st.session_state.responses.update({
                "p2_understand":    SCALE2.index(p2_understand) + 1,
                "p2_trust":         SCALE2.index(p2_trust) + 1,
                "p2_confidence":    SCALE2.index(p2_confidence) + 1,
                "p2_placement":     p2_placement,
                "p2_comprehension": 1 if correct else 0,
            })
            st.session_state.step = "p3"
            st.rerun()

# ══════════════════════════════════════════════════════════════
# PROTOTYPE 3 — Transparency & Confidence screen (B or C)
# Tests: Principle 1 (Make uncertainty visible) + Principle 4 (Own the failure)
# Condition B = forecast only | Condition C = forecast + Why this number + accuracy
# ══════════════════════════════════════════════════════════════
elif st.session_state.step == "p3":
    progress_bar("p3")
    st.markdown(f"<div style='display:inline-block;background:{GREEN};color:white;font-size:11px;font-weight:700;text-transform:uppercase;padding:3px 12px;border-radius:20px;margin-bottom:8px;'>Concept 3 of 3</div>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{DARK};margin-top:4px;'>Bike availability detail screen</h3>", unsafe_allow_html=True)
    st.caption("ℹ️ This is one version of several designs — other participants may see a different version.")

    cond = st.session_state.condition

    if cond == "B":
        st.markdown("**Scenario:** You tap on the OV-fiets section in the journey detail. This screen opens:")
        show_screen("OV-fiets_forecast.png")
        st.markdown("*The screen shows a range (5–10 bikes), a confidence bar (75%), the hourly forecast, and past prediction accuracy.*")
    else:
        st.markdown("**Scenario:** The app warns you that availability is uncertain and shows your options:")
        show_screen("other_options.png")
        st.markdown("*The screen shows 50% confidence (lower reliability), a warning message, and three alternatives: take an earlier train, walk, or use a different OV-fiets location.*")

    survey_box()
    SCALE3 = ["1 — Not at all","2","3 — Neutral","4","5 — Completely"]
    SA    = ["1 — Strongly disagree","2","3 — Neutral","4","5 — Strongly agree"]

    p3_trust = st.radio(
        "\"I trust the availability information shown on this screen\"",
        SCALE3, index=None, horizontal=True
    )
    p3_overload = st.radio(
        "The amount of information on this screen felt...",
        ["Too little — I need more", "About right", "A bit too much", "Way too much"],
        index=None
    )

    if cond == "B":
        p3_forecast = st.radio(
            "The hourly forecast (showing 100/30/10 bikes across the day) is...",
            ["Confusing", "Neutral", "Somewhat useful", "Very useful for planning"],
            index=None
        )
        p3_accuracy = st.radio(
            "Showing the prediction accuracy of the last 7 days makes me...",
            ["Less likely to trust the system",
             "No difference",
             "Slightly more likely to trust it",
             "Much more likely to trust it"],
            index=None
        )
        p3_why = st.radio(
            "Would you tap 'Why this number?' to see the explanation?",
            ["Definitely not", "Probably not", "Maybe", "Probably yes", "Definitely yes"],
            index=None
        )
    else:
        p3_forecast = st.radio(
            "The warning 'Prediction less reliable right now' makes me feel...",
            ["More anxious — I wish it didn't say this",
             "Neutral — doesn't change anything",
             "Reassured — at least it's honest",
             "More in control — I can now plan alternatives"],
            index=None
        )
        p3_accuracy = st.radio(
            "The three alternatives shown (earlier train / walk / other location) are...",
            ["Not useful — I'd rather figure it out myself",
             "Neutral",
             "Somewhat helpful",
             "Very helpful — this is exactly what I need"],
            index=None
        )
        p3_why = st.radio(
            "Compared to an app that shows nothing when predictions are uncertain, this approach is...",
            ["Much worse", "Worse", "About the same", "Better", "Much better"],
            index=None
        )

    p3_control = st.radio(
        "\"After seeing this screen, I feel in control of my travel decision\"",
        SA, index=None, horizontal=True
    )
    p3_open = st.text_area(
        "Anything else you want to tell us about what you saw? (optional)",
        placeholder="Your thoughts, anything confusing, or ideas...", height=80
    )

    st.markdown("---")
    if st.button("Finish →", type="primary", use_container_width=True):
        if not all([p3_trust, p3_overload, p3_forecast, p3_accuracy, p3_why, p3_control]):
            st.warning("Please answer all questions before continuing.")
        else:
            omap = {"Too little — I need more":1,"About right":2,"A bit too much":3,"Way too much":4}
            st.session_state.responses.update({
                "p3_trust":    SCALE3.index(p3_trust) + 1,
                "p3_overload": omap.get(p3_overload),
                "p3_forecast": p3_forecast,
                "p3_accuracy": p3_accuracy,
                "p3_why":      p3_why,
                "p3_control":  SA.index(p3_control) + 1,
                "p3_open":     p3_open,
                "timestamp":   datetime.now().isoformat(),
            })
            save(st.session_state.responses)
            st.session_state.step = "done"
            st.rerun()

# ══════════════════════════════════════════════════════════════
# DONE
# ══════════════════════════════════════════════════════════════
elif st.session_state.step == "done":
    st.balloons()
    st.markdown(f"<h2 style='color:{DARK}'>🎉 Thank you!</h2>", unsafe_allow_html=True)
    st.success("Your responses have been saved.")
    st.markdown("Your input helps improve how OV-fiets communicates bike availability to users.")
    st.markdown("---")
    if st.button("↩ Start new participant session", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()