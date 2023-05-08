## Introduction

The purpose of this interview exercise is to assess your ability to index and query some data in elasticsearch.

Your goal is to ingest a dataset into two elasticsearch indexes then query them smartly to find specific documents.

Elasticsearch instance could be deploy with a docker-compose file in this github repo. There is no need to customize it, thus you will be able to focus on data ingestion and data querying.

The result code should be written on Python language (either pure python scripts or jupyter notebook, as you want). Upon completion, please upload your code on a public git repository and add a README that could help us to test your code.  

After the exercise is completed, we will take the time to discuss what has been done. There's not a single way to do things right, and we're aware of that. Please code what you feel would be naturally elegant and simple for you, not what you think we might expect.

If you're stuck on something, please reach out to us.

## Exercise

The exercise is divided between the following steps:

- First, deploy Elasticsearch instance with : `docker-compose up -d` . It will deploy your elasticsearch instance available at [localhost:9200](http://localhost:9200) (login : elastic, password: elastic)
- Recuperate the dataset in this repo "test_dataset.csv.gz"
    - This dataset is an extraction from the [French Sirene database representing information about french companies](https://www.data.gouv.fr/fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/). This extraction contains data from two french departments "Creuse (23)" and "Lozere (48)" (about ~40k companies)
- Find a way to index properly this dataset into Elasticsearch local instance. Data should be ingested into two different indexes (one by departement). Data ingestion could be made by several ways but there is probably ways faster and cleaner than others.
- Once indexation is done, find a way to query :
    - All companies in Department 23 where `denominationUniteLegale` **contains** word : `boulanger`
    - All companies in Department 48 where `activitePrincipaleEtablissement`  **is** `90.01Z`
    - All companies in Department 23 where `codeCommuneEtablissement` **is** `23079` **or** `23176`
    - Relevant companies in Departement 48 where terms of query **is** `Théâtre Mende` (NB : Mende is the city capital of Department 48)
    

## Vocabulary

Datasets contains different columns which can be difficult to interprete. Here is the signification of them :

- `siren` : French id of a french company
- `siret` : French id of a french establishment (subdivision of a company)
- `denominationUniteLegale` : Name of the company
- `sigleUniteLegale` : Eventual short name of a company
- `enseigne1Etablissement` : Eventual name of the establishment
- `activitePrincipaleEtablissement`  : Type of company (types meaning could be found here : [https://www.insee.fr/fr/information/2120875](https://www.insee.fr/fr/information/2120875))
- `geo_adresse` : Adress of the company
- `geo_score` : Confidence score of the adress
- `categorieJuridiqueUniteLegale` : Juridical category of the company
- `codeCommuneEtablissement` : geographical code of the city hosting the company
- `dep` : department of the company
