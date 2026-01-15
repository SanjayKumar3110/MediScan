import streamlit as st
from PIL import Image
# We import ONLY the Orchestrator. It handles all other agents/helpers.
from src.orchestrate import Orchestrator 

# Page Configuration
st.set_page_config(page_title="Smart Medical Assistant", layout="centered")
st.title("💊 Smart Medical Assistant")
st.markdown("Upload a prescription to analyze, chat, or find nearby doctors.")

# --- 1. Initialize the Multi-Agent System ---
if 'brain' not in st.session_state:
    # The Orchestrator initializes the MedicalAgent and LocationAgent internally
    st.session_state['brain'] = Orchestrator()

# --- Session State Management ---
if 'extracted_text' not in st.session_state:
    st.session_state['extracted_text'] = None
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# --- Step 1: Image Upload (The "Eyes") ---
uploaded_file = st.file_uploader("Drop your prescription image here", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    # Display the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Prescription', width='content')
    
    # Button to Trigger Analysis
    if st.button("Analyse Prescription"):
        with st.spinner("Orchestrator is assigning tasks..."):
            # ROUTING: We send the image to the Orchestrator.
            # The Orchestrator sees the image and automatically routes it to the MedicalAgent.
            result = st.session_state['brain'].route_request(
                user_input="analyze_image", 
                image=uploaded_file
            )
            
            st.session_state['extracted_text'] = result
            st.success("Extraction Complete!")

# --- Step 2: Interaction (The "Voice") ---
# We display the chat area if we have text OR if the user just wants to chat (optional)
if st.session_state['extracted_text']:
    st.divider()
    st.subheader("📄 Extracted Data")
    
    # Show extracted text (editable)
    text_content = st.text_area("Prescription Content:", 
                                value=st.session_state['extracted_text'], 
                                height=200)
    
    # Update state if user edits manually
    st.session_state['extracted_text'] = text_content

    st.divider()
    st.subheader("💬 Smart Assistant")

    # Chat Interface
    # Note: This single input now handles BOTH Medical questions AND Location searches
    user_question = st.text_input("Ask about meds or 'Find a doctor':")
    
    if st.button("Send Question"):
        if not user_question:
            st.warning("Please type a question.")
        else:
            with st.spinner("Consulting Agents..."):
                # ROUTING: We send the text to the Orchestrator.
                # It will classify the intent:
                # 1. "What is this med?" -> MedicalAgent
                # 2. "Where is a cardiologist?" -> LocationAgent 
                answer = st.session_state['brain'].route_request(
                    user_input=user_question, 
                    context=st.session_state['extracted_text']
                )
                
                # Store chat in history
                st.session_state['chat_history'].append(("User", user_question))
                st.session_state['chat_history'].append(("AI", answer))

    # Display Chat History
    for role, message in reversed(st.session_state['chat_history']):
        if role == "User":
            st.chat_message("user").write(message)
        else:
            st.chat_message("assistant").write(message)