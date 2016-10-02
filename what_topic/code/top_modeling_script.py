from sklearn.datasets import fetch_20newsgroups

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.snowball import SnowballStemmer

from sklearn import decomposition

import numpy as np

import re
from string import punctuation

def clean_stemmed_doc(doc, regex, snowball):
    '''
    parameters
    -----------
    doc as STR
    regex: re to remove punctuation
           regex = re.compile('[%s]' % re.escape(punctuation))
    snowball: instance of Snowball Stemmer
            snowball = SnowballStemmer('english')

    returns
    -------
    the document as STR
                lowercased, all punctuation removed,
                numbers and words containing numbers removed
                stemmed (Snowball)
    '''
    str_num = [str(num) for num in range(10)]
    set_str_num = set(str_num)

    #returns a list
    clean_doc = [regex.sub(' ', word.lower()).strip() for word in doc.split()\
                if (set(list(word)).intersection(set_str_num)) == set()]
    clean_text = ' '.join(clean_doc)
    #returns a list
    lemmatized_doc = [snowball.stem(word) for word in clean_text.split()]

    return ' '.join(lemmatized_doc)

def top_terms(H,feature_names, top_n=10):
    '''
    parameters
    ----------
    H as np.array
        (each row is a topic, each column is a term)
    feature_names as LST
    top_n as INT
            the number of top words for each topic

    returns
    -------
    as LST the top_n most common words for each topic in H
    '''
    lst_words = []
    for i in xrange(H.shape[0]):
        indices = np.argsort(H[i])[::-1][:top_n]
        lst_words.append(np.array(feature_names)[indices])
    return lst_words

def topic_modeling(n_components, vectors):
    '''
    parameters
    ----------
    n_component: as INT
                number of latent topic we want to uncover
    vectors: the document-words matrix

    returns
    -------
    W, H , nmf (fitted to vectors)
        vectors = WH
        with vectors (m rows-ie datapoints/articles, p columns-ie words of vocabulary)
             W (m rows, n_components columns) --> contains top topics for document
             H (n_components rows, p columns) --> contains top word for topic
    '''
    nmf = decomposition.NMF(n_components=n_components)
    nmf.fit(vectors)
    W = nmf.transform(vectors) #shape: (11314, 6)
    H = nmf.components_ #shape: (6, 5000)
    return W, H, nmf

def vary_n_components(list_num_components, vectors, verbose=True):
    '''
    parameters
    ----------
    list_num_components: as LST of INT
                        values to be given to the nmf decomposition
    vectors: term-document matrix
    verbose: as BOOL, defaults True
            gives indications on the state of completion

    returns
    -------
    dictionary where n_component is the key and (W, H, nmf) the values
                nmf is fitted to vectors
                vectors = WH
    '''
    d_components = {}
    for n_components in list_num_components:
        if verbose: print('working for {} components'.format(n_components))
        W,H,nmf = topic_modeling(n_components, vectors)
        d_components[n_components] = (W, H, nmf)
    return d_components

def set_topics(d_components):
    '''
    interactive script that ask the user to come up with a general topic
    based on the top_n words that define it.
    It goes through however number of topics (n_components) present in the
    dictionary d_components
    '''
    d_labels = {}
    first_run = True
    for n_component in sorted(d_components):
        print '-'*20
        print 'Looking at {} topics.'.format(n_component)
        print '-'*20
        if first_run:
            d = {}
            W,H,nmf = d_components[n_component]
            list_terms = top_terms(H,words)
            for lst in list_terms:
                print lst
                label = raw_input('What label do you want to set? ')
                d[label] = set(lst)
            d_labels[n_component] = d
            first_run = False
            print '\n'
            print '-'*10
            print d.keys()
            print '\n' + '*'*50
            previous_key = n_component
            go_on = raw_input('add more topics?(y/n) ')
            if go_on == 'n': break
        else:
            d = {}
            new_labels = set()
            W,H,nmf = d_components[n_component]
            list_terms = top_terms(H,words)
            for lst in list_terms:
                common_max = 0
                output = 'N/A'
                for label in d_labels[previous_key]:
                    set1 = d_labels[previous_key][label]
                    common = len(set(lst) & set1)
                    if common > common_max and common > 2:
                        output = label
                        common_max = common
                    elif common == common_max & common > 2:
                        output +=' ' + label
                print lst
                print 'previous label(s): {}'.format(output)
                if (output in new_labels):
                    label = raw_input('Label is already in use. What label do you want to set? ')
                    new_labels.add(label)
                if output not in new_labels:
                    response = raw_input('keep label?(y/n): ')
                    if response == 'y':
                        label = output
                        new_labels.add(label)
                    elif response == 'n':
                        label = raw_input('What label do you want to set? ')
                        new_labels.add(label)
                d[label] = set(lst)
            d_labels[n_component] = d
            print '\n'
            print '-'*10
            print d.keys()
            print 'newly set labels: ', set(d.keys()) - set(d_labels[previous_key].keys())
            print 'discarded labels: ', set(d_labels[previous_key].keys()) - set(d.keys())
            print '\n' + '*'*50
            go_on = raw_input('add more topics?(y/n) ')
            if go_on == 'n': break
            previous_key = n_component
    return d_labels, d_labels[n_component].keys()

if __name__ == '__main__':
    ################  GET DATA

    newsgroups_train = fetch_20newsgroups(subset='train',
                                          remove=('headers', 'footers', 'quotes'))

    data = newsgroups_train.data

    ################  CLEAN DATA
    snowball = SnowballStemmer('english')
    regex = re.compile('[%s]' % re.escape(punctuation))
    clean_data_snow = map(lambda doc: clean_stemmed_doc(doc, regex, snowball), data)

    ################  FROM TEXT TO VECTOR
    #max feature is limited here
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    sparse_vectors = tfidf_vectorizer.fit_transform(clean_data_snow)
    vectors = sparse_vectors.toarray()
    words = tfidf_vectorizer.get_feature_names()

    ################  TOPIC MODELING
    d_components = vary_n_components(range(4,23,2), vectors)
    d_labels, set_topics = set_topics(d_components)
