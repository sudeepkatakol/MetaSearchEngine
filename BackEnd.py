import gensim
import numpy as np
from time import time

class ModelAndClassifier:
    def __init__(self):
        print 'Loading wiki model... '
        s = time()
        # Load the pretrained model available in enwiki_dbow. See the README file for more 
        try :
            self.model = gensim.models.Doc2Vec.load('./enwiki_dbow/doc2vec.bin')
        except Exception as e:
            print(e)
            print ("Couldn't load the model. Exiting")
            exit()
        y = time()
        print 'Model loading time ' + str(y - s)
        try :
            self.W = np.load('./model/Averaged20times_W_(300, 8).npy')
            self.b = np.load('./model/Averaged20times_b_(8).npy')
        except Exception as e:
            print(e)
            print ("Couldn't load the W, b parameters. Exiting")
            exit()

    def process_document(self, document):
        '''
        type(document) = string
        return a list of words for document given as a string
        '''
        return gensim.utils.simple_preprocess(document)

    def get_vector_for_processed_document(self, processed_doc):
        '''
        type(processed_doc) = list
        processed_doc is a list of strings.
        returns the vector
        '''
        return self.model.infer_vector(processed_doc)

    def get_distribution_from_classifier(self, x):
        '''
        returns the probability distribution (in %) for a vec. This probability distribution is obtained from the Neural Network
        '''
        y = np.matmul(x, self.W) + self.b
        return _softmax(y) * 100

# Helper function
def _softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()
