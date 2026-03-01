import streamlit as st
from google import genai

# API Client configuration
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("Secrets mein GOOGLE_API_KEY nahi mili. Please check karein.")

st.markdown(
    """
    <h1 style="
        text-align: center;
        font-size: 42px;
        background: linear-gradient(to right, #15ea89, #30b478, #7de4b5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        margin-bottom: 30px;
    ">
      WELCOME TO YOUR PERSONAL AI DOCTOR ASSISTANT
    </h1>
    """,
    unsafe_allow_html=True
)

if "history" not in st.session_state:
    st.session_state.history = []

with st.form("doctor_form", clear_on_submit=True):
    text = st.text_input("Describe your symptoms:")
    submitted = st.form_submit_button("Consult")

if submitted and text: 
    st.chat_message("user").write(text)
    st.session_state.history.append(f"user:{text}")                   
    
    with st.spinner("Analyzing your symptoms, Please Hold few seconds..."):
        prompt = f"""
        You are a multilingual professional AI medical doctor assistant.
        Conversation history: {st.session_state.history}
        Current user message: {text}
        Rules:
        - Detect user's language and reply in same language.
        - Be calm, polite and reassuring.
        - Suggest precautions and specialists.
        - If symptoms serious → mark EMERGENCY.
        Format: 1. Understanding, 2. Possible cause, 3. Precautions, 4. When to see doctor.
        """

        try:
            # Gemini API call
            response = client.models.generate_content(
                model="models/gemini-1.5-flash", 
                contents=[prompt]
            )
            
            if response.text:
                reply = response.text
            else:
                reply = "I couldn't generate a response. Please try again."

        except Exception as e:
            # Actual error dikhane ke liye
            st.error(f"Actual Error: {e}")
            reply = "Sorry, an error occurred while processing your request."

        st.session_state.history.append(f"Doctor: {reply}")
        st.chat_message("assistant").write(reply)
                                  
        # Emergency detection
        if "EMERGENCY" in reply.upper():
            st.error("⚠️ Emergency symptoms detected. Seek medical help immediately.")






