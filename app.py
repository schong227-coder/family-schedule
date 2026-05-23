import streamlit as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Set mobile-friendly page config
st.set_page_config(page_title="Family Schedule", layout="centered")
st.title("🗓️ Family Shift Calendar")

# Establish connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 1. Fetch Existing Data
try:
    df = conn.read(ttl="5m") # Cache data for 5 minutes to remain efficient
except Exception:
    df = pd.DataFrame(columns=["Date", "Name", "Shift_Start", "Shift_End", "Notes"])

# 2. Sidebar Filters for Quick Mobile Viewing
st.sidebar.header("Filter View")
member_filter = st.sidebar.selectbox("Select Family Member", ["Everyone"] + list(df["Name"].unique() if not df.empty else []))

# Filter dataframe based on selection
if member_filter != "Everyone" and not df.empty:
    display_df = df[df["Name"] == member_filter]
else:
    display_df = df

# Sort by upcoming date
if not display_df.empty:
    display_df['Date'] = pd.to_datetime(display_df['Date'])
    display_df = display_df.sort_values(by='Date', ascending=True)
    
    st.subheader("Upcoming Roster")
    st.dataframe(display_df.style.format({"Date": lambda t: t.strftime('%Y-%m-%d')}), use_container_width=True)
else:
    st.info("No shifts logged yet. Add one below!")

st.markdown("---")

# 3. Mobile Add-Shift Input Form
st.subheader("➕ Log New Shifts")
with st.form(key="add_shift_form", clear_on_submit=True):
    date_input = st.date_input("Date", datetime.now())
    name_input = st.selectbox("Family Member", ["Member A", "Member B", "Member C", "Member D"])
    
    # Quick select common options for your family parameters
    shift_type = st.radio("Shift Type", ["Fixed Day (7:30 AM - 4:00 PM)", "12-Hour Day", "12-Hour Night", "Custom"])
    
    notes = st.text_input("Notes (e.g., 'Need vehicle priority')")
    
    submit_button = st.form_submit_with_rows_action = st.form_submit_button(label="Submit Shift")
    
    if submit_button:
        # Determine standard hours based on selection
        if "Fixed" in shift_type:
            start, end = "07:30 AM", "04:00 PM"
        elif "12-Hour Day" in shift_type:
            start, end = "07:00 AM", "07:00 PM"
        elif "12-Hour Night" in shift_type:
            start, end = "07:00 PM", "07:00 AM"
        else:
            start, end = "Variable", "Variable"
            
        # Create new row entry
        new_row = pd.DataFrame([{
            "Date": date_input.strftime('%Y-%m-%d'),
            "Name": name_input,
            "Shift_Start": start,
            "Shift_End": end,
            "Notes": notes
        }])
        
        # Append and write back to Google Sheet securely
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(data=updated_df)
        st.success(f"Shift successfully added for {name_input}!")
        st.rerun()