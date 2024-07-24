import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
import datetime
import warnings
from elasticsearch.exceptions import ElasticsearchWarning

warnings.simplefilter('ignore', ElasticsearchWarning)


# Verileri çeken fonksiyon
def fetch_news():
    url = "https://www.sozcu.com.tr/"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching the website: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    items = soup.find_all('a', class_='currency-item down') + soup.find_all('a', class_='currency-item up')

    data = []
    for item2 in items:
        name_tag = item2.find('span', class_='currency-item-name')
        value_tag = item2.find('span', class_='currency-item-value')

        if name_tag and value_tag:
            name = name_tag.text.strip()
            value = value_tag.text.strip()
            data.append({"name": name, "value": value, "timestamp": datetime.datetime.now().isoformat()})

    return data


# Elasticsearche verileri yükleyen fonksiyon
def load_to_elasticsearch(data, index_name='currency_data'):
    try:
        # Connect to Elasticsearch
        es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

        # Load data one by one
        for item1 in data:
            es.index(index=index_name, document=item1)

    except Exception as e:
        print(f"Error loading data to Elasticsearch: {e}")


# Elasticsearchteki datayı yazdıran fonksiyon
def check_data_in_elasticsearch(index_name='currency_data'):
    try:
        es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
        if not es.ping():
            print("Elasticsearch server is not responding.")
            return

        result = es.search(index=index_name, body={"query": {"match_all": {}}})
        for doc in result['hits']['hits']:
            print(doc['_source'])
    except Exception as e:
        print(f"Error querying Elasticsearch: {e}")


# Main kısmı
if __name__ == "__main__":
    news_data = fetch_news()

    if news_data:
        load_to_elasticsearch(news_data)
    else:
        print("No data fetched.")

# Burada elasticsearche yolladığım veriyi gösterdim
    print("Data in Elasticsearch:")
    check_data_in_elasticsearch()

# Burada da fonksiyonun çektiği datayı gösterdim ama ikisi uyuşmuyor bir türlü düzeltemedim maalesef
    print("Fetched data:")
    for item in news_data:
        print(item)
