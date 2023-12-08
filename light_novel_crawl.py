from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import quote

def extract_domain(url):
    match = re.match(r'https?://([^/]+)', url)
    if match:
        return match.group(0)
    else:
        return None

def remove_dot(text):
    blacklist = [",", ".", ":", "!", "~"]
    for char in text:
        if (char in blacklist):
            text = text.replace(char, "")
    return text

lightNovel = input("Enter the url of light novel: ")
resq = requests.get(lightNovel).text
soup = BeautifulSoup(resq, 'html.parser')  
base_url = extract_domain(lightNovel)
url = lightNovel.replace(base_url, "") 

find_name = soup.find_all("div", class_ = "block pad-bottom-5")
book_name = []
for name in find_name:
    if (name.text.isascii()):
        book_name.append(name.text)
resquestSearch = ""

print("Light novel name: " + book_name[0])
book_name_search = remove_dot(book_name[0]).lower() + " novel updates"
encoded_book_name = quote(book_name_search)
google_search_url = f'https://www.google.com/search?q={encoded_book_name}&rlz=1C1CHBD_viVN991VN991&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDIyODZqMGoxqAIAsAIA&sourceid=chrome&ie=UTF-8'
resquestSearch = requests.get(google_search_url).text
    
english_light_novel_url = []
print("Light novel english version: ")
soup2 = BeautifulSoup(resquestSearch, 'html.parser')
book_links_eng = soup2.find_all('a', href=True)
for b in book_links_eng:
    link = b['href'].replace("/url?q=", "")
    if (link.startswith("https://www.novelupdates.com/series/")):
        english_light_novel_url.append(re.sub(r'&sa=.*$', '', link))
novel_update_final_url = []
if (english_light_novel_url == None):
    print("Can not find the english version please search by hand!")
else:
    for lightNovelEngUrl in english_light_novel_url:
        source = requests.get(url=lightNovelEngUrl).text
        soup_novel_update = BeautifulSoup(source, 'html.parser')
        novel_update_book_names = soup_novel_update.find_all("div", {"id" : "editassociated"})
        for book_eng_name in novel_update_book_names:
            if (book_name[0] in book_eng_name):
                print("Novel update link: " + lightNovelEngUrl)
                novel_update_final_url.append(lightNovelEngUrl)

# find translator team
trans_team = set()
for novel_link in novel_update_final_url:
    res = requests.get(url=novel_link).text
    soup_for_translator = BeautifulSoup(res, "html.parser")
    translator_team = soup_for_translator.find("a", href=True)
    for trans in translator_team:
        if (trans['href'].startswith("https://novelupdates.com/group/")):
            trans_team.add(remove_dot(trans['href']).lower().replace("https://www.novelupdates.com/group/"))

trans_team = list(trans_team)
search_light_novel = book_name[0] + " " + trans_team[0] + "light novel eng"
encoded = quote(search_light_novel)
goole_search_light_novel_with_trans = f'https://www.google.com/search?q={encoded}&rlz=1C1CHBD_viVN991VN991&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDIyODZqMGoxqAIAsAIA&sourceid=chrome&ie=UTF-8'
responseSearchLightNovelEng = requests.get(url=goole_search_light_novel_with_trans)
print("Light Novel version: ")
soupForGoogleSearch = BeautifulSoup(responseSearchLightNovelEng, "html.parser")
light_novel_origin_list = soupForGoogleSearch.find_all("a", href=True)
for link in light_novel_origin_list:
    temp = link['href'].replace("/url?q=", "")
    if (temp.startswith("https://www." + remove_dot(trans_team[0]) + ".com") or temp.startswith("https://" + remove_dot(trans_team[0]) + ".com")):
        print(re.sub(r'&sa=.*$', '', temp))



                
