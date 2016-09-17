'''the credentials are stored in ./credentials/credentials.yml, please update
the path to the file on line 11 (beginning of the code).
.yml format: the key used is 'NYT_api_key'
'''

import yaml
import requests
import json
import math
import csv
import matplotlib.pyplot as plt #for visualization
import numpy as np

def get_NYT_request(search_term, begin_year, end_year, page=0,
                path_to_credentials='../../credentials/credentials.yml'):

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
    page: as INT
                the value of page corresponds to a set of 10 results
                defaults to 0: set of results 0-9
    path_to_credentials: as STR
                path to the .yml file with the API key stored in the following
                format: NYT_api_key: + space + NYT issued code
                defaults to file credentials outside of the NYT project

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
                     'page': page,
                     'api-key': NYT_api_key}

    # make the request
    r = requests.get(NYT_request_url, params=search_params)

    return r

def extract_num_hits(search_term, begin_year, end_year, page=0,
                path_to_credentials='../../credentials/credentials.yml'):
    '''
    parameters:
    -----------
    see docstring of get_NYT_request

    returns:
    --------
    hits as INT
         number of articles that the search found
    '''
    # make request
    r = get_NYT_request(search_term, begin_year, end_year,
                    path_to_credentials=path_to_credentials)

    ########    Extract the relevant data
    # convert the raw file (.json) to a dictionary
    data = json.loads(r.text)

    # get number of hits
    hits = data['response']['meta']['hits']

    return hits

def find_trend(start_year, end_year,
              search_term,
              path_to_credentials='../../credentials/credentials.yml'):
    '''
    parameters:
    -----------
    start_year: as INT
                first year of the range over which the trend will be observed
    end_year: as INT, must be higher than start_year
                last year (included) of the range over which the trend will
                be observed
    see docstring of get_NYT_request for the other variables

    returns:
    --------
    list_of_values: as LIST of INT
                hits for the year range specified
    '''
    list_of_hits = []

    for year in range(start_year, end_year+1):
        hits = extract_num_hits(search_term, year, year, page=0,
                        path_to_credentials='../../credentials/credentials.yml')
        list_of_hits.append(hits)

    return list_of_hits

def plot_trend(start_year, end_year,
                search_term, list_of_hits, show_option=True):
    '''
    parameters:
    -----------
    start_year: as INT
                year at the beginning of the year range to observe the trend in
    end_year: as INT
                year at the end of the year range to observe the trend in
    show_option: as BOOL, default True
                show the plot directly

    returns:
    --------
    fig: bar graph
    '''
    width = 1
    range_years = range(start_year, end_year+1)

    #create graph
    fig = plt.figure()
    plt.bar(range_years, list_of_hits, width=width)

    #setting labels
    plt.ylabel('Number of hits')
    plt.xlabel('Year')
    plt.title("Number of hits per year for search term '{}'".format(search_term))
    plt.xticks(np.array(range_years)+width*.5, range_years, rotation=30)

    if show_option:
        plt.show()
    return fig

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
