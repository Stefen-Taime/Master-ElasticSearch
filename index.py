from elasticsearch import Elasticsearch, helpers
import csv

# Connect to Elasticsearch
es = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])


# Read the CSV file and preprocess it
def read_csv(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row

def preprocess_data(row):
    row['dep'] = int(row['dep'])
    return row

def get_index_name(row):
    if row['dep'] == 23:
        return "dept23"
    elif row['dep'] == 48:
        return "dept48"

# Index the dataset into Elasticsearch
def index_data(data, index_name):
    actions = [
        {
            "_op_type": "index",
            "_index": index_name,
            "_source": preprocess_data(row),
        }
        for row in data
    ]
    helpers.bulk(es, actions)

# Separate the data by department and index it
dept23_data = [row for row in read_csv('test_dataset.csv') if row['dep'] == '23']
dept48_data = [row for row in read_csv('test_dataset.csv') if row['dep'] == '48']

index_data(dept23_data, 'dept23')
index_data(dept48_data, 'dept48')
