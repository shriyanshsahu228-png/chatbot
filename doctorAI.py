#streamlit run doctorAI.py
import streamlit as st
from google import genai
#from dotenv import load_dotenv
#import os
#load_dotenv()

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
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
    
        with st.spinner("Analyzing your symptoms,Please Hold few seconds..."):

                prompt = f"""
        You are a multilingual professional  AI medical doctor assistant.

        conversation history:
        {st.session_state.history}

        current user message:
        {text}
        Rules:
        - Detect user's language and reply in same language.
        - Be calm, polite and reassuring like a real doctor.
        - Ask follow-up questions if needed.
        - Give simple explanations.
        - Suggest precautions.
        - If symptoms serious → mark EMERGENCY.
        - Suggest which specialist doctor to consult.
        - Never give dangerous advice.

        Format response strictly like:
            1. Understanding of problem
            2. Possible cause
            3. Precautions
            4. When to see doctor
            """

                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt
                        )
                reply = response.text if response.text else "No responce generated"

                st.session_state.history.append(f"Doctor:{reply}")
                st.chat_message("assistant").write(reply)
                                  
                # Emergency detection only
                if "EMERGENCY" in reply.upper():
                    st.error("⚠️ Emergency symptoms detected. Seek medical help immediately.")
