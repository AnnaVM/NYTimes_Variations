'''
python 2.7

this script writes the html file for a dashboard enabling to obtain the top n
most similar documents to a reference document, and to observe the repartition
of the categories (Science, Politics...) that this similar documents have.

The corpus used is from 20 Newsgroup training dataset

The .csv files and the .html file are stored in a folder that must be created
'./labels_percentage'
author: AnnaVM
'''

from sklearn.datasets import fetch_20newsgroups

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

from nltk.stem.snowball import SnowballStemmer

from sklearn.metrics.pairwise import cosine_similarity

import numpy as np
import re
from string import punctuation

from collections import Counter

def general_labels_apply(label):
    '''
    from the 20 labels possible, extract one of the 6 possible categories
    suggested on the 20 Newsgroups homepage (my labels)

        # description:
        # COMPUTER 'comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware',
        # 'comp.sys.mac.hardware', 'comp.windows.x',
        # MISCELLANEOUS 'misc.forsale',
        # HOBBIES 'rec.autos', 'rec.motorcycles', 'rec.sport.baseball','rec.sport.hockey',
        # SCIENCE 'sci.crypt', 'sci.electronics', 'sci.med', 'sci.space',
        # RELIGION 'soc.religion.christian', 'talk.religion.misc', 'alt.atheism',
        # POLITICS 'talk.politics.guns', 'talk.politics.mideast', 'talk.politics.misc'

    parameter
    ---------
    label as STR ('xxx.xxxx.xxxx')
    returns
    -------
    category as STR
    '''
    if label[0:5] == 'comp.':
        return 'Computer'
    elif label[0:4] == 'rec.':
        return 'Hobbies'
    elif label[0:4] == 'sci.':
        return 'Science'
    elif label[0:14] == 'talk.politics.':
        return 'Politics'
    elif label[0:5] == 'misc.':
        return 'Miscellaneous'
    else:
        return 'Religion'

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

def get_closest_docs(input_vector, top_n=100):
    '''
    parameters
    ----------
    input_vector: as np.array
                vector from similarity matrix (with cosine similarity)
    top_n: as INT
          the number of closest documents

    returns
    -------
    index: array of the index of the documents from closest to farthest
            the top n, with the document itself (ie closest) is removed
    values: cosine similarity between the document of interest
            ordered with the index
    '''
    index = np.argsort(input_vector)[::-1]
    values = input_vector[index]
    return index[1:top_n+1], values[1:top_n+1]

def get_counts_labels(index, labels):
    '''
    parameters
    ----------
    index: as array
            from get_closest_docs
    labels: as LST of STR
            either the 20 newsgroups or the 6 global labels
    returns
    -------
    counter, with label as key and counts as value
    '''
    return Counter(list(np.array(labels)[index]))

def write_csv_file(filename, counter):
    with open('../labels_percentage/'+filename, 'w') as f:
        f.write('journal,count')
        for label, count in counter.most_common(len(counter)):
            new_line = '\n'+label+','+str(count)
            f.write(new_line)


def wrapper_function(filename, input_vector,top_n, labels):
    index, values = get_closest_docs(input_vector, top_n)
    counter = get_counts_labels(index, labels)
    write_csv_file(filename, counter)

def write_dashboard(document_nums, similarity, labels, top_n=100):
    '''
    parameters
    ----------
    document_nums: as LST of INT, the list has a length 4
                  the index of the documents in the corpus that
                  will be investigated
    similarity matrix (cosine similarity)
    labels: as LST of STR,
            as a list of labels of the documents in the corpus
    top_n: as INT (the number of most similar documents)
    '''
    ########## write the 4 .csv
    for document_num in document_nums:
        csv_filename = "document_"+str(document_num)+"_data.csv"
        wrapper_function(csv_filename, similarity[document_num], top_n, labels)

    ######### write the html for the dashboard
    with open('../labels_percentage/dashboard.html', 'w') as f:
        head = '''<!DOCTYPE html>
        <html>
          <head>
        <!-- Bootstrap-->
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

        <!-- D3js-->
            <script src="//d3js.org/d3.v4.min.js" charset="utf-8"></script>

        <!-- setting style -->
            <style>
              .legend {
                font-size: 12px;
              }

              rect {
                stroke-width: 2;
              }

              #chart {
                height: 360px;
                position: relative;
                width: 360px;
              }

              .label {
                color: #333;
              }

              div.tooltip {
                position: absolute;
                text-align: center;
                width: 120px;
                height: 50px;
                padding: 2px;
                font: 14px sans-serif;
                background: lightsteelblue;
                border: 0px;
                border-radius: 8px;
                pointer-events: none;
              }

              .disclaimer{
                font: 12px sans-serif;
                color: grey;
              }
            </style>
        <!-- end setting style -->
        '''
        script = '''
        <!-- script -->
          <script>
            <!-- buttons + heading of panel-->
            function changePage(pageNum) {
                d3.select('svg').remove();
                if (pageNum == 0) { d3.csv("document_'''+str(document_nums[0])+'''_data.csv", draw);
                                    d3.select("#add_text").html("Exploring document '''+ str(document_nums[0]) +'''");}
                if (pageNum == 1) { d3.csv("document_'''+str(document_nums[1])+'''_data.csv", draw);
                                    d3.select("#add_text").html("Exploring document '''+ str(document_nums[1]) +'''"); }
                if (pageNum == 2) { d3.csv("document_'''+str(document_nums[2])+'''_data.csv", draw);
                                    d3.select("#add_text").html("Exploring document '''+ str(document_nums[2]) +'''");}
                if (pageNum == 3) { d3.csv("document_'''+str(document_nums[3])+'''_data.csv", draw);
                                    d3.select("#add_text").html("Exploring document '''+ str(document_nums[3]) +'''");}
            }

            <!-- donut graph -->
            function draw(dataset){

                <!-- fixed variables -->
                var width = 500;
                var height = 360;
                var radius = Math.min(width, height) / 2;
                var donutWidth = 75;

                var legendRectSize = 18;
                var legendSpacing = 4;

                var color = d3.scaleOrdinal(d3.schemeCategory20b);

                <!-- adding svg -->
                var svg = d3.select('#chart')
                    .append('svg')
                    .attr('width', width)
                    .attr('height', height)
                    .append('g')
                    .attr('transform', 'translate(' + radius +  ',' + radius + ')');

                <!-- adding the tooltip properties -->
                var tooltip = d3.select('#chart')
                    .append('div')
                    .attr('class', 'tooltip');

                tooltip.append('div')
                    .attr('class', 'label');

                tooltip.append('div')
                    .attr('class', 'count');

                tooltip.append('div')
                    .attr('class', 'percent');

                <!-- adding the arc properties for the donut chart-->
                var arc = d3.arc()
                    .innerRadius(radius-donutWidth)
                    .outerRadius(radius);

                <!-- converting count data to number -->
                dataset.forEach(function(d) {
                    d.count = +d.count;
                });

                <!-- adding the data to the pie chart, and getting path-->
                var pie = d3.pie()
                    .value(function(d) { return d.count; })
                    .sort(null);

                var path = svg.selectAll('path')
                    .data(pie(dataset))
                    .enter()
                    .append('path')
                    .attr('d', arc)
                    .attr('fill', function(d, i) {
                        return color(d.data.journal);
                    });

                <!-- setting tooltip functions-->
                path.on('mouseover', function(d) {
                    tooltip.transition()
                           .duration(200)
                           .style("opacity", .9);
                    var total = d3.sum(dataset.map(function(d) {
                        return d.count;
                    }));
                    var percent = Math.round(1000 * d.data.count / total) / 10;
                    tooltip.select('.label').html(d.data.journal);
                    tooltip.select('.count').html(d.data.count);
                    tooltip.select('.percent').html(percent + '%');
                    tooltip.style("left", (radius-60) + "px")
                           .style("top", (radius-25) + "px")
                });

                path.on('mouseout', function(d) {
                    tooltip.transition()
                           .duration(200)
                           .style("opacity", 0);
                });

                <!-- setting legend properties-->
                var legend = svg.selectAll('.legend')
                    .data(color.domain())
                    .enter()
                    .append('g')
                    .attr('class', 'legend')
                    .attr('transform', function(d, i) {
                        var height = legendRectSize + legendSpacing;
                        var offset =  height * color.domain().length / 2;
                        var horz = 5/4 * radius;
                        var vert = i * height - offset;
                        return 'translate(' + horz + ',' + vert + ')';
                        });

                legend.append('rect')
                      .attr('width', legendRectSize)
                      .attr('height', legendRectSize)
                      .style('fill', color)
                      .style('stroke', color);

                legend.append('text')
                      .attr('x', legendRectSize + legendSpacing)
                      .attr('y', legendRectSize - legendSpacing)
                      .text(function(d) { return d; });

            }
            <!-- end donut graph -->
        </script>
        </head>
        '''

        body = '''
        <body>
          <div>
            <h3>Hello!</h3>
            <p> Use this dashboard to see the repartition of labels of the top '''+str(top_n)+'''
              most similar documents to a choosen reference document in the <i>20 Newsgroup Dataset</i>.
              Click on the button below to set this reference document.</p>
          </div>

          <div class='container'>
            <b>Choose the document to study</b>
            <div class='buttons'>
                <input type="button" onclick="changePage(0);" value="Document '''+str(document_nums[0])+'''">
                <input type="button" onclick="changePage(1);" value="Document '''+str(document_nums[1])+'''">
                <input type="button" onclick="changePage(2);" value="Document '''+str(document_nums[2])+'''">
                <input type="button" onclick="changePage(3);" value="Document '''+str(document_nums[3])+'''">
            </div>

        <div class="panel panel-primary">
            <div class="panel-heading">
                <h3 id='add_text' class="panel-title"></h3>
            </div>

            <div class="panel-body">
                <p> <b>Donut chart with the labels of the top '''+str(top_n)+''' most similar documents (in terms of cosine similarity)</b> </p>
                <div id='chart'></div>
                <p></p>
                <p> <b> More details on the process </b>
                  <ul>
                    <li>The data was cleaned: the text was lowercased, all punctuation was removed, words were stemmed.</li>
                    <li>The documents were transformed into vectors with a Tf-Idf Vectorizer with stopwords.</li>
                    <li>The similarity matrix is then calculated (choosen distance metric: cosine similarity). </li>
                  </ul>

                The possible labels, based on categories from the <i>20 Newsgroup Dataset</i> website, are:
                Science, Politics, Miscellaneous, Hobbies, Religion, Computer.
                </p>
            </div>
        </div>


        <p class='disclaimer'> Disclaimer: pie charts and donut charts are probably not the best vizualization
          to convey percentages. But I loved the challenge of writing this neat interactive graph in D3js. Thanks to
          Zero Viscosity for his awesome tutorial.</p>
        <!-- http://zeroviscosity.com/d3-js-step-by-step/step-2-a-basic-donut-chart-->

        </body>
    </html>
    '''
        f.write(head + script + body)


if __name__ == '__main__':

    #######################################################
    ####            Get the data
    #######################################################

    ##########      text documents
    # keeping the information in the headers, footers (signature) and quotes
    # is not very realistic
    newsgroups_train = fetch_20newsgroups(subset='train',
                                      remove=('headers', 'footers', 'quotes'))

    data = newsgroups_train.data  #as a LST of docs (each document is a string)
    print('data loaded')
    ##########      labels
    full_labels = newsgroups_train.filenames #with the full path to file

    labels = [label.split('/')[-2] for label in full_labels]

    general_labels = map(general_labels_apply, labels)
    print('labels/categories made')
    #######################################################
    ####            Clean the texts
    #######################################################

    snowball = SnowballStemmer('english')
    regex = re.compile('[%s]' % re.escape(punctuation))

    clean_data_snow = map(lambda doc: clean_stemmed_doc(doc, regex, snowball), data)
    print('data cleaned')
    #######################################################
    ####            From texts to vectors
    #######################################################

    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    sparse_vectors = tfidf_vectorizer.fit_transform(clean_data_snow)
    vectors = sparse_vectors.toarray()
    words = tfidf_vectorizer.get_feature_names()
    print('corpus was vectorized')
    #######################################################
    ####            Finding similar vectors
    #######################################################

    full_similarity = cosine_similarity(vectors, vectors)
    print('similarity matrix was computed')
    document_nums = [1,100,200,300]
    write_dashboard(document_nums, full_similarity, general_labels, top_n=100)
