from dotenv import load_dotenv
import os
from groq import Groq
## add required file name in .gitignore such that i wont be imported to git repo, now added .env file in .gitignore
load_dotenv()


def main():
    while True:
        input_text=input("Enter message (you):")
        client = Groq(api_key=os.getenv("Gorq_Key"))
        if input_text.lower() == "exit":
            break
        response = client.chat.completions.create(
            model=os.getenv("model_name"),
            messages=[{"role":"user", "content":input_text}],
            temperature=0.2,
            max_tokens=20
        )
        print("AI: ", response.choices[0].message.content)


if __name__ == "__main__":
    main()
