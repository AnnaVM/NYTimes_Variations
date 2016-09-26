from sklearn.datasets import fetch_20newsgroups

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

import numpy as np

def get_data(categories, subset='train', clean_option='True'):
    ###########   loading the data
    newsgroups_train = fetch_20newsgroups(subset=subset,
                                       categories=categories)
    data = fetch_20newsgroups(subset='train', categories=categories).data

    ###########   clean the data
    #remove _ in the texts
    if clean_option:
        data_clean = []
        for document in data:
            data_clean.append(document.replace('_', ' ').lower())
        return data_clean
    data_lowercase = []
    for document in data:
        data_lowercase.append(document.lower())
    return data

def process_documents(vectorizer_option, data):
    if vectorizer_option == 'counts':
        vectorizer = CountVectorizer()
    elif vectorizer_option == 'counts_stopwords':
        vectorizer = CountVectorizer(stop_words='english')
    elif vectorizer_option == 'tfidf':
        vectorizer = TfidfVectorizer(stop_words='english')

    vectors = vectorizer.fit_transform(data).toarray()
    words = vectorizer.get_feature_names()

    return vectors, words

def frequent_words(int_article, vectors, words):
    counts = vectors[int_article] #get the counts
    mask = (vectors[int_article]!=0) #get the non null values
    #let us deal only with words relevant for this article
    array_words = np.array(words)[mask]
    array_values = counts[mask]
    #sorting everything
    index = np.argsort(array_values)[::-1]
    sorted_words = array_words[index]
    sorted_values = np.round(array_values[index],2)
    return sorted_words, sorted_values

def build_dict_csv(data, article_num, top_n_words=10, verbose=True):
    dict_csv = dict()
    list_vectorizer_option = ['counts', 'counts_stopwords', 'tfidf']
    for i in range(1,4):
        vectorizer_option = list_vectorizer_option[i-1]
        csv_filename = 'document_'+ str(article_num)+'_data_'+ str(i) +'.csv'
        vectors, words = process_documents(vectorizer_option, data)
        words, values = frequent_words(article_num, vectors, words)
        dict_csv[i] = csv_filename, words, values, top_n_words
        if verbose:
            print vectorizer_option, 'done'
    return dict_csv

if __name__ == '__main__':
    from build_d3 import make_3_d3_graph
    import sys
    ###########################################################
    ##              GET THE DATA
    ###########################################################

    #restrain categories
    categories = ['alt.atheism', 'talk.religion.misc',
               'comp.graphics', 'sci.space']
    data = get_data(categories, subset='train', clean_option='True')

    ###########################################################
    ##              GET THE DASHBOARD
    ###########################################################
    document_num = int(sys.argv[-1])
    dict_csv = build_dict_csv(data, document_num)
    make_3_d3_graph('document_'+str(document_num)+'_dashboard.html',
                    dict_csv, document_num)
