'''
This python script creates a reporting dashboard that allows the user to
investigate top latent topics (as defined by NMF decompositon) in various
documents of the corpus.

1) the user will be prompted to give a "human" label based on top 10 words of
 the latent topics obtained by NMF decomposition
2) the user can change the list of documents to explore (via their number in
the corpus)

structure of the section <if __name__ == '__main__'>
    #########  GET and CLEAN THE DATA

    #########  From TEXT to VECTOR

    ##########  Define LATENT TOPICS  <<-- place to change number of topics

    ##########  Get TOP LATENT TOPICS for each DOCUMENT (in dictionary)

    ##########  Making the DASHBOARD  <<-- place to change the list of documents

'''

from sklearn.datasets import fetch_20newsgroups

from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.stem.snowball import SnowballStemmer
import re
from string import punctuation

from sklearn import decomposition

import numpy as np


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

def top_latent_topics(W, list_topics, option_100=True):

    '''
    parameters
    ----------
    W as numpy array (each row is an article, each column is a latent topic)
    list_topics as LST
    option_100 as BOOL, defaults to True
            if True: the percentage as represented on a scale from 0 to 100%
            if False: the percentage are represented on a scale from 0 to 1

    returns
    --------
    the most common latent topics for each topic in W with score of importance
    '''
    dic = {}
    for i in xrange(W.shape[0]): #for each document
        indices = np.argsort(W[i])[::-1]
        tot = sum(W[i])
        if tot!=0:
            if option_100: perc = W[i]/tot*100
            elif option_100 == False: perc = W[i]/tot
        #dic[i] = zip(np.array(list_topics)[indices], perc[indices])
        ordered_topics = np.array(list_topics)[indices]
        ordered_percentage = perc[indices]

        select_large_percents = (np.greater_equal(ordered_percentage,10))
        select_small_percents = np.logical_not(select_large_percents)

        others_sum = sum(ordered_percentage[select_small_percents])
        dic[i] = zip(ordered_topics[select_large_percents],
                     ordered_percentage[select_large_percents])
        dic[i].append(('others', others_sum))
    return dic

def write_data_file(doc_num, d, d_top_words):
    with open('../20topics/doc'+ str(doc_num)+'_data.csv','w') as f:
        string = 'name,value,words'
        for topic, value in d[doc_num]:
            string += '\n' + topic + ',' + str(round(value)/100.) + ',' + str(d_top_words[topic])
        f.write(string)

def write_txt_file(list_doc_numbers, data, labels):
    string = ''
    for doc_num in list_doc_numbers:
        label = '''<p id="doc_label'''+str(doc_num)+'''">''' + labels[doc_num] + '''</p>'''
        text = '''<p id="doc'''+str(doc_num)+'''">'''+ data[doc_num] +'''</p>'''
        string += '\n' + label + '\n' + text
    with open('../20topics/text.txt','w') as f:
        f.write(string)

def page_num_function(doc_num):
    '''helper function for the html file writer (dashboard)
    makes an extra entry to the changePage javascript function'''
    entry = '''
           if (pageNum == ''' + str(doc_num) + ''') {
           var csv_document = "doc'''+str(doc_num)+'''_data.csv";
           var text_selection = "#tempDiv #doc'''+str(doc_num)+'''";
           var label_selection = "#tempDiv #doc_label'''+str(doc_num)+'''";
           var exploring = "Exploring document '''+str(doc_num)+'''";
           d3.select("#add_text").html(d3.select(text_selection).html());
           d3.select("#add_label").html(d3.select(label_selection).html());
           d3.csv(csv_document, type, draw);
           d3.select("#explore").html(exploring);
         }'''
    return entry

def make_button(doc_num):
    '''helper function for the html file writer (dashboard)
    creates button'''
    button = '''<input type="button" onclick="changePage('''+str(doc_num)+''');" value="Document '''+str(doc_num)+'''">'''
    return button

def write_html_dashboard(list_doc_numbers):

    head = '''
    <!DOCTYPE 5html>
<meta charset="utf-8">
<head>
  <!-- Bootstrap-->
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">


  <!-- D3js-->
      <script src="//d3js.org/d3.v3.min.js" charset="utf-8"></script>

  <!-- Style-->
  <style>

    body {
      font: 12px sans-serif;
    }

    .axis path,
    .axis line {
      fill: none;
      stroke: #000;
      shape-rendering: crispEdges;
    }

    .bar {
      fill: steelblue;
    }

    .bar:hover {
      fill: orangered ;
    }

    .x.axis path {
      display: none;
    }


  </style>

  <!-- Load .txt file-->
  <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
  <script type="text/javascript">
     jQuery(function($){
         $ ('#tempDiv').load("text.txt");});
  </script>

  <!-- javascript functions-->
  <script>

   function changePage(pageNum) {
        d3.select('svg').remove();
'''
    pageNumFunction = ''
    for doc_num in list_doc_numbers:
        pageNumFunction += page_num_function(doc_num)

    drawFunction = '''
    }

    function draw(data){
      var margin = {top: 40, right: 20, bottom: 30, left: 40},
          width = 480 - margin.left - margin.right,
          height = 250 - margin.top - margin.bottom;

      var formatPercent = d3.format(".0%");

      var x = d3.scale.ordinal()
          .rangeRoundBands([0, width], .1);

      var y = d3.scale.linear()
          .range([height, 0]);

      var xAxis = d3.svg.axis()
          .scale(x)
          .orient("bottom");

      var yAxis = d3.svg.axis()
          .scale(y)
          .orient("left")
          .tickFormat(formatPercent);

      var svg = d3.select(".svg_holder").append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
        .append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

          x.domain(data.map(function(d) { return d.name; }));
          y.domain([0, d3.max(data, function(d) { return d.value; })]);

          svg.append("g")
              .attr("class", "x axis")
              .attr("transform", "translate(0," + height + ")")
              .call(xAxis);

          svg.append("g")
              .attr("class", "y axis")
              .call(yAxis)
            .append("text")
              .attr("y", -30)
              .attr("dy", "1em")
              .style("text-anchor", "start")
              .text("Relative Latent Topic Importance");

          svg.selectAll(".bar")
              .data(data)
            .enter().append("rect")
              .attr("class", "bar")
              .attr("x", function(d) { return x(d.name); })
              .attr("width", x.rangeBand())
              .attr("y", function(d) { return y(d.value); })
              .attr("height", function(d) { return height - y(d.value); })

              .on('mouseover', function(d){
                d3.select(".words")
                  .html("<p><strong>Top words for latent topics</strong> for <span style='color:red'><strong>" + d.name + "</strong></span>:</p>" + "<p>"  + d.words + "</p>")
              })
              .on('mouseout', function(d){
                d3.select(".words")
                  .html('')
              })

        }

        function type(d) {
          d.value = +d.value;
          return d;
        }
  </script>



</head>'''

    body = '''
<body>

  <div>
    <h3>Hello!</h3>
    <p> Use this dashboard to see the repartition of latent topics to describe
       a choosen reference document in the <i>20 Newsgroup Dataset</i>.
      Click on the button below to set this reference document.</p>
  </div>

  <div class='container'>
    <b>Choose the document to study</b>
    <div class='buttons'>
    '''

    buttons = ''
    for doc_num in list_doc_numbers:
        buttons += make_button(doc_num)


    end_body = '''
    </div>



  <div id="explore"></div>
  <div class='svg_holder'></div>
  <div class='words'></div>

  <div id="tempDiv" style="display:none;"></div>
  <div class="panel panel-default">
      <div class="panel-heading"> More information
      </div>
      <div class="panel-body">
        <div>Original category in the <i>20 Newsgroup Dataset</i>:
              <strong><span id="add_label"></span></strong>
        </div>

        <div>Text: <p id="add_text"></p>
        </div>
      </div>
  </div>


</body>'''
    string = head + pageNumFunction + drawFunction+ body + buttons + end_body
    with open('../20topics/dashboard.html','w') as f:
        f.write(string)

if __name__ == '__main__':

    #########  GET and CLEAN THE DATA
    print('Get data')
    newsgroups_train = fetch_20newsgroups(subset='train',
                                          remove=('headers', 'footers', 'quotes'))
    data = newsgroups_train.data
    full_labels = newsgroups_train.filenames
    labels = [label.split('/')[-2] for label in full_labels]

    snowball = SnowballStemmer('english')
    regex = re.compile('[%s]' % re.escape(punctuation))

    print('Clean data')
    clean_data_snow = map(lambda doc: clean_stemmed_doc(doc, regex, snowball), data)

    #########  From TEXT to VECTOR
    print('Apply vectorizer')
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)

    sparse_vectors = tfidf_vectorizer.fit_transform(clean_data_snow)
    vectors = sparse_vectors.toarray()
    words = tfidf_vectorizer.get_feature_names()

    ##########  Define LATENT TOPICS
    print('Define latent topics')
    n_components = 20
    W,H,nmf = topic_modeling(n_components, vectors)
    print '-'*20
    print 'Looking at {} topics.'.format(n_components)
    print '-'*20
    d = {}
    list_terms = top_terms(H,words)
    list_topics = []
    for lst in list_terms:
        print lst
        label = raw_input('What label do you want to set? ')
        list_topics.append(label)
    print '\n'
    print '-'*10
    print list_topics
    print '\n' + '*'*50

    ##########  Get TOP LATENT TOPICS for each DOCUMENT (in dictionary)
    d = top_latent_topics(W, list_topics)

    d_top_words = {} ###put top words for each topic in a dictionary as a string
    for i in range(len(list_topics)):
        topic = list_topics[i]
        word_list = top_terms(H,words)[i]
        d_top_words[topic] = ' / '.join(word_list)
    d_top_words['others'] = ' '

    ##########  Making the DASHBOARD
    print('Making the dashboard')
    list_doc_numbers = [0,10,100, 200, 300, 500, 1000]
    for doc_num in list_doc_numbers:
        write_data_file(doc_num, d, d_top_words)
    write_txt_file(list_doc_numbers, data, labels)
    write_html_dashboard(list_doc_numbers)
