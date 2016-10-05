# So, what's your topic?

**AIM:** Investigating the impact of various scikit-learn feature extraction methods (get the counts, remove stopwords, apply tfidf, lemmatize). Modeling the topics in the documents (unsupervised learning - matrix factorization).


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

Here are some latent topics that appear as the number of components increases:

- <b>science</b>: [space, nasa, orbit, program, launch, shuttl, data, develop, scienc, research]
- <b>bike</b>: [bike, ride, motorcycl, dod, rider, helmet, mile, look, honda, buy]
- <b>car</b>: [car, engin, dealer, driver, mile, speed, look, model, owner, buy]
- <b>guns</b>: [gun, law, right, govern, peopl, state, crime, weapon, crimin, firearm]


# Determining the latent topics characterizing documents

Looking at the W matrix in V = WH matrix factorization gives information as to which latent topics are important for each document. I translate this information into relative percentage importance, disregarding topics that account for less that 10% of the total importance. To see how these latent topics correlate back to the original file, the actual text is displayed as well as the category it was originally from.

Dashboard demo:
![dashboard demo](https://github.com/AnnaVM/NYTimes_Variations/blob/master/what_topic/20topics/latent_topic_demo.gif "Demo - looking at latent topics for documents")

Link to the Dashboard:
https://annavm.github.io/NYTimes_Variations/what_topic/20topics/dashboard.html


If you want to have access to the code, or run the script yourself:

```code
$python latent_topic_script.py
```
# Latent topics and categories

In order to compare latent topics to original categories the documents belonged to, I designed a heatmap that shows the graphical representation of documents repartition between categories and latent topics.

A first heatmap is obtained for 20 latent topics (20 components in the matrix factorization), as a sanity check. Some clear correlations reinforce the validity of the latent topics.
![20_topics](https://github.com/AnnaVM/NYTimes_Variations/blob/master/what_topic/images/20_components.png)
- car: rec.autos and rec.motocycles
- israel: talk.politics.mideast
- space: sci.space
- sales: misc.forsale
- sports: rec.sport.hockey and rec.sport.baseball
- religion: mainly soc.religion.christian and to a smaller extend alt.atheism and talk.religion.misc
- computer security: sci.crypt
- opinion: evenly partitioned across categories

A second heatmap, for only 10 latent topics, allows more general topics to be defined.
![10_topics](https://github.com/AnnaVM/NYTimes_Variations/blob/master/what_topic/images/10_components.png)

A Jupyter notebook [Heatmap.ipynb](https://github.com/AnnaVM/NYTimes_Variations/blob/master/what_topic/code/Heatmap.ipynb) allows the user to design heatmaps for the desired number of latent topics.
