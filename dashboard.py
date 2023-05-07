import streamlit as st
from elasticsearch import Elasticsearch
from pandas import DataFrame

# Establish a connection to Elasticsearch
es = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])

# Define search queries
query1 = {
    "query": {
        "bool": {
            "must": [
                {"match": {"denominationUniteLegale": "baker"}},
                {"match": {"dep": "23"}}
            ]
        }
    }
}

query2 = {
    "query": {
        "bool": {
            "must": [
                {"match": {"activitePrincipaleEtablissement": "90.01Z"}},
                {"match": {"dep": "48"}}
            ]
        }
    }
}

query3 = {
    "query": {
        "bool": {
            "must": [
                {"terms": {"codeCommuneEtablissement": ["23079", "23176"]}},
                {"match": {"dep": "23"}}
            ]
        }
    }
}

query4 = {
    "query": {
        "bool": {
            "must": [
                {"match": {"dep": "48"}},

                {"bool": {
                    "should": [
                        {"match": {"denominationUniteLegale": "Theatre"}},

                        {"match": {"denominationUniteLegale": "Mende"}}
                    ]
                }}
            ]
        }
    }
}


# Perform search queries
res1 = es.search(index="dept23", query=query1["query"])
res2 = es.search(index="dept48", query=query2["query"])
res3 = es.search(index="dept23", query=query3["query"])
res4 = es.search(index="dept48", query=query4["query"])


# Create dataframes from search results
dept23_baker_df = DataFrame([hit["_source"] for hit in res1["hits"]["hits"]])
dept48_activity_df = DataFrame([hit["_source"] for hit in res2["hits"]["hits"]])
dept23_codes_df = DataFrame([hit["_source"] for hit in res3["hits"]["hits"]])
dept48_theatre_mende_df = DataFrame([hit["_source"] for hit in res4["hits"]["hits"]])

# Create Streamlit dashboard
st.title("Dashboard Catalogue")

st.header("Department 23 - Companies with 'baker' in denominationUnitLegal")
st.write(dept23_baker_df)

st.header("Department 48 - Companies with activitePrincipaleEtablissement 90.01Z")
st.write(dept48_activity_df)

st.header("Department 23 - Companies with codeCommuneEtablissement 23079 or 23176")
st.write(dept23_codes_df)

st.header("Department 48 - Companies with 'Theatre' and 'Mende' in denominationUniteLegale")
st.write(dept48_theatre_mende_df)
