# NYTimes_Variations
This repository contains various small data science project/python programs based on  the New York Time resources (API, corpus...) to answer a general question and produce a visual overview/tool. The first project looks into using APIs ('Trending or not Trending'). The second project will cover Topic Modeling with NY Times corpus.

WORK IN PROGRESS

## Trending or not Trending

-- Finished project

*Resource:* New York Times API


This [project](https://github.com/AnnaVM/NYTimes_Variations/tree/master/trending_not_trending) was inspired by a [DLab](http://dlab.berkeley.edu/) workshop  "Extracting Data through Web APIs in Python" led by Rochelle Terman at UC Berkeley.


* **Global Picture:** Is the subject of "Donald Trump" trending? This interactive bar chart will allow you to explore the evolution of the popularity of your chosen search word over a certain time frame.

* **Technical Milestones:** The popularity of a search term is defined as the number of articles published on the subject in the New York Times. Goals: i) query the New York Times API, ii) set up a reporting tool (interactive bar chart), iii) develop a user-friendly way of showing corresponding keywords (wordclouds)

Goal *i* is inline with the DLab workshop aims, goals *ii* and *iii* go further.

* **Teaching Aim:** read the **Follow_Along.md** markdown to have a step-by-step built-up of the simple script **NYT_api.py**

*Sample Output*
#### Popularity of term 'Data Science' from 2010-2016

command line: `$ python NYT_api_advanced 'Data Science' 2010 2016`

Page: https://annavm.github.io/NYTimes_Variations/trending_not_trending/example_0/

Screenshot: ![Screenshot of example_0][ex_0]


[ex_0]: https://github.com/AnnaVM/NYTimes_Variations/blob/master/trending_not_trending/images/plotly_Data_Science.png "Screenshot for the interactive bar graph for the trend in search term Data Science from 2010 to 2016"

## Topic Modeling

-- coming up

*Resource:* New York Times corpus
