import requests
from bs4 import BeautifulSoup
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

def website_content(ur):
    resp = requests.get(url=url)
    beautify = BeautifulSoup(resp.content,'html.parser')
    #Returns distinct tags inside the url
    # print(sorted(set(tag.name for tag in beautify.body.find_all()))) 
    if beautify.body:
        for decom in beautify.body(["img","path","ellipse","input","span","nav","link","script","style"]):
            decom.decompose()
        text = beautify.body.get_text()
    else:
        text = ""
    return text

system_prompt = """
You are an assistant that analyzes the contents of several relevant pages from a company website
and creates a short brochure about the company for prospective customers, investors and recruits.
"""

def user_prompt(url):
    user_prompt = f"""
    Your looking at the company with url f{'url'} and concatinated with website contents as below
    and need to assit in creating a short broucher with website landing page content details
    """

    wb_content = website_content(url)
    return user_prompt + wb_content.strip()

def main(url):
    output = ''
    client = Groq(api_key=os.getenv("Gorq_Key"))
    response = client.chat.completions.create(
        model=os.getenv("model_name"),
        messages=[
            {"role":"system", "content":system_prompt},
            {"role":"user", "content":user_prompt(url)}
            ],
        temperature=0.2,
        stream=True
    )
    for chunk in response:
        resp = chunk.choices[0].delta.content
        if resp:
            print(resp, end="", flush=True) #to print each chunk without \n at the end
            output += resp
    return output


if __name__ == "__main__":
    url = "https://huggingface.co/"
    # Result will be streamed
    main(url)

    # to print entire output as a string
    # print(main(url))