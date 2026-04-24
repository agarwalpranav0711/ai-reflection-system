import streamlit as st
import requests

st.set_page_config(page_title="AI Brain", page_icon="🧠")

st.title("🧠 AI Brain Chat")

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# input box
if prompt := st.chat_input("Ask something..."):

    # show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # call API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            response = requests.post(
                "http://127.0.0.1:8000/ask",
                params={"question": prompt}
            )

            data = response.json()

            answer = data.get("final_answer", "Error")
            confidence = data.get("confidence", 0)

            # display answer
            st.markdown(answer)

            # display confidence
            st.caption(f"Confidence: {confidence}%")

    # save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"{answer}\n\nConfidence: {confidence}%"
    })