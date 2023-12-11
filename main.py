from bs4 import BeautifulSoup

def get_html(url = None, header=None):         # Вытаскивает код страницы html
    with open("html/index.html", "r") as html:
        src = html.read()
    
    return src

def processing(html):                          # Обрабатывает 
    # soup = BeautifulSoup(html, "lxml").find("div"
    #     ).find_all("a")[0].find("div")         # BeautifulSoup(Что парсить , с помощью чего)
    # find("a") - Вытащит первую встречную <a> в виде str, find_all("a") - Вытащит все <a> в типе данных list
    # soup = BeautifulSoup(html,"lxml").find("title").text
    soup = BeautifulSoup(html,"lxml").find("form"
        ).find_all("label")
    item_texts = []
    for item in soup:
        # item_texts.append(item.get_text(strip =True))
        # item_texts.append(item.text)
        item_texts.append(item.get("for"))                # Применяется к атрибута
    return item_texts
    # return soup

# get(), text, get_text() - подметоды применяются после основных

def run():                                     # Запуск 
    html = get_html()
    source = processing(html)

    return source

print(run())