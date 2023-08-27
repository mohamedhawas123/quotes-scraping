import requests
from bs4 import BeautifulSoup
import psycopg2


DATEBASE_URL = 'postgresql://postgres:NuQmt3k6kJX8C0fNEOMp@containers-us-west-32.railway.app:7007/railway'



def scrape_quotes():
    url = "http://quotes.toscrape.com"
    response = requests.get(url)

    if response.status_code != 200:
        print('something went wrong')
        return []

    
    soup = BeautifulSoup(response.text, 'html.parser')
    quote_elements = soup.find_all('div', class_='quote')

    quotes = []

    for element in quote_elements:
        text = element.find('span', class_='text').text
        author = element.find('small', class_='author').text

        quotes.append((text, author))

    print(quotes)
    return quotes


def stores_quotes_in_db(quotes):
    with psycopg2.connect(DATEBASE_URL) as conn:
        with conn.cursor() as cursor:
            for quote, author in quotes:
                cursor.execute("INSERT INTO quotes (quote, author) VALUES (%s, %s)", (quote, author))


if __name__ == "__main__":
    quotes = scrape_quotes()
    stores_quotes_in_db(quotes)