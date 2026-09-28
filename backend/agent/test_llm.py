import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY is not configured in .env")


llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0
)


response = llm.invoke(
    "Say exactly: Restaurant AI Agent is connected."
)


print(response.content)