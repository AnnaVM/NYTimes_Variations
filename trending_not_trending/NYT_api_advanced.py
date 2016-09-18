import yaml
import requests
import json

import math
import csv
import re

import matplotlib.pyplot as plt #for visualization
import numpy as np

from wordcloud import WordCloud
from collections import defaultdict

def get_all_NYT_data(search_term, begin_year, end_year,
                path_to_credentials='../../credentials/credentials.yml',
                verbose=True):
    '''
    caveat: we are not taking into account the fact that NY Times will not give
            more than 100 pages back.
            e.g. number of hits:  77814
                 number of pages to query: 7782
                 number of pages obtained: 100

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
                defaults to file credentials outside of the NYT project
    verbose: as BOOL, defaults to True
                prints status information in the terminal

    returns:
    --------
    hits as INT, the number of queries
    a list of the dictionaries containing data['response']['docs']
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

    ########    Prepare the GET request
    # ensure authentification
    NYT_api_key = credentials['NYT_api_key']

    # define the search parameters:
    search_params = {'q': search_term,
                     'begin_date': str(begin_year)+'0101',
                     'end_date': str(end_year)+'1231',
                     'api-key': NYT_api_key}

    ########    Look for the number of hits, and therefore pages to go through
    # make the first request
    r = requests.get(NYT_request_url, params=search_params)

    # convert .json result to a dictionary
    data=json.loads(r.text)

    # extract number of hits
    hits = data['response']['meta']['hits']
    if verbose: print("number of hits: ", str(hits))

    # find the number of pages
    num_pages = int(math.ceil(hits/10))
    if verbose:
        print("number of pages to query: ", str(num_pages))
        if num_pages > 100:
            print('there are too many pages to query,'\
                   ' only 100 pages will be obtained')
    num_pages = min(num_pages, 100)
    ########    Gather all the documents
    all_docs = []

    for num_page in range(num_pages):
        if verbose: print("collecting page", str(num_page))

        # set the page parameter in the search term
        search_params['page'] = num_page

        # make request for that specific page
        r = requests.get(base_url+response_format, params=search_params)

        # convert to a dictionary
        data = json.loads(r.text)

        # extract the docs (list of dictionaries)
        docs = data['response']['docs']

        # add those docs to the big list
        all_docs += docs

    return hits, all_docs

def extract_info(doc):
    '''
    parameters
    ----------
    doc: dictionary obtained by querying the NYT api

    returns
    -------
    year: as INT publication date
    list of keywords
    '''
    year = int(doc['pub_date'][:4])
    list_keywords = []
    for d in doc['keywords']:
        list_keywords.append(d['value'])
    return year, list_keywords

def regroup_wanted_data(all_docs):
    dict_keywords = defaultdict(list)
    for doc in all_docs:
        year, list_keywords = extract_info(doc)
        dict_keywords[year].extend(list_keywords)

    return dict_keywords

def wraper_function_data(start_year, end_year, search_term, verbose=False):
    '''
    parameters
    ----------
    start_year: as INT
                first year of the time range to consider
    end_year: as INT
                last year of the time range to consider (year included)
    search_term: as STR
                the search term for the query to the NYT api
    verbose: as BOOL, defaults to False
            prints to terminal which year is being queried

    returns
    -------
    dictionnary where keys are the years in the time range
                      values are the number of hits for the query that year
    dictionnary where keys are the years in the time range
                      values are lists of the keywords found that year
    '''
    dict_hits = {}
    all_docs = []
    for year in range(start_year, end_year+1):
        if verbose: print ('year {}'.format(year))
        hits, docs = get_all_NYT_data(search_term, year, year, verbose=False)
        dict_hits[year] = hits
        all_docs += docs

    d_keywords = regroup_wanted_data(all_docs)
    return dict_hits, d_keywords

def handle_multiple_words(d_keywords):
    '''
    aim: some keywords should be parsed together 'New York City', the choice I made
         is to link them 'New_York_City'

    parameters
    ----------
    d_keywords: dictionary with years as keys and a list of keywords as value

    returns
    -------
    dictionary with the same keys as d_keywords, and values as a STR
                value: the keywords joined with '_' when they are parsed together
                       and with ' ' otherwise
    '''
    d_value_as_string ={}
    for year in d_keywords.keys():
        value = ''
        for item in d_keywords[year]:
            value += ' '
            word = '_'.join(item.split(' '))
            word = re.sub(',','',word)
            value += word
        d_value_as_string[year] = value
    return d_value_as_string

def produce_wordclouds(d_value_as_string, plot_option=True):
    '''
    aim: produce wordclouds, with the size indicating the rank (not the frequency)
    based on github 'wordcloud'

    parameters
    ----------
    d_value_as_string: as DICT
                       dictionary with years as keys and values as a STR
                       value: the keywords joined with '_' when they are parsed together
                       and with ' ' otherwise
    plot_option: as BOOL
                shows the plots by default

    returns
    -------
    dictionnary with years as keys and the matplotlib graphs as values
    '''
    dict_figs = {}
    for year in d_value_as_string:
        fig = plt.figure()
        text= d_value_as_string[year]
        wordcloud = WordCloud().generate(text)
        plt.imshow(wordcloud)
        plt.axis("off")
        if plot_option: plt.show()
        dict_figs[year] = fig
    return dict_figs
