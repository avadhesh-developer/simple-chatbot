from fastapi import FastAPI,Request
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage,SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()

chat = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

app=FastAPI()


class Message(BaseModel):
    type: str
    content: str


class ChatRequest(BaseModel):
    messages:list[Message]

@app.get("/")
def read_root():
    return {"message": "API is running!"} 

@app.post("/chat")
async def chat_endpoint(request:ChatRequest):

    try:
        formatted_msg=[]

        for m in request.messages:
            if m.type== "system":
                formatted_msg.append(SystemMessage(content=m.content))
            elif m.type == "human" :
                formatted_msg.append(HumanMessage(content=m.content))
            else:
                return {"error": f"Invalid message type: {m.type}"}
            
        response=chat.invoke(formatted_msg)
        return {"response":response.content}
    
    except Exception as e:
        return{"error":str(e)}

