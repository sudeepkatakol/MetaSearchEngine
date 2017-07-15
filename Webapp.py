#!/home/sudeep/anaconda3/envs/tensorflow/bin/python

'''
Entry point for the program flow of the application.
'''
import sys
from ConcurrentServer import SearchPageHandlerScraperThreads
from BackEnd import ModelAndClassifier
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def welcome():
	'''
	Displays the welcome page. See static/welcome.html
	'''
	return render_template('welcome.html')


@app.route('/search/', methods=['POST', 'GET'])
def search():
    '''
    Handles the requests from the search page.
    '''
    global handler, prev_no_of_pages, back_end, prev_search_query


    # Obtain data from the webpage
    if request.method == 'POST':
        search_query = request.form['query']
        index = request.form['class']
        no_of_pages = request.form['no_of_pages']
    else:
        search_query = request.args.get('query')
        index = request.args.get('class')
        no_of_pages = request.args.get('no_of_pages')
    no_of_pages = int(no_of_pages)
    index = index.split('/')[0]
    print 'Index: ' + str(index)
    index = int(index)

    # If the search query and the no. of pages are same, then use previous handler object, no need to create another one 
    if search_query != prev_search_query or prev_no_of_pages != no_of_pages:
    	handler = SearchPageHandlerScraperThreads(search_query, back_end, pages=no_of_pages)
    	prev_search_query = search_query
    	prev_no_of_pages = no_of_pages

    if index == -1:
       	sort_index = handler.determine_class()
    else:
    	sort_index = index
    return render_template('index2.html', results=handler.get_sorted_results(sort_index), search_query=search_query, index=index)


if __name__ == '__main__':
    # Use UTF-8 encoding because python 2 doesn't use UTF-8 as default encoding
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    back_end = ModelAndClassifier()
    prev_search_query = None
    prev_no_of_pages = None
    handler = None
    
    # For debugging use:
    # app.run(debug=True)
    app.run()
