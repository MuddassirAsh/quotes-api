from bs4 import BeautifulSoup
import requests
import json

quotes = []
container = []

endPageNumber = 5
pageNumber = 1
while pageNumber <= endPageNumber:
    webpage = requests.get('https://www.goodreads.com/author/quotes/957894.Albert_Camus?page={}'.format(pageNumber))
    soup = BeautifulSoup(webpage.text, 'html.parser')
    quoteText = soup.find_all("div", {"class": "quoteText"})

    for i in quoteText:
        quotes.append(i.get_text(strip=True, separator=" ").replace('“','').replace('”','').split('― '))

    for x, y in quotes:
        data = {
            'Quotes': x.strip(),
            'Source': y.strip()
        }
        container.append(data)

    # coverting dict into JSON
    JSONdata = json.dumps(container, ensure_ascii=False, indent=2)
    pageNumber = pageNumber + 1


with open('samplefile.json', 'w', encoding='utf-8') as file:
    file.write(JSONdata)