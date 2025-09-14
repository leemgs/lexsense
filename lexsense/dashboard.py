"""Streamlit dashboard – browse reports with a simple role toggle."""
import os, requests, pandas as pd, streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.set_page_config(page_title="LexSense Dashboard", page_icon="📊", layout="wide")
st.title("LexSense Regulatory Monitoring Dashboard")
st.write("This is a reproducible demo of the LexSense pipeline.")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

if not st.session_state.logged_in:
    st.subheader("Sign in (Demo)")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["analyst", "guest"], index=0)
    if st.button("Sign in"):
        if password == "lexsense":
            st.session_state.logged_in = True
            st.session_state.role = role
            st.success(f"Signed in as {role}")
        else:
            st.error("Invalid credentials.")
    st.stop()

st.sidebar.markdown(f"**User:** {st.session_state.role}")
st.sidebar.markdown("**Status:** Logged In")

def fetch_reports():
    try:
        r = requests.get(f"{BACKEND_URL}/reports"); r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Failed to fetch reports: {e}")
        return []

data = fetch_reports()
if not data:
    st.info("No reports available.")
else:
    st.subheader("🔎 Reports")
    hide_entities = (st.session_state.role == "guest")
    rows = []
    for item in data:
        rows.append({
            "Title": item.get("title", ""),
            "Date": item.get("date", ""),
            "Category": item.get("category", ""),
            "Summary": item.get("summary", ""),
            "Entities": "Hidden (no permission)" if hide_entities else ", ".join(item.get("entities", [])),
        })
    st.table(rows)

    st.subheader("📈 Category distribution")
    counts = {}
    for item in data:
        cat = item.get("category", "Unknown")
        counts[cat] = counts.get(cat, 0) + 1
    chart_df = pd.DataFrame(list(counts.items()), columns=["Category", "Count"]).sort_values("Count", ascending=False)
    st.bar_chart(chart_df.set_index("Category"))

    st.subheader("📄 Detail view")
    options = {f"{i['title']} ({i['id']})": i['id'] for i in data}
    selected = st.selectbox("Select a report", list(options.keys()))
    sid = options.get(selected)
    if sid:
        try:
            d = requests.get(f"{BACKEND_URL}/reports/{sid}").json()
            st.markdown(f"**Title:** {d.get('title','')}")
            st.markdown(f"**Date:** {d.get('date','')}")
            st.markdown(f"**Category:** {d.get('category','')}")
            if not hide_entities:
                st.markdown(f"**Entities:** {', '.join(d.get('entities', []))}")
            st.markdown("**Summary:**"); st.write(d.get('summary',''))
            if st.session_state.role == "analyst":
                st.markdown("**Full Text:**"); st.write(d.get('text',''))
            else:
                st.markdown("*Full text requires analyst role.*")
        except Exception as e:
            st.error(f"Failed to fetch detail: {e}")
