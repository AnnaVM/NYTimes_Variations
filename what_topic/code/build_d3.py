'''
the aim of this script is to provide functions that will build a d3 bar chart from a
list of words and a corresponding list of their counts. It builds a .csv file and
the html file

format of csv (must include header):
word,frequency
cat,2

the output is an html file with the d3 bar graph
'''

def write_csv(csv_filename, words, values, top=10):
    '''
    parameters
    ----------
    csv_filename: name of the file (will be in data folder)
    words: as LST
           list of words (as string)
    values: as LST
            list of counts (as integer)
    top: as INT, defaults to 10
         the number of most frequent words kept

    creates a .csv file in the data folder
    '''
    with open('../data/'+csv_filename, 'w') as f:
        header = 'word,frequency'
        f.write(header)
        for i in range(len(words)):
            if i>= top:
                break
            entry = '\n' + str(words[i]) +',' + str(values[i])
            f.write(entry)

def d3js_html(html_filename, csv_filename, document_num):
    '''
    parameters
    ----------
    html_filename: as STR
                   name of the file (will be in data folder)
    csv_filename: as STR
                  name of the file (will be in data folder)
            csv format:
            word,frequency
            cat,3
    information_text: as STR
                     text that will appear on top of the bar graph

    creates a .html file in the data folder
    '''
    #####################################################################
    ####                      start file
    #####################################################################

    ########## starting the html
    html = '''
        <!DOCTYPE html>
     <html> '''

    ########## creating the head - with d3js source
    head = '''
       <head>
         <script src="//d3js.org/d3.v3.min.js" charset="utf-8"></script>'''

    ########## creating the style
    style = '''
         <style>

         .chart rect {
           fill: steelblue;
         }

         .chart text {
           fill: white;
           font: 10px sans-serif;
           text-anchor: end;
         }

    .chart rect {
      fill:  #0072c8;
    }

    .chart rect:hover {
      fill: #968C83;
    }

    .y path, .y stroke, .y line {
      display: none;
    }

    .x path, .x stroke {
      display: none;
      shape-rendering: crispEdges;
    }

    .y text {
      font-family: 'Open Sans';
      font-size: 14px;
      text-anchor: middle;
    }

    .x text {
      font-family: 'Open Sans';
      font-size: 10px;
      text-anchor: middle;
    }
    </style>'''

    ########## creating the script with the draw function
    script ='''
    <script>
    function changePage(pageNum) {
          d3.select('svg').remove();
          if (pageNum == 1) { d3.csv("document_'''+str(document_num)+'''_data_1.csv", draw); }
          if (pageNum == 2) { d3.csv("document_'''+str(document_num)+'''_data_2.csv", draw); }
          if (pageNum == 3) { d3.csv("document_'''+str(document_num)+'''_data_3.csv", draw); }
      }

    function draw(data){

      var width = 420,
          barHeight = 20;

      var x = d3.scale.linear()
          .range([0, width]);

      var chart = d3.select("body")
            .append('svg')
            .attr("class", 'chart')
          .attr("width", width)

          data.forEach(function (d){ d.frequency = +d.frequency;});
          x.domain([0, d3.max(data, function(d){
            return d.frequency;
          })]);

        chart.attr("height", barHeight * data.length);

        var bar = chart.selectAll("g")
            .data(data)
          .enter().append("g")
            .attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")"; });

        bar.append("rect")
            .attr("width", function(d) { return x(d.frequency);})
            .attr("height", barHeight - 1);

        bar.append("text")
            .attr("x", function(d) { return x(d.frequency) - 3; })
            .attr("y", barHeight / 2)
            .attr("dy", ".35em")
            .text(function(d) { return d.word + '  -->  ' + d.frequency; });

    }
    </script>'''
    ########## creating the full head
    full_head = html + head + style + script + '''
       </head>
    '''

    #####################################################################
    ####                      body of html
    #####################################################################
    body_prior_loading_data = '''
       <body>

        <p> ''' + 'document' + str(document_num) + '''</p>

         <h1>Select Vectorizer:</h1>
         <input type="button" onclick="changePage(1);" value="Count Vectorizer">
         <input type="button" onclick="changePage(2);" value="Count Vectorizer with stop words">
         <input type="button" onclick="changePage(3);" value="Tfidf Vectorizer">

         <p> Bar chart with the most frequent word (word --> value) </p>
    '''

    body_loading_data = '''
        <script>
        d3.csv("''' + csv_filename + '''", draw);

        </script>

       </body>
     </html>'''

    full_body = body_prior_loading_data + body_loading_data

    #####################################################################
    ####                      write html file
    #####################################################################
    with open('../data/'+html_filename, 'w') as f:
        f.write(full_head + full_body)

def make_d3_graph(html_filename, csv_filename,
                  words, values,
                  information_text='',
                  top=10):
    '''
    this is a wrapper function for the functions write_csv and d3js_html
    see functions for parameters
    '''
    write_csv(csv_filename, words, values, top=top)
    d3js_html(html_filename, csv_filename, information_text=information_text)

def make_3_d3_graph(html_filename, dict_csv, document_num):
    '''
    this is a wrapper function for the functions write_csv and d3js_html
    parameters
    ----------

    dict_csv as csv:
        key: vectorizer_option
        value:  csv_filename, words, values, top
    '''
    for vectorizer_option in range(1,4):
        csv_filename, words, values, top = dict_csv[vectorizer_option]
        write_csv(csv_filename, words, values, top=top)
    d3js_html(html_filename, dict_csv[1][0], document_num=document_num)
