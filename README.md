# SearchEngine

Simple search engine implementation, using IDF nad LSI.

## Requirements
project implemented using __python 3.7__.<br/>
Compatibility with python < 3.5 is not guaranteed.<br/>
To install needed requirements, navigate in command prompt to project's main folder and type:<br/>
`pip install -r requirements.txt`

## Run 
run project by navigating in command prompt to project's main folder and typing:<br/>
`python manage.py runserver`, or open project using pycharm which would detect django project automatically.

## Resources
Attached database (sqlite) contains 2200 Simple Wiki articles.<br/>
Design provided by simple [w3 css framework](https://www.w3schools.com/w3css/) 

## Search Process
For each article, bag-of-words vector is created (after previous stemming and removing stop words). WordsDictionary is a union set of all
existing words in provided articles. Bag-of-words vectors are rescaled using Inverse Document Frequency.<br/>
If SVD option is chosen, term-by-document matrix is approximated using SVD and low rank approximation.
