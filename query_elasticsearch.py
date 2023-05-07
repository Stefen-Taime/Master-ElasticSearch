from elasticsearch import Elasticsearch

es = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])

# Query 1: All companies in department 23 where denominationUniteLegale contains the word 'baker'
query1 = {
    "query": {
        "bool": {
            "must": [
                {"match": {"denominationUniteLegale": "baker"}}
            ]
        }
    }
}

res1 = es.search(index="dept23", body=query1)
print("Results for Query 1:")
for hit in res1['hits']['hits']:
    print(hit['_source'])

# Query 2: All companies in department 48 where activitePrincipaleEtablissement is 90.01Z
query2 = {
    "query": {
        "bool": {
            "must": [
                {"match": {"activitePrincipaleEtablissement": "90.01Z"}}
            ]
        }
    }
}

res2 = es.search(index="dept48", body=query2)
print("\nResults for Query 2:")
for hit in res2['hits']['hits']:
    print(hit['_source'])

# Query 3: All companies in department 23 where codeCommuneEtablissement is found in [23079, 23176]
query3 = {
    "query": {
        "bool": {
            "must": [
                {"terms": {"codeCommuneEtablissement": ["23079", "23176"]}}
            ]
        }
    }
}

res3 = es.search(index="dept23", body=query3)
print("\nResults for Query 3:")
for hit in res3['hits']['hits']:
    print(hit['_source'])

# Query 4: Companies in department 48 where the query terms are Theatre Mende
query4 = {
    "query": {
        "bool": {
            "must": [
                {"multi_match": {
                    "query": "Theatre Mende",
                    "fields": ["denominationUniteLegale", "activitePrincipaleEtablissement"]
                }}
            ]
        }
    }
}

res4 = es.search(index="dept48", body=query4)
print("\nResults for Query 4:")
for hit in res4['hits']['hits']:
    print(hit['_source'])
