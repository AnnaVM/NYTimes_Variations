# Follow Along

*Teaching Aims*

### 1. Useful Background Information
> **- What is an API?**

API stands for Application Program Interface, it handles the communication between computers or apps. The information exchanged is extremely well structured and is therefore easier to query than unstructured data.

> **- What is a RESTful API?**

A RESTful API is simply queried thanks to a url.

URL: uniform resource location, a string of characters interpreted through http
(e.g. start of url (http) + secure status (s) + domain name (www.google.com/) + query (#q) + search terms)

REST is an acronynm for "representational state transfert".

> **- What information can I find on an API?**

Quite a lot of metadata is available on APIs. Companies will naturally not give access to all their databases in order preserve the integrity of their business model. NY Times does not give the whole article, but still provides a lot if information (title, author, year, keywords, lead paragraph, ...)

Usually, APIs will have a rate limit (NYT API is limited to 1K calls per day, and 5 calls per second) and will ask for authentification. A good practice is to refrain from making your keys and passwords available on any shared documents (`yaml` package is quite handy).

> **- How does an API work?**

The following steps are very general and can apply to a lot of APIs:

 1. Structure your query (typically: base url + authentification + response format + search parameters)
 2. Send your query (GET action, easily achieved with `requests` package in Python)
 3. Receive the raw information from host (as a raw format that needs to be parsed)
 4. Format the information and store it locally (Python dictionaries are great with .json formats)

 For each API, its specific documentation will provide information as to how the API is designed. Here, we will be focusing on the NY Times (http://developer.nytimes.com/) and more specifically on the Article Search API (http://developer.nytimes.com/article_search_v2.json#/Documentation/GET/articlesearch.json).

### 2. Getting started

#### 1. Useful libraries:
`$ pip install library_name`
 - `yaml`(protect your keys and passwords)
 - `requests` (send a GET request to a server)
 - `json` (handle the '.json' format and import it in Python)

```Python
import yaml
import requests
import json
```
#### 2. API Key registration:
(http://developer.nytimes.com/signup)
  - enter your information and wait for the email with your code

  ![screenshot of my sign up][signup]

  - getting the credential file ready for `yaml`
    in credentials.yml saved in a separate file
    (structure: 'name of key' + ':' + 'space' + 'your key', here: NYT_api_key: your_key)

    * NB: this file will never be added to GitHub or other collaborative plateforms

    * note: reading the file is very easy, use the `yaml.load` method which will produce a dictionary to look up the value of the key.

    ```Python
    ########    authentification
    # define the path to the credentials
    path_to_file = path_to_credentials
    credentials = yaml.load(open(path_to_file))
    ```
### 3. Coding:

#### 1. Building the request url

```Python
########    building the request url
# define the base url
base_url="http://api.nytimes.com/svc/search/v2/articlesearch"

# choose response format (here, Article Search API outputs .json)
response_format=".json"

# make the url
NYT_request_url = base_url+response_format
```

#### 2. Sending the GET request

 - search parameters: look up the stucture in the documentation. As an overview, I listed the parameters I will be using.

|     parameters   |   name   | type  | quick definition from documentation |
|:----------------:|:--------:|:-----:|:-----------------------------------:|
|Search query term.|   q      |string | Search is performed on the article body, headline and byline.|
|Earliest date     |begin_date|string | "Format: YYYYMMDD" Restricts responses to results with publication dates of the date specified or later. |
|Latest date       |end_date  |string | "Format: YYYYMMDD" Restricts responses to results with publication dates of the date specified or earlier. |
|view all results  | page     |integer| The value of page corresponds to a set of 10 results|

The search parameters `search_params` is a dictionary with the name of the parameter as the key and the value set to our needs. Do not forget to include the field 'api-key' with your code, accessed through `yaml`.

 - GET request: I am using the `requests`library, but others are available (`httplib2`, `urllib.request`...)

 ```Python
 ########    Sent the GET request
 # ensure authentification
 NYT_api_key = credentials['NYT_api_key']

 # define the search parameters:
 search_params = {'q': search_term,
                  'begin_date': str(begin_year)+'0101',
                  'end_date': str(end_year)+'1231',
                  'page': page,
                  'api-key': NYT_api_key}

 # make the request
 r = requests.get(NYT_request_url, params=search_params)
 ```

I have built a request object `r`, that I can easily explore (give `search_term`, `begin_year`, `end_year` and `page` some values)
```Python
print(r.url)
print(r.text)
```

In NYT_api.py, you can see the function `get_NYT_request` where I combine all our building blocks.

#### 3. Formatting the raw response

 The response send by the NY Times server is a string, with the format corresponding to a .json file. I now want to have access to information it contains. I convert the .json into a Python dictionary (with nested dictionaries) and access the relevant values by figuring out which keys to call (here `'response'`,`'meta'` and `'hits'`).
 NB. So far, I only have the 10 of all the results displayed, corresponding to page 0 of the request.

```Python
########    Extract the relevant data
# convert the raw file (.json) to a dictionary
data = json.loads(r.text)

# get number of hits
hits = data['response']['meta']['hits']
```
In NYT_api.py, you can see the function `extract_num_hits` where I combine all our building blocks.

#### 4. Visualizing the trends

- First I want to generate a list of the number of hits over the years I am interested in. This is a perfect job for a `for` loop, that is then included in the function `find_trend`.

```Python
list_of_hits = []

for year in range(start_year, end_year+1):
    hits = extract_num_hits(search_term, year, year, page=0,
                    path_to_credentials='../../credentials/credentials.yml')
    list_of_hits.append(hits)

print list_of_hits
```

- I will use the `matplotlib.pyplot` package to see the evolution of the number of hits along the year range studied.

```Python
import matplotlib.pyplot as plt
import numpy as np

width = 1 #width of the bars
range_years = range(start_year, end_year+1)


plt.bar(range_years, list_of_hits, width=width)

#adding labels
plt.ylabel('Number of hits')
plt.xlabel('Year')
plt.xticks(np.array(range_years)+width*.5, range_years, rotation=30)

plt.title('Number of hits per year for search term {}'.format{search_term})

plt.show()
```
This plotting option is given by the function `plot_trend`

**Outcome for search term 'Donald Trump', years 2000-2015**
```Python
if __name__ == '__main__':
    # define the path to the credentials
    path_to_cred_file = '../../credentials/credentials.yml'
    #search parameters
    terms = 'Donald Trump'
    year_start = 2000
    year_end = 2015
    list_of_hits = find_trend(start_year=year_start, end_year=year_end, search_term=terms,
                    path_to_credentials=path_to_cred_file)

    plot_trend(year_start, year_end, terms, list_of_hits)
```

Running the script in the terminal `$python NYT_api.py` gives the following output:

![trend for Donal Trump][donald_trump]

### 4. Going further

get all the data from all the pages
save the data in csv
get keywords
get frequency of keywords

[signup]: https://github.com/AnnaVM/NYTimes_Variations/blob/master/trending_not_trending/images/sign_up.png "Screenshot of my sign up"
[donald_trump]: https://github.com/AnnaVM/NYTimes_Variations/blob/master/trending_not_trending/images/trend_donald_trump.png "Bar graph for the trend in search term Donald Trump"
