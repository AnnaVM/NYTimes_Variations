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

import StringIO #saving image as text for Javascript
import base64

import plotly.plotly as py
import plotly.graph_objs as go

import argparse #for command line

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

def wraper_function_data(start_year, end_year, search_term,
                        path_to_credentials='../../credentials/credentials.yml',
                         verbose=False):
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
        hits, docs = get_all_NYT_data(search_term, year, year,
                                    path_to_credentials = path_to_credentials,
                                    verbose=False)
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

#####################    interactive bar graph
#### adapted from
#### https://github.com/etpinard/plotly-dashboards/tree/master/hover-images

def save_images_as_str(dict_figs):
    '''
    parameters
    ----------
    dict_figs: as DICT
                key is the year
                value is the wordcloud stored in matplotlib figure

    returns
    -------
    dict_str: as DICT
            key is the year
            value is the wordcloud stored as a string
    '''
    dict_str = {}
    for year in dict_figs:
        fig = dict_figs[year]
        output = StringIO.StringIO()
        fig.savefig(output, transparent=True, bbox_inches='tight')

        encoded_string = base64.b64encode(output.getvalue())
        dict_str[year] = encoded_string
    return dict_str

def for_js_dictionary(dict_str):
    '''
    for the main.js, a Javascript dictionary structure is needed to link the bars to an image
       'year-2014': 'data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAA ... ==',
       'year-2015': 'data:image/jpeg;base64,iVBORw0 ...',

    parameters
    ----------
    dict_str: as DICT
        key is the year
        value is the wordcloud stored as a string

    returns
    -------
    STR, with the text for the Javascript dictionary
    '''
    middle_str = ''
    for year in dict_str:
        temp_str = '''   'year-''' + str(year) + '''': 'data:image/jpeg;base64,''' + dict_str[year] +'''',
        '''
        middle_str += temp_str
    return middle_str

def plotly_url(start_year, end_year, dict_hits):
    '''
    generates the url for the bar chart
    start_year and end_year must be included in dict_hits.keys()

    dict_hits as DICT
              key is year, value is the hits for that year
    '''
    #####  data
    # x-values
    range_years = range(start_year, end_year + 1)
    years_string = ['year ' + str(year) for year in range_years]

    # y-values
    list_of_hits = [dict_hits[year] for year in range_years]

    data = [go.Bar(
                x=years_string,
                y=list_of_hits
        )]

    layout = go.Layout(
        xaxis=dict(tickangle=-45)
    )

    #### get fig
    fig = go.Figure(data=data, layout=layout)
    plot_url = py.plot(fig)
    return plot_url

def writing_js_file(dict_str, filename='main.js'):
    '''
    writes the main.js file necessary for plotly interactivity with images on hover
    '''

    top_part = '''(function main() {

    var Plot = {
        id: 'plot',
        imgId: 'hover-image',
        domain: 'https://plot.ly'
    };

    Plot.iframe = document.getElementById(Plot.id);
    Plot.graphContentWindow = Plot.iframe.contentWindow;

    Plot.hoverImg = document.getElementById(Plot.imgId);

    Plot.init = function init() {
        var pinger = setInterval(function() {
            Plot.post({task: 'ping'});
        }, 500);

        function messageListener(e) {
            var message = e.data;

            if(message.pong) {
                console.log('Initial pong, frame is ready to receive');
                clearInterval(pinger);

                Plot.post({
                    'task': 'listen',
                    'events': ['hover']
                });
            }
            else if(message.type === 'hover') {
                Plot.onHover(message);
            }
        }

        window.removeEventListener('message', messageListener);
        window.addEventListener('message', messageListener);
    };

    Plot.post = function post(o) {
        Plot.graphContentWindow.postMessage(o, Plot.domain);
    };

    var artistToUrl = {
    '''

    middle_part = for_js_dictionary(dict_str)

    bottom_part = '''};

    var blankImg = 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=';

    Plot.onHover = function(message) {
        var artist = message.points[0].x
            .toLowerCase()
            .replace(/ /g, '-');

        var imgSrc = blankImg;

        if(artistToUrl[artist] !== undefined) imgSrc = artistToUrl[artist];

        Plot.hoverImg.src = imgSrc;
    };

    Plot.init();

    })();
    '''
    with open(filename, 'w') as f:
        f.write(top_part + middle_part + bottom_part)
    return top_part + middle_part + bottom_part

def writing_html_file(plotly_url, js_file, filename='index.html'):
    '''
    writes the index.html file necessary for plotly interactivity with images on hover
    '''

    style_content = '''
    <!DOCTYPE html>>
    <style>
    /* http://stackoverflow.com/questions/11555809/image-overhead-iframe */
    iframe{
      width: 1000px;
      height: 600px;
      border : none;
      z-index: 2;
    }

    img{
      position: absolute;
      left: 400px;
      top: 130px;
      z-index: 3;
      border : none;
      max-width: 400px;
      max-height: 300px;
      align: "middle";
    }
    </style>'''

    body_content = '''
    <body>

    <iframe id="plot" src="{}" seamless></iframe>

    <!-- http://stackoverflow.com/questions/11555809/image-overhead-iframe -->
    <img id="hover-image" src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=">

    <script src='{}'></script>

    </body>

    '''.format(plotly_url, js_file)

    content = style_content + body_content
    with open(filename, 'w') as f:
        f.write(content)
    return content

if __name__ == '__main__':
    #if it is the first time you use plotly, you need to register for a key
    #and run the following line to create the credential file
    # plotly.tools.set_credentials_file(username='AnnaVM', api_key='****')

    # define the path to the credentials (for NYT API)
    path_to_cred_file = '../../credentials/credentials.yml'

    # retrieve the information from the command line
    # for ex: $ python NYT_api.py 'Donald Trump' 1999 2015
    parser = argparse.ArgumentParser(description='Get the evolution of popularity over time')
    parser.add_argument('query_term', metavar='q', type=str, nargs='+',
                        help='a string used as the search term for the query')
    parser.add_argument('start_year', metavar='year_range_start', type=int,
                        help='the year as INT that marks the earliest year queried')

    parser.add_argument('end_year', metavar='year_range_end', type=int,
                        help='the year as INT that marks the latest year queried')

    args = parser.parse_args()

    #search parameters
    terms = args.query_term[0]
    year_start = args.start_year
    year_end = args.end_year

    print ('getting the data from NYT API')
    dict_hits, d_keywords = wraper_function_data(year_start, year_end,
                                terms, path_to_cred_file)
    print ('making the wordclouds')
    d_linked_keywords = handle_multiple_words(d_keywords)
    dict_figs = produce_wordclouds(d_linked_keywords, plot_option=False)
    dict_str = save_images_as_str(dict_figs)
    print('making the bar chart')
    url = plotly_url(year_start, year_end, dict_hits)
    print ('preparing files')
    writing_js_file(dict_str, 'main.js')
    writing_html_file(url, 'main.js', 'index.html')

    print ('in order to have the js execute, run the html on a local server')
    print ('command in terminal $python -m SimpleHTTPServer')
