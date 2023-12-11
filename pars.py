from bs4 import BeautifulSoup
import json

def get_html(url = None, header=None):
    with open("html/index.html", "r") as html:
        src = html.read()
    
    return src

def processing(html):
    soup = BeautifulSoup(html,"lxml").find_all("div", {"class": "shortstory"})

    info = []

    for item in soup:
        url = item.find("div", {"class": "shortstoryHead"}
            ).find("h2").find("a").get("href")
        
        title = item.find("div", {"class": "shortstoryHead"}
            ).find("h2").find("a").text

        cotegory = item.find("div", {"class": "shortstoryFuter"}
            ).find("span").find("i").text
        
        tbody_info = item.find("div", {"class": "shortstoryContent"}).find(
            'table').find('tbody').find('tr').find_all('p')

        director = str(tbody_info[4].text).split(": ")[1]

        info.append({
            "url": url,
            "title": title,
            "cotegory": cotegory,
            "release_year": str(tbody_info[0].text).split(": ")[1],
            "genre": str(tbody_info[1].text).split(": ")[1],
            "type": str(tbody_info[2].text).split(": ")[1],
            "episode": str(tbody_info[3].text).split(": ")[1],
            "director": director if len(director) <= 30 else None,
        })
    return info

    # info = []

    # for item in soup:
    #     url = item.find("h2").find("a").get("href")
    #     title = item.find("h2").find("a").text

    #     info.append({
    #         "url" : url,
    #         "title" : title
    #     })
    # return info

def run():
    html = get_html()
    source = processing(html)
    with open ("info.json", "w", encoding="UTF-8") as file_json:
        json.dump(source, file_json, indent=4, ensure_ascii=False)

    return source

print(run())