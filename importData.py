import pandas as pd
import csv
import copy 
import os
from HTMLParser import HTMLParser
import re
import difflib
from pymongo import MongoClient

#os.chdir('/Users/gromit/ISOM_Recommender/recommender/')
# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		if (tag != 'br') and (tag != 'td')and (tag != 'tr'):
			startTag.append(tag)
	def handle_endtag(self, tag):
		endTag.append(tag)
	def handle_data(self, data):
		Data.append(data)

directory='MovieTranscriptInputFiles'
filename = 'MovieNameMatchedWithMovieLens.txt'
articles = []

# Using the newer with construct to close the file automatically.
with open(filename) as f:
	data = f.readlines()

category={
	'movieId':None,
	'movieName':None,
	'tag':None,
	'dialogue':None
}
movieLens=[]
movieNames=[]
for row in data:
	row =row.rstrip('\n')
	temp=copy.deepcopy(category)
	content=row.split("::")
	temp['movieId']=content[0]
	temp['movieName']=content[1][:-7]
	temp['tag']=content[2].split('|')
	movieNames.append(temp['movieName'])
	movieLens.append(temp)

for file in os.listdir(directory):
	if file.endswith(".txt"):
		articles.append(file)

for file in articles:
	f= open(directory+"/"+file, "r")
	file_list = f.read()
	startTag=[]
	endTag=[]
	Data=[]
	parser = MyHTMLParser()
	parser.feed(file_list)
	movieName= file.replace('-',' ').replace('.txt','')
	dialogue=''
	startIterate=False
	for item in Data:
		tmp=re.sub(' +',' ',item.replace('\n','')).strip()
		if tmp=='User Comments':
			break
		if item=='ALL SCRIPTS':
			startIterate=True
			continue
		if startIterate:
			dialogue+=" "+tmp
	try:
		(item for item in movieLens if item["movieName"] == movieName).next()['dialogue']=dialogue
		movieNames.remove(movieName)
		articles.remove(file)
		os.rename("MovieTranscriptInputFiles/"+file, "movieDone/"+file)
	except StopIteration:
		haha=0

for file in articles:
	f= open(directory+"/"+file, "r")
	file_list = f.read()
	startTag=[]
	endTag=[]
	Data=[]
	parser = MyHTMLParser()
	parser.feed(file_list)
	movieName= file.replace('-',' ').replace('.txt','')
	dialogue=''
	startIterate=False
	for item in Data:
		tmp=re.sub(' +',' ',item.replace('\n','')).strip()
		if tmp=='User Comments':
			break
		if item=='ALL SCRIPTS':
			startIterate=True
			continue
		if startIterate:
			dialogue+=" "+tmp

	try:
		(item for item in movieLens if item["movieName"] == movieName).next()['dialogue']=dialogue
		movieNames.remove(movieName)
		os.rename("MovieTranscriptInputFiles/"+file, "movieDone/"+file)
	except StopIteration:
		notFound=True
		counter=0
		duplicates=[]
		matchedName= ''
		for name in movieNames:
			seq=difflib.SequenceMatcher(a=movieName,b=name)
			if (movieName.replace(', The','').lower()==name.replace(', The','').lower()) or (movieName.replace('The ','').lower()==name.replace('The ','').lower())or(movieName.replace(', The','').lower()==name.replace('The ','').lower()) or (movieName.replace('The ','').lower()==name.replace(', The','').lower() or (movieName.replace(' ','-')==name)):
				matchedName=name
				notFound=False
				counter=1
				break
			if seq.ratio()>0.9 or (movieName in name) or (movieName.replace(', The','')in name) or (movieName.replace('The ','')in name):
				duplicates.append(name)
				matchedName=name
				notFound=False
				counter+=1
		if counter == 1:
			(item for item in movieLens if item["movieName"] == matchedName).next()['dialogue']=dialogue
			movieNames.remove(matchedName)
			articles.remove(file)
			os.rename("MovieTranscriptInputFiles/"+file, "movieDone/"+file)
		elif counter>1:
			print movieName.replace('-',' ').replace('.txt','')+' has duplicate results.'
		if notFound:
			print movieName.replace('-',' ').replace('.txt','')+' not found.'



export=[]
for items in movieLens:
	if items['dialogue']!=None:
		export.append(items)

client = MongoClient('localhost',27017)
db = client.ISOM 									#database name
posts = db.movies									#collection name

result = posts.insert_many(export)
print result.inserted_ids
