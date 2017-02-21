import requests, json

# if comma, support multiple keywords
search = "healthcare"

# sets up url
params = {"api-key":"65ba2d56f56c46fdb954ada862757158",
    "q": search,
    "fq":"keywords",
    "fl":"web_url,headline,pub_date",
    "hl":"true"
    }
nyt_url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
body = requests.get(nyt_url, params = params).content

# if response, hits == 0, print "use another keyword"

# prints url
print body

# json.loads(response)
# response = str(response.content)
# http = response.split('\n', 1)[0]
# print http
