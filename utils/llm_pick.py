from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv

load_dotenv()

def pick_llm(level: str):

    if level.lower() == "low":
        return ChatMistralAI(
            model="ministral-3b-2512",
            temperature=0
        )

    elif level.lower() == "medium":
        return ChatMistralAI(
            model="mistral-small-2603",
            temperature=0
        )

    elif level.lower() == "high":
        return ChatMistralAI(
            model="mistral-large-2512",
            temperature=0
        )

    else:
        raise ValueError("Choose low, medium, or high")


# llm = pick_llm("low")

# response = llm.invoke("What is the capital of Pakistan?")
# print(response.content)