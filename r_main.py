import json
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent":
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.1.1148 (beta) Yowser/2.5 Safari/537.36"
}


def get_html(url, header=HEADERS):
    responce = requests.get(url, headers=header)
    if responce.status_code == 200:
        return responce.text
    else:
        raise ValueError(f"Error: {responce.status_code}")
    
def processing(html):
    soup = BeautifulSoup(html, "lxml").find_all("div", {"class": "shortstory"})

    info = []

    for item in soup:
        url = item.find("div", {"class": "shortstoryHead"}
            ).find("h2").find("a").get("href")
        
        title = item.find("div", {"class": "shortstoryHead"}
            ).find("h2").find("a").text

        cotegory = item.find("div", {"class": "shortstoryFuter"}
            ).find("span").find("i").text
        
        tbody_info = item.find("div", {"class": "shortstoryContent"}).find(
            'table').find('tr').find_all('p')
        
        director = str(tbody_info[4].text).split(": ")[1]

        img = item.find("div", {"class": "shortstoryContent"}).find(
            'table').find('tr').find('img').get("src")
        
        responce_img = requests.get("https://v2.vost.pw" + img)

        name = str(title).split('/')[0]
        if len(name) >= 30:
            name = name[:30]

        with open(f"img/{name}.jpg", "wb") as file_img:
            file_img.write(responce_img.content)

        info.append({
            "url": url,
            "title": str(title).split(" [")[0],
            "cotegory": cotegory,
            'release_year': str(tbody_info[0].text).split(": ")[1],
            'genre': str(tbody_info[1].text).split(": ")[1],
            'type': str(tbody_info[2].text).split(": ")[1],
            'episode': str(tbody_info[3].text).split(": ")[1],
            'director': director if len(director) <= 30 else None,
        })   
    return info

def run():
    base_list = []
    for i in range(1,6):   #page?=6
        URL = f"https://v2.vost.pw/page/{i}/"
        html = get_html(URL)
        source = processing(html)
        base_list.extend(source)
        print(f"Страница {i} завершена")

    with open ("info.json", "w", encoding="UTF-8") as file_json:
        json.dump(base_list, file_json, indent=4, ensure_ascii=False)

run()