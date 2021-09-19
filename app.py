import collections
from flask import Flask 
from pymongo import MongoClient
from bson import json_util
import json
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
from markupsafe import escape

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))


load_dotenv()
quotes = []
container = []

endPageNumber = 2
pageNumber = 1
while pageNumber <= endPageNumber:
    webpage = requests.get('https://www.goodreads.com/author/quotes/203707.Pythagoras?page={}'.format(pageNumber))
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


with open('pythagoras.json', 'w', encoding='utf-8') as file:
    file.write(JSONdata)



app = Flask(__name__)   
app.debug = True
app.url_map.strict_slashes = False

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
connection_string = "mongodb+srv://{}:{}@cluster0.pgynk.mongodb.net/cluster0?retryWrites=true&w=majority".format(username, password)
client = MongoClient(connection_string)
db = client['PhilosophicalAPI']
collection = db['Quotes']


@app.route('/random/', methods=['GET'])
def randoma():
    randomQuote = collection.aggregate([ { '$sample': { 'size': 1 } } ])
    quotes = [x for x in randomQuote]
    serializeQuotes = json.dumps(quotes, indent=2, separators=(',', ':'), sort_keys=True, default=json_util.default)    
    return serializeQuotes

@app.route('/quotes/', methods=['GET'])
def randomTen():
        randomTenQuotes = collection.aggregate([ { '$sample': { 'size': 10 } } ])
        tenQuotes = [x for x in randomTenQuotes]
        serializeTenQuotes = json.dumps(tenQuotes, indent=2, separators=(',', ':'), sort_keys=True, default=json_util.default)  
        return serializeTenQuotes   

@app.route('/<author>', methods=['GET']) 
def socrates(author):
    authorQuotes = collection.find( {'Source': {'$in': [author] }})
    container_authorQuotes = [x for x in authorQuotes ]
    serializ_authorQuotes = json.dumps(container_authorQuotes, indent=2, separators=(',', ':'), sort_keys=True, default=json_util.default)  
    return serializ_authorQuotes



'''Quotes from Albert Camus, Confucius, Socrates, Plato, Nietzsche, Immanuel Kant, René Descartes, Fyodor Dostoevsky,
   Marcus Aurelius, David Hume, John Locke, Jean-Paul Sartre, Thomas Hobbes, Søren Kierkegaard, Bertrand Russell,
   Epicurus, Niccolò Machiavelli, Arthur Schopenhauer, Pythagoras
'''
