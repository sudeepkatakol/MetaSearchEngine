# MetaSearchEngine
## Disclaimer:
The algorithm scrapes the content of pages whose url links are obtained when the search engine is queried. Hence, you may be banned from accessing certain websites.

I've used this software locally and haven't been *completely* banned from any websites


## What is this software about?

This software is a miniature version of Metasearch engine developed keeping in mind the interest of middle school students. The algorithm fetches Google results for a given user query and sorts the results according to the students' needs. 


## How to use it?

To use the software locally on your Linux system: 

When using for the first time,

Open the downloaded directory on terminal and execute  `bash run.sh`

Follow the instructions dictated by the script

__Note__: Make sure you have [Anaconda] installed on your system.

[Anaconda]: https://www.continuum.io/downloads

Later on, you can either execute either `bash run.sh`   or   `source activate metasearchengine && python Webapp.py` to run the app

Open the url (displayed on your terminal window) on your browser to run the application


## How does it work?
When you query the search engine, it gathers search results from Google and scrapes the corresponding pages to obtain a document for each result.

The software uses a Doc2Vec model trained (using DBOW algorithm) on the Wikipedia Dataset to obtain vector representations for documents.

Then the classifier returns a probability distribution for each result using the document vectors and the results are sorted according to the class with highest aggregate probability or with respect to the class user enters.
