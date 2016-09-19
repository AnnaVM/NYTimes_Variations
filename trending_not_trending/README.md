# Trending? Not Trending?

**AIM:** Investigating the evolution of the popularity of a term, as the number of hits over the years for the search term on the NY Times API.

**OUPUT:** Interactive bar chart of the number of hits over the years with a wordcloud on hover action to give the keywords most often associated with the articles retrieved.

**USAGE:**
`$ python NYT_api_advanced 'search_term' start_year end_year`
with `'search_term'` (a STR) the term to query the NYT API for, and the years between `start_year` (as INT) and `end_year` (as INT) the time range to look at.

## Examples

#### Popularity of term 'Donald Trump' from 2005-2015

command line: `$ python NYT_api_advanced 'Donald Trump' 2005 2015`
Page: https://annavm.github.io/NYTimes_Variations/trending_not_trending/example_1/

Screenshot: ![Screenshot of example_1][ex_1]


#### Popularity of term 'Terrorism' from 2005-2015

command line: `$ python NYT_api_advanced 'terrorism' 2005 2015`
Page: https://annavm.github.io/NYTimes_Variations/trending_not_trending/example_2/

Screenshot: ![Screenshot of example_2][ex_2]


[ex_1]: https://github.com/AnnaVM/NYTimes_Variations/blob/master/trending_not_trending/images/plotly_Donald_Trump.png "Screenshot for the interactive bar graph for the trend in search term Donald Trump from 2005 to 2015"

[ex_2]: https://github.com/AnnaVM/NYTimes_Variations/blob/master/trending_not_trending/images/plotly_terrorism.png "Screenshot for the interactive bar graph for the trend in search term terrorism from 2005 to 2015"

## Code
