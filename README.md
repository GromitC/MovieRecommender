# Project Name: Movie Recommendater Using Topic Modelling as Distance Measure
## Installation
1. Anaconda for python scientific computation packages: https://docs.continuum.io/anaconda/install
2. Mongodb: https://www.mongodb.com/
3. Install python packages using pip: https://pypi.python.org/pypi/pip
4. Run install.py to install Python packages
## Usage
### importData.py 
Description: 
This program matches the movies from iMDB and Movie Lens, combine the information and store the standardised data into mongodb. The successfully processed text files will be copied to folder “movieDone”.
Prerequisite:  
1. txt files from folder “MovieTranscriptInputFiles”
2. 'MovieNameMatchedWithMovieLens.txt'

### lda.py 
Description: 
This program computes the topic model and store the preprocessed movie dialogue and model into ’cache/movie.dict’ and 'cache/model.pkl'
Prerequisite:  
1. collection “movie” from database

### calculateJSD.py 
Description: 
This program computes the JSD divergence between each movie based on topic distribution from the LDA model and store the distances into "cache/JSD.pkl"
Prerequisite:  
1. ’cache/model.pkl’: a generated LDA model
2. ’cache/movie.dict’: a pre-processed dictionary of movie transcript

### recommender.py 
Description: 
This program computes the accuracy of item-based recommender and store the results into “result.txt”
Prerequisite:  
1. collection “movie” from database
2. “ratings.csv”

### recommenderMod.py 
Description: 
This program computes the accuracy of item-based recommender and lda recommender and print the result in console.
Prerequisite:  
1. collection “movie” from database
2. “ratings.csv”
3. “JSD.pkl”

]]></content>
  <tabTrigger>readme</tabTrigger>
</snippet>