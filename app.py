from flask import Flask 
from pymongo import MongoClient
from bson import json_util
import json
from bs4 import BeautifulSoup
import requests

quotes = []
container = []

endPageNumber = 60
pageNumber = 1
while pageNumber <= endPageNumber:
    webpage = requests.get(f'https://www.goodreads.com/author/quotes/17212.Marcus_Aurelius?page={pageNumber}')
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



app = Flask(__name__)   
app.debug = True
app.url_map.strict_slashes = False

with open('aurelius.json', 'a', encoding='utf-8') as file:
    file.write(JSONdata)
    

connection_string = "mongodb+srv://ratocato:Ashfaque64!@cluster0.pgynk.mongodb.net/cluster0?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client['PhilosophicalAPI']
collection = db['Quotes']


@app.route('/random', methods=['GET'])
def randoma():
    randomQuote = collection.aggregate([ { '$sample': { 'size': 1 } } ])
    quotes = [x for x in randomQuote]
    serializeQuotes = json.dumps(quotes, indent=2, separators=(',', ':'), sort_keys=True, default=json_util.default)    
    return serializeQuotes

@app.route('/quotes', methods=['GET'])
def randomTen():
        randomTenQuotes = collection.aggregate([ { '$sample': { 'size': 10 } } ])
        tenQuotes = [x for x in randomTenQuotes]
        serializeTenQuotes = json.dumps(tenQuotes, indent=2, separators=(',', ':'), sort_keys=True, default=json_util.default)  
        return serializeTenQuotes   


'''Quotes From Albert Camu, Confucius, Socrates, Plato, Nietzsche, Immanuel Kant, René Descartes, Fyodor Dostoevsky,
    Marcus Aurelius,
'''

#asdsada testing