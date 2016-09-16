'''the credentials are stored in ./credentials/credentials.yml, please update
the path to the file on line 11 (beginning of the code).
.yml format: the key used is 'NYT_api_key'
'''

import yaml
import requests
import json
import math
import csv

def get_NYT_request(search_term, begin_year, end_year,
                path_to_credentials='./credentials/credentials.yml'):

    '''
    parameters:
    -----------
    search_term: as STR
                query term on which the search is performed on the
                article body, headline and byline
    begin_year: as INT
                year that restricts responses to results with publication dates
                of the year specified or later.
    end_year: as INT
                year that restricts responses to results with publication dates
                of the year specified or earlier.
    path_to_credentials: as STR
                path to the .yml file with the API key stored in the following
                format: NYT_api_key: + space + NYT issued code

    returns:
    --------
    r: a request object
    '''
    ########    authentification
    # define the path to the credentials
    path_to_file = path_to_credentials
    credentials = yaml.load(open(path_to_file))

    ########    building the request url
    # define the base url
    base_url="http://api.nytimes.com/svc/search/v2/articlesearch"

    # choose response format (here, Article Search API outputs .json)
    response_format=".json"

    # make the url
    NYT_request_url = base_url+response_format

    ########    Sent the GET request
    # ensure authentification
    NYT_api_key = credentials['NYT_api_key']

    # define the search parameters:
    search_params = {'q': search_term,
                     'begin_date': str(begin_year)+'0101',
                     'end_date': str(end_year)+'1231',
                     'api-key': NYT_api_key}

    # make the request
    r = requests.get(NYT_request_url, params=search_params)

    return r
if __name__ == '__main__':
    # define the path to the credentials
    path_to_cred_file = '../../credentials/credentials.yml'
    #search parameters
    terms = 'Donald Trump'

    r = get_NYT_data(search_term=terms,
                    begin_year= 2013,
                    end_year=2015,
                    path_to_credentials=path_to_cred_file)
    print r.url
    print r.text
