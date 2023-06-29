import pandas as pd
from thefuzz import fuzz
from urllib.parse import quote

df = pd.read_csv("phones_data.csv")

def check_caregory(user_input):
    for d in df["model_name"]:
        if fuzz.ratio(user_input, d) > 80:
            return True
        elif fuzz.partial_ratio(user_input, d) > 80:
            return True
    for f in df["brand_name"]:
        if fuzz.ratio(user_input, f) > 90:
            return True
        elif fuzz.partial_ratio(user_input, f) > 90:
            return True
    
    return False
       
def google_search_link(item_name):
    search_query = quote(item_name)
    link = f"https://www.google.com/search?q={search_query}"
    return link

        


