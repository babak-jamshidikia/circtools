#curl -X 'POST'
#'https://circhemy.jakobilab.org/api/query'
#-H 'accept: application/json'
#-H 'Content-Type: application/json' -d '{
#    "input": [
#        {
#            "query": "chr22",
#            "field": "Chr",
#            "operator1": "AND",
#            "operator2": "is"
#        }
#    ],
#    "output": [
#        "CircAtlas2"
#    ]
#}'
import requests
import json
url = "https://circhemy.jakobilab.org/api/query"

headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}
chromosome = "chr22"
chrstart = "36341370"
chrstop ="36349255"

data = '{"input": [{"query": "' + chromosome + '", "field": "Chr", "operator1": "AND", "operator2": "is"},'\
        '{"query": "' + chrstart + '", "field": "Start", "operator1": "AND", "operator2": "is"},'\
        '{"query": "' + chrstop + '", "field": "Stop", "operator1": "AND", "operator2": "is"}],'\
        ' "output": ["Circpedia2"]}'

response = requests.post(url, data=data,headers=headers)

#print(response.json())
jsondata= response.json()
jj =jsondata["rowData"][0]["Circpedia2"]
print(jj)







