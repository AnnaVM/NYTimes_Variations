# NYTimes_Variations
This repository contains various small data science project/python programs based on  the New York Time resources (API) and corpus of other news aricles to answer a general question and produce a visual overview/tool. The first project looks into using APIs ('Trending or not Trending'). The second project will cover Topic Modeling with the 20 newsgroup dataset.

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

Screencast: ![dashboard demo](https://github.com/AnnaVM/NYTimes_Variations/blob/master/trending_not_trending/example_0/Dashboard_Demo_DataScience.gif "Dashboard demo for Data Science query")

Screenshot: ![Screenshot of example_0][ex_0]


[ex_0]: https://github.com/AnnaVM/NYTimes_Variations/blob/master/trending_not_trending/images/plotly_Data_Science.png "Screenshot for the interactive bar graph for the trend in search term Data Science from 2010 to 2016"

## So, what's your topic? A Topic Modeling project

-- in construction

*Resource:*  20 newsgroups dataset (New York Times corpus is behind a paywall for me)

This dataset, available in scikit-learn, comprises around 18000 newsgroups posts on 20 topics.

- I first look into the impact of the vectorization scheme on the document representation, with a simple bar chart based interactive interface for investigation.
- I then compute the most similar documents in the corpus for a given document, and as a sanity check, I investigate the categories, or labels, associate with those documents. A D3js dashboard sums up the information.

Dashboard demo:
![dashboard demo](https://github.com/AnnaVM/NYTimes_Variations/blob/master/what_topic/example_1/similar_docs_dashboard.gif "Dashboard demo for document 13")

Link to the Dashboard:
https://annavm.github.io/NYTimes_Variations/what_topic/example_1/dashboard.html
