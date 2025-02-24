import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000/api"

# 🟢 Get Events
def get_events():
    response = requests.get(f"{BASE_URL}/events/")
    if response.status_code == 200:
        return response.json()
    return []

def create_event(name, date, location, description, organizer):
    data = {
        "name": name,
        "date": date,
        "location": location,
        "description": description,
        "organizer": organizer  # ✅ Added organizer field
    }
    response = requests.post(f"{BASE_URL}/events/", json=data)
    return response


# 🟢 Get Registrations
def get_registrations():
    response = requests.get(f"{BASE_URL}/registrations/")
    if response.status_code == 200:
        return response.json()
    return []

# 🟢 Register User for Event
def register_user(attendee_name, email, event_id, ticket_count):
    data = {
        "attendee_name": attendee_name,  
        "email": email,
        "ticket_count": ticket_count,  
        "event": event_id
    }
    
    response = requests.post(f"{BASE_URL}/registrations/", json=data)
    return response


# 🟢 Get Feedback
def get_feedback():
    response = requests.get(f"{BASE_URL}/feedbacks/")
    if response.status_code == 200:
        return response.json()
    return []

# 🟢 Submit Feedback
def submit_feedback(attendee_name, comments, rating, event_id):
    data = {"attendee_name": attendee_name, "comments": comments, "rating": rating, "event": event_id}
    return requests.post(f"{BASE_URL}/feedbacks/", json=data)


# 🎯 Streamlit App Layout
st.sidebar.title("🎫 Event Management System")
st.sidebar.write("Use the tabs to navigate.")

tab1, tab2, tab3 = st.tabs(["📅 Events", "📝 Registrations", "⭐ Feedback"])


# 🎉 Events Tab
with tab1:
    st.header("🎉 Events")

    # Display Events
    events = get_events()
    
    if events:
        for event in events:
            st.subheader(event["name"])
            st.write(f"📅 **Date:** {event['date']}")
            st.write(f"📍 **Location:** {event['location']}")
            st.write(f"📝 **Description:** {event['description']}")
            st.write(f"👤 **Organizer:** {event['organizer']}")  # ✅ Display organizer
            st.write("---")
    else:
        st.warning("🚨 No events available.")

    # 🆕 Event Creation Form
    st.subheader("➕ Create a New Event")
    
    with st.form(key="event_form"):
        event_name = st.text_input("Event Name", key="event_name")
        event_date = st.date_input("Date", key="event_date")
        event_location = st.text_input("Location", key="event_location")
        event_description = st.text_area("Description", key="event_description")
        organizer = st.text_input("Organizer Name", key="event_organizer")  # ✅ Added organizer input

        submit_button = st.form_submit_button("Create Event")

        if submit_button:
            if event_name and event_date and event_location and event_description and organizer:
                response = create_event(event_name, str(event_date), event_location, event_description, organizer)
                if response.status_code == 201:
                    st.success("✅ Event created successfully! Refresh to see updates.")
                else:
                    st.error(f"❌ Error: {response.text}")
            else:
                st.warning("⚠️ Please fill out all fields before submitting.")

# 📝 Registrations Tab
with tab2:
    st.header("🎟 Registrations")

    registrations = get_registrations()

    if registrations:
        for reg in registrations:
            st.write(f"👤 {reg.get('attendee_name', 'Unknown')} ({reg.get('email', 'No Email')}) - 🎟 {reg.get('ticket_count', 0)} tickets")
            st.write("---")

    st.subheader("📝 Register for an Event")

    attendee_name = st.text_input("Your Name", key="register_name")
    email = st.text_input("Your Email", key="register_email")
    
    if events:
        selected_event = st.selectbox("Select Event", [(event["id"], event["name"]) for event in events], key="register_event")
        ticket_count = st.number_input("Number of Tickets", min_value=1, step=1, key="register_tickets")

        if st.button("Register"):
            if not attendee_name.strip():
                st.warning("⚠️ Name is required.")
            elif "@" not in email or "." not in email:
                st.warning("⚠️ Please enter a valid email address.")
            elif ticket_count <= 0:
                st.warning("⚠️ Please select at least 1 ticket.")
            else:
                response = register_user(attendee_name, email, selected_event[0], ticket_count)
                if response.status_code == 201:
                    st.success("✅ Successfully registered!")
                else:
                    st.error(f"❌ Error: {response.text}")
    else:
        st.warning("🚨 No events available to register for.")




# ⭐ Feedback Tab
with tab3:
    st.header("⭐ Feedback")
    
    feedbacks = get_feedback()
    
    if feedbacks:
        for fb in feedbacks:
            st.write(f"🗣 **{fb['attendee_name']}** rated **{fb['rating']}/10**")
            st.write(f"💬 {fb['comments']}")
            st.write(f"📅 Submitted on: {fb['submitted_at']}")
            st.write("---")
    else:
        st.warning("🚨 No feedback provided yet.")

    st.subheader("📝 Submit Feedback")
    
    with st.form(key="feedback_form"):
        attendee_name = st.text_input("Your Name", key="feedback_name")
        comments = st.text_area("Your Comments", key="feedback_comments")
        rating = st.slider("Rating (1-10)", min_value=1, max_value=10, key="feedback_rating")
        
        if events:
            selected_event = st.selectbox(
                "Select Event", 
                [(event["id"], event["name"]) for event in events], 
                key="feedback_event"
            )

            submit_feedback_btn = st.form_submit_button("Submit Feedback")

            if submit_feedback_btn:
                if attendee_name and comments and rating and selected_event:
                    response = submit_feedback(attendee_name, comments, rating, selected_event[0])
                    if response.status_code == 201:
                        st.success("✅ Feedback submitted successfully!")
                    else:
                        st.error(f"❌ Error: {response.text}")
                else:
                    st.warning("⚠️ Please fill out all fields before submitting.")
        else:
            st.warning("🚨 No events available to provide feedback for.")