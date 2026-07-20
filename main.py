from dotenv import load_dotenv
import os

## add required file name in .gitignore such that i wont be imported to git repo, now added .env file in .gitignore
load_dotenv()
print("Key value for Key1 is", os.getenv("Key1"))
print("Key value for Key2 is", os.getenv("KEY2"))
print("Key value for No Key is", os.getenv("Key3"))




# def main():
#     print("Hello from uv-project!")


# if __name__ == "__main__":
#     main()
