# So, what's your topic?

**AIM:** Investigating the impact of various scikit-learn feature extraction methods (get the counts, remove stopwords, apply tfidf, lemmatize). Model the topics in the news post and be able to predict the topics of previously unlabeled posts.


# Investigating vectorizers

Usage: run the script and choose the document to investigate, thanks to its number, in the example we are looking at 13.

```code
$python vectorizer_script.py 13
```

This generates .csv files of top words and their counts/tfidf value, as well as a small dashboard to explore the output for that document.

Dashboard demo:
![dashboard demo](https://github.com/AnnaVM/NYTimes_Variations/blob/master/what_topic/data/document_13.gif "Dashboard demo for document 13")

Link to the Dashboard:
https://annavm.github.io/NYTimes_Variations/what_topic/data/document_100_dashboard.html
