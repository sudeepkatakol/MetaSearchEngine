from WebInterface import get_search_results, scrape
from threading import Thread
from Queue import Queue
import numpy as np

'''
This subclass of Thread helps in concurrent scraping of the url's fetched from google results.  
'''
class ScraperThread(Thread):
    def __init__(self, queue, put_list, model):
        '''
        queue cantains the google results to be scraped and classified
        put_list: will contain the SearchResults with the probability distribution calculated for them
        model is required from processing the document as a vector
        '''
        Thread.__init__(self)
        self.queue = queue
        self.model = model
        self.put_list = put_list

    def run(self):
        '''
		Does the following:
		1) Scrapes
        2) Gets the vector representation for the scraped document
        3) Fetches the probability distribution for the document using the vector
        '''
        while True:
            result = self.queue.get()
            print 'Fetching ' + result.link + " ..."
            try:
                text = scrape(result.link)
            except:
            	print "Couldn't fetch " + result.link
                self.queue.task_done()
            	continue
            text = self.model.process_document(text)
            vec1 = self.model.get_vector_for_processed_document(text)
            vec2 = self.model.get_vector_for_processed_document(text)
            vec3 = self.model.get_vector_for_processed_document(text)
            vec = np.mean(np.array([vec1, vec2, vec3]), axis = 0)
            result.distribution = self.model.get_distribution_from_classifier(vec)
            result.calc_top3()
            self.put_list.append(result)
            self.queue.task_done()

'''
This class handles all the necessary actions required when an user types in query to search.
'''
class SearchPageHandlerScraperThreads:
    def __init__(self, search_query, modelandclassifier, pages=1):
        '''
        Gets the google search results and the probability distribution for each result
        '''
        self.search_query = search_query
        self.modelandclassifier = modelandclassifier
        self.search_results = get_search_results(self.search_query, page_limit=pages)
        self.scrape_queue = Queue()
        self.final_results = []
        self._action()
        del self.search_results
        if len(self.final_results) == 0:
            raise Exception

    def _action(self):
    	'''
    	Concurrent scraping with the help of ScraperThreads
    	'''
        for i in range(8):
            t = ScraperThread(self.scrape_queue, self.final_results, self.modelandclassifier)
            t.daemon = True
            t.start()

        for item in self.search_results:
            self.scrape_queue.put(item)

        self.scrape_queue.join()

    def determine_class(self):
    	'''
    	Finds the sum of the probabilities for each class and returns the class with maximum sum 
    	'''
        aggregate = np.squeeze(np.sum([result.distribution for result in self.final_results], axis=0))
        index = np.argmax(aggregate)
        return index

    def get_sorted_results(self, index):
    	'''
    	sorts the result according the probabilities wrt class (specified by index)
    	'''
        dist = [result.distribution for result in self.final_results]
        sorting_base = np.squeeze(np.transpose(dist)[index])
        return [res for (y, res) in reversed(sorted(zip(sorting_base, self.final_results)))]

'''
Code from the internet which may be of use:

This didn't work because Scraping time >> (time to infer vector + time to process document)

class SearchPageHandler:
    def __init__(self, search_query, modelandclassifier):
        self.search_query = search_query
        self.modelandclassifier = modelandclassifier
        self.search_results = get_search_results(self.search_query)
        self.to_scrape_queue = Queue()
        self.to_vectorise_queue = Queue()
        self.to_get_distribution_queue = Queue()
        self.final_results = []

    def action(self):
        worker1 = ScraperThread(self.to_scrape_queue, self.to_vectorise_queue)
        worker2 = VectorisingThread(self.to_vectorise_queue, self.to_get_distribution_queue, self.modelandclassifier)
        worker3 = ProbabilityDistributionThread(self.to_get_distribution_queue, self.final_results, self.modelandclassifier)
        worker1.daemon = True
        worker2.daemon = True
        worker3.daemon = True
        worker1.start()
        worker2.start()
        worker3.start()
        for i in range(len(self.search_results)):
            self.to_scrape_queue.put(self.search_results[i])
        self.to_scrape_queue.join()
        self.to_vectorise_queue.join()
        self.to_get_distribution_queue.join()

'''
'''
    for x in range(8):
        worker = DownloadWorker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
    # Put the tasks into the queue as a tuple
    for link in links:
        logger.info('Queueing {}'.format(link))
        queue.put((download_dir, link))
'''

'''
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print('Remaining :' + str(len(queued_links)))
        create_jobs()

def create_jobs():
    for x in file_to_set(QUEUE_FILE):
        queue.put(x)
    queue.join()
    create_jobs()

def create_workers():
    for _ in range(NO_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()
'''