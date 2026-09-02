from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    client = Groq(api_key=os.getenv("Gorq_Key"))
    while True:
        user_input = input("Enter your message(you):")
        if user_input == "exit":
            break
        response = client.chat.completions.create(
            model=os.getenv("model_name"),
            messages=[
                {'role':'user','content':user_input},
                {'role':'system','content':"""assumes your are a AI chatbot which takes input meesage and respond politely
                """}
            ],
            temperature=0.2,
            max_tokens=100
        )
        print(f"AI Bot: {response.choices[0].message.content}")


if __name__ == "__main__":
    main()