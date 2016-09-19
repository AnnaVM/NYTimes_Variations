# Trending? Not Trending?

**AIM:** Investigating the evolution of the popularity of a term, as the number of hits over the years for the search term on the NY Times API.

**OUPUT:** Interactive bar chart of the number of hits over the years with a wordcloud on hover action to give the keywords most often associated with the articles retrieved.

**USAGE:**

`$ python NYT_api_advanced 'search_term' start_year end_year`

with `'search_term'` (a STR) the term to query the NYT API for, and the years between `start_year` (as INT) and `end_year` (as INT) the time range to look at.

To investigate the graph on your local computer, you will need a local server (as Javascript are not well rendered with the 'file' protocol)

`$python -m SimpleHTTPServer`
 then go to 'http://localhost:8000/' (or which ever port number the server is running on) to open the html file.

## Examples

#### Popularity of term 'Data Science' from 2010-2016

command line: `$ python NYT_api_advanced 'Data Science' 2010 2016`

Page: https://annavm.github.io/NYTimes_Variations/trending_not_trending/example_0/

Screenshot: ![Screenshot of example_0][ex_0]

#### Popularity of term 'Donald Trump' from 2005-2015

command line: `$ python NYT_api_advanced 'Donald Trump' 2005 2015`

Page: https://annavm.github.io/NYTimes_Variations/trending_not_trending/example_1/

Screenshot: ![Screenshot of example_1][ex_1]


#### Popularity of term 'Terrorism' from 2005-2015

command line: `$ python NYT_api_advanced 'terrorism' 2005 2015`

Page: https://annavm.github.io/NYTimes_Variations/trending_not_trending/example_2/

Screenshot: ![Screenshot of example_2][ex_2]


[ex_0]: https://github.com/AnnaVM/NYTimes_Variations/blob/master/trending_not_trending/images/plotly_Data_Science.png "Screenshot for the interactive bar graph for the trend in search term Data Science from 2010 to 2016"

[ex_1]: https://github.com/AnnaVM/NYTimes_Variations/blob/master/trending_not_trending/images/plotly_Donald_Trump.png "Screenshot for the interactive bar graph for the trend in search term Donald Trump from 2005 to 2015"

[ex_2]: https://github.com/AnnaVM/NYTimes_Variations/blob/master/trending_not_trending/images/plotly_terrorism.png "Screenshot for the interactive bar graph for the trend in search term terrorism from 2005 to 2015"

## Code
Two python files are available **NYT_api.py** and **NYT_api_advanced.py**.

- **NYT_api.py** is meant to be an introduction to APIs and the different programming steps (setting up credentials, parsing arguments, sending a GIT request...) are detailled in the accompanying markdown **Follow_Along.md**.

- **NYT_api_advanced.py** is the file containing the code necessary to obtain the interactive bar graphs. A Jupyter Notebook 'Explore.ipynb' is available if you want to explore the various functions for yourself.
