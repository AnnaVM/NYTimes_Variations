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

# Investigating similar documents

Usage: run the script and choose the 4 documents to investigate, thanks to their number. We are looking at [1, 100, 200, 300] (hardcoded in script). A '../labels_percentage' folder must exist.

```code
$python similar_documents_script.py
```

This generates .csv files of top words and their counts/tfidf value, as well as a small dashboard to explore the output for that document.

Dashboard demo:
![dashboard demo](https://github.com/AnnaVM/NYTimes_Variations/blob/master/what_topic/example_1/similar_docs_dashboard.gif "Dashboard demo for document 13")

Link to the Dashboard:
https://annavm.github.io/NYTimes_Variations/what_topic/example_1/dashboard.html

# Investigating latent topics

NMF decomposition transforms the vector-matrix (V) into a product of matrices (V = WH). This section explores the information in H, the next will focus on W. The dimensions of W and H are fixed by those of the vector matrix V and by the number of components we set for the matrix decomposition. H links the number of latent topics (number of components chosen) to the words in the vocabulary developped by TfIDF algorithm. A human user can explore the words in each topic to set a global label for the latent topic discovered. A Jupyter notebook [Explore_topics.ipynb](https://github.com/AnnaVM/NYTimes_Variations/blob/master/what_topic/number_topics/Explore_topics.ipynb) allows you to do just that. This is where the magic of matrix decomposition for topic discovery really kicks in!

Exploration demo:
![ipynb demo](https://github.com/AnnaVM/NYTimes_Variations/blob/master/what_topic/number_topics/set_number_topics.gif "Demo for looking at topics for varying number of components")

If you want to have access to the code, or run the script yourself:
```code
$python top_modeling_script.py
```
