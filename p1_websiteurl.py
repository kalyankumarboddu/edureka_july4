from dotenv import load_dotenv
import os
from groq import Groq
import requests 
from bs4 import BeautifulSoup
from requests.exceptions import InvalidURL, MissingSchema
load_dotenv()


system_prompt = """
Assume you are an expert in understanding an website and you have been provide with the complete urls that are present 
in the website and you need to extract the urls that are very much relavent to the website.
Share us the result in an Json format as below.
{
   "links": [
    {"type" : "about","url": "url_that_gives_information_about_website"},
    {"type" : "carrers" , "url" : "url_that_gives_information_about_carrers_inside_that_website"}
    ]
}
"""
def fetch_website_url(url,header):
    try:
        resp = requests.get(url=url, headers=header)
        resp.raise_for_status()
    except InvalidURL as e:
        print(f"{url} raised an exception")
        return None
    except MissingSchema as e:
        print(f"{url} raise missing schema exception")
        return None
    except Exception as e:
        print(f"{url} raised an general exception")
        return None
    
    soup = BeautifulSoup(resp.content, "html.parser")

    title = soup.title.string if soup.title else "No-title"
    
    url_links = [ele.get("href") for ele in soup.find_all('a')]

    return(title + "\n" + str(url_links))[:2000]

def user_prompt_link(url,header):
    user_prompt = f"""
    As assumed your are the expert in understanding website page for the given website {url},
    extract the relavent information and share us the details in Json format and exclude website terms and service
    conditions.
    Passing the relavent title concatenated with URLS of the websites as follows:

    """
    wb_url = fetch_website_url(url,header)
    return user_prompt + wb_url


def main():
    client = Groq(api_key=os.getenv("Gorq_Key"))
    response = client.chat.completions.create(
        model=os.getenv("model_name"),
        messages=[
            {"role":"system", "content":system_prompt},
            {"role":"user", "content":user_prompt_link(url,header)}
            ],
        temperature=0.2,
        response_format={"type":"json_object"}
    )
    print(response.choices[0].message.content)


if __name__ == "__main__":
    header = {
    "User-Agents" : "Browser Details"
    }
    url = "https://huggingface.co/"
    main()