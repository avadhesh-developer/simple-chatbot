import streamlit as st
from dotenv import load_dotenv
from streamlit_chat import message
import requests

  
def init():
    load_dotenv()
    st.set_page_config(page_title="ChatBot",
                       page_icon="🤖",)
  
def main():
    init()
    st.header("Clone ChatBot 🤖")

    if "messages" not in st.session_state:
       st.session_state.messages=[
         {"type":"system","content":"You Are A Helpful Assistant 😊"}
       ]

    user_input=st.chat_input("Your Message 🗣️:",key="user_input")

    if user_input:
        st.session_state.messages.append({"type":"human","content":user_input}) 

        with st.spinner("Thinking...🤔"):
            valid_msg=[m for m in st.session_state.messages if m['type'] in ["system","human"]] 
    
            response=requests.post("http://localhost:8000/chat",json={
                "messages":valid_msg
            })
        if response.status_code == 200 and "response" in response.json():
            ai_reply = response.json()["response"]
            st.session_state.messages.append({"type": "ai", "content": ai_reply})
        else:
            st.error("API error or invalid response")
            st.json(response.json())


    
    for i,msg in enumerate(st.session_state.messages[1:]):
        if msg["type"] == "human":
            message(msg["content"],is_user=True,key=str(i) + '_user')
        elif msg["type"] == "ai":
            message(msg["content"],is_user=False,key=str(i) + '_ai')

    
if __name__ == "__main__":
    main()
                    