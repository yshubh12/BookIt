import streamlit as st
import requests

st.title("BookIt-- Appointment Assistant")

with st.expander("📅 View Upcoming Booked Appointments"):
    if st.button("🔍 Show Appointments"):
        try:
            response = requests.get("http://localhost:8000/appointments")
            appts = response.json().get("appointments", [])
            if appts:
                for a in appts:
                    st.markdown(f"✅ {a}")
            else:
                st.info("No upcoming appointments found.")
        except Exception as e:
            st.error("Error loading appointments")
            st.write(e)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.expander("📜 View Full Chat Transcript"):
    for sender, msg in st.session_state.chat_history:
        st.markdown(f"**{sender}:** {msg}")


if "available_slots" not in st.session_state:
    st.session_state.available_slots = []

user_input = st.chat_input("Ask me to book a slot...")

# 🧠 Step 1: Handle user input
if user_input:
    st.session_state.chat_history.append(("You", user_input))

    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={"message": user_input}
        )
        reply = response.json()["response"]
        st.session_state.chat_history.append(("TailorTalk", reply))
    except Exception as e:
        st.error("❌ Backend error")
        st.write(e)

# 🧠 Step 2: If last bot message is asking to book, show slots
last_bot_msg = st.session_state.chat_history[-1][1].lower() if st.session_state.chat_history else ""
if "select one of the available time slots" in last_bot_msg:
    try:
        slot_response = requests.get("http://localhost:8000/slots")
        slots = slot_response.json().get("slots", [])

        if slots:
            st.session_state.available_slots = slots
            slot_dict = {s["readable"]: s["iso"] for s in slots}

            selected_readable = st.selectbox("🕒 Choose a time slot to book:", list(slot_dict.keys()))

            if st.button("✅ Confirm Booking"):
                selected_iso = slot_dict[selected_readable]

                book_response = requests.post(
                    "http://localhost:8000/book",
                    json={"slot": selected_iso}
                )
                if book_response.status_code == 200:
                    st.success(f"✅ Appointment booked for {selected_readable}")
                    st.session_state.chat_history.append(
                        ("TailorTalk", f"✅ Your appointment has been booked for {selected_readable}")
                    )
                    st.session_state.available_slots = []  # Clear after booking
                else:
                    st.error("❌ Booking failed.")
    except Exception as e:
        st.error("❌ Failed to load slots.")
        st.write(e)

# 💬 Step 3: Display full chat history
for sender, msg in st.session_state.chat_history:
    st.chat_message(sender).write(msg)

def get_upcoming_appointments(limit=5):
    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=limit, singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    readable_appointments = []

    for event in events:
        start = event['start'].get('dateTime', '')
        dt = datetime.fromisoformat(start)
        readable = dt.strftime("%A, %B %d at %I:%M %p (UTC)")
        readable_appointments.append(f"{event['summary']} on {readable}")

    return readable_appointments
