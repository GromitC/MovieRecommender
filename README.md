#####################################################################################
Program Name: importData.py 

Description: This program matches the movies from iMDB and Movie Lens, combine the information and store the standardised data into mongodb. The successfully processed text files will be copied to folder “movieDone”.

Prerequisite:  1. txt files from folder “MovieTranscriptInputFiles”
		2. 'MovieNameMatchedWithMovieLens.txt'
#####################################################################################
Program Name: lda.py 

Description: This program computes the topic model and store the preprocessed movie dialogue and model into ’cache/movie.dict’ and 'cache/model.pkl'

Prerequisite:  1. collection “movie” from database
#####################################################################################
Program Name: calculateJSD.py 

Description: This program computes the JSD divergence between each movie based on 
topic distribution from the LDA model and store the distances into "cache/JSD.pkl"

Prerequisite:  1. ’cache/model.pkl’: a generated LDA model
		2. ’cache/movie.dict’: a pre-processed dictionary of movie transcript
#####################################################################################
Program Name: recommender.py 

Description: This program computes the accuracy of item-based recommender and store the results into “result.txt”

Prerequisite:  1. collection “movie” from database
		2. “ratings.csv”
#####################################################################################
Program Name: recommenderMod.py 

Description: This program computes the accuracy of item-based recommender and lda recommender and print the result in console.

Prerequisite:  1. collection “movie” from database
		2. “ratings.csv”
		3. “JSD.pkl”
#####################################################################################

