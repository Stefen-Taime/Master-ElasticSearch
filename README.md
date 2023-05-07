Introduction

Elasticsearch is a powerful, distributed, RESTful search and analytics engine that can handle large amounts of data in real-time. In this article, we will demonstrate how to set up an Elasticsearch instance using Docker Compose, index data from a CSV file, perform queries using Python’s Elasticsearch library, and visualize the query results using Streamlit.

Setting Up Elasticsearch with Docker Compose

First, let’s set up an Elasticsearch instance using Docker Compose. Create a `docker-compose.yml` file with the following content:

```
version: '3.8'services:  elasticsearch:    image: docker.elastic.co/elasticsearch/elasticsearch:7.15.0    container_name: elasticsearch    environment:      - node.name=elasticsearch      - cluster.name=es-docker-cluster      - cluster.initial_master_nodes=elasticsearch      - bootstrap.memory_lock=true      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"      - xpack.security.enabled=false      - xpack.security.transport.ssl.enabled=false      - "ELASTIC_PASSWORD=elastic"    ulimits:      memlock:        soft: -1        hard: -1    volumes:      - esdata:/usr/share/elasticsearch/data    ports:      - 9200:9200    networks:      - esnetvolumes:  esdata:    driver: localnetworks:  esnet:
```

To start the Elasticsearch container, run the following command in the terminal:

```
docker-compose up
```

Indexing CSV Data into Elasticsearch with Python

Now that we have an Elasticsearch instance running, let’s index some data from a CSV file. We will use Python’s `csv` and `elasticsearch` libraries to read the CSV file, preprocess the data, and index it into Elasticsearch. Here's a Python script that demonstrates this process:

```
from elasticsearch import Elasticsearch, helpersimport csves = Elasticsearch("http://elastic:elastic@localhost:9200")def read_csv(file_path):    with open(file_path, 'r') as f:        reader = csv.DictReader(f)        for row in reader:            yield rowdef preprocess_data(row):    row['dep'] = int(row['dep'])    return rowdef get_index_name(row):    if row['dep'] == 23:        return "dept23"    elif row['dep'] == 48:        return "dept48"def index_data(data, index_name):    actions = [        {            "_op_type": "index",            "_index": index_name,            "_source": preprocess_data(row),        }        for row in data    ]    helpers.bulk(es, actions)dept23_data = [row for row in read_csv('test_dataset.csv') if row['dep'] == '23']dept48_data = [row for row in read_csv('test_dataset.csv') if row['dep'] == '48']index_data(dept23_data, 'dept23')index_data(dept48_data, 'dept48')
```

Querying Elasticsearch with Python

After indexing the data, we can perform queries using Python’s Elasticsearch library. Here’s an example of how to perform four different queries on the indexed data:

```
from elasticsearch import Elasticsearches = Elasticsearch("http://elastic:elastic@localhost:9200")query1 = {    "query": {        "bool": {            "must": [                {"match": {"denominationUniteLegale": "baker"}}            ]        }    }}res1 = es.search(index="dept23", body=query1)print("Results for Query 1:")for hit in res1['hits']['hits']:    print(hit['_source'])query2 = {    "query": {        "bool": {            "must": [                {"match": {"activitePrincipaleEtablissement": "90.01Z"}}            ]        }    }}res2 = es.search(index="dept48", body=query2)print("\nResults for Query 2:")for hit in res2['hits']['hits']:    print(hit['_source'])query3 = {    "query": {        "bool": {            "must": [                {"terms": {"codeCommuneEtablissement": ["23079", "23176"]}}            ]        }    }}res3 = es.search(index="dept23", body=query3)print("\nResults for Query 3:")for hit in res3['hits']['hits']:    print(hit['_source'])query4 = {    "query": {        "bool": {            "must": [                {"match": {"_all": "Theatre Mende"}}            ]        }    }}res4 = es.search(index="dept48", body=query4)print("\nResults for Query 4:")for hit in res4['hits']['hits']:    print(hit['_source'])
```

1.  Query 1 searches for all companies in department 23 where the `denominationUniteLegale` field contains the word 'baker'. The query results are printed out using a for loop.
2.  Query 2 searches for all companies in department 48 where the `activitePrincipaleEtablissement` field is equal to '90.01Z'. The query results are printed out with a newline separator.
3.  Query 3 searches for all companies in department 23 where the `codeCommuneEtablissement` field is either '23079' or '23176'. The query results are printed out with a newline separator.
4.  Query 4 searches for companies in department 48 with the query terms ‘Theatre Mende’. Note that this query is incorrect, as the `_all` field has been removed in Elasticsearch 6.0 and later. Instead, you should use a `multi_match` query or specify the fields you want to search in.

```
streamlit run dashboard.py
```