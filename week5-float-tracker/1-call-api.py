import os
import requests
from dotenv import load_dotenv 

load_dotenv()

API_KEY = os.getenv("FMP_API_KEY")



# makes ONE call to FMP's bulk float endpoint and prints the raw JSON
def make_call(page):
    url = f"https://financialmodelingprep.com/stable/shares-float-all?page={page}&limit=1000&apikey={API_KEY}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    print(data)


make_call("1")