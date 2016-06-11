
# coding: utf-8

# In[1]:

from models.datamodel import *
from recommender.topmatches import *
from recommender.recommender import UserRecommender, ItemRecommender, SlopeOneRecommender
from recommender.utils import DiffStorage
from similarities.similarity import UserSimilarity, ItemSimilarity
from similarities.similarity_distance import *
from neighborhood.itemstrategies import  PreferredItemsNeighborhoodStrategy
import pandas as pd
import numpy as np
from pymongo import MongoClient
from evaluation.statistics import AverageAbsoluteDifferenceRecommenderEvaluator
from topicSimilarity import *
import joblib 
from joblib import Parallel, delayed 
import multiprocessing


# In[2]:

df=pd.read_csv('ratings.csv')


# In[3]:

client = MongoClient('localhost')
db = client.ISOM
cursor = db.movies.find({},{"movieId":1})
movieId=[]
for document in cursor:
    movieId.append(int(document['movieId']))


# In[4]:

filteredDf=df[df['movieId'].isin(movieId)]


movieListCount={}
for ids in movieId:
    movieListCount[ids]=filteredDf[filteredDf.movieId==ids].userId.count()


one=[]
two=[]
three=[]
four=[]
five=[]
sort=sorted(movieListCount.values())
for keys in movieListCount:
    if movieListCount[keys]<=sort[200]:
        one.append(keys)
        continue
    if (movieListCount[keys]>sort[200])and (movieListCount[keys]<=sort[400]):
        two.append(keys)
        continue
    if (movieListCount[keys]>sort[400])and (movieListCount[keys]<=sort[600]):
        three.append(keys)
        continue 
    if (movieListCount[keys]>sort[600])and (movieListCount[keys]<=sort[800]):
        four.append(keys)
        continue 
    if movieListCount[keys]>sort[800]:
        five.append(keys)
        continue 

ratingList=[one,two,three,four,five]



def parallel(evaluator,recSys,model,i):
     return evaluator.evaluate(recSys,model,0.1*i,1-(0.1*i))

for ratingRange in ratingList:
    selectedMovieRatings=filteredDf[filteredDf['movieId'].isin(ratingRange)]

    bytag = selectedMovieRatings.groupby('userId').aggregate(np.count_nonzero)
    Tags = [bytag[(bytag.movieId < 100)].index,bytag[(bytag.movieId > 200)&(bytag.movieId < 300)].index,bytag[(bytag.movieId > 300)&(bytag.movieId < 400)].index,bytag[(bytag.movieId > 400)&(bytag.movieId < 500)].index,bytag[(bytag.movieId > 500)].index]
    label=1
    for tags in Tags:
        print 'Iteration: '+str(label)
        df=selectedMovieRatings[selectedMovieRatings['userId'].isin(tags)]

        dummy=[0,0,0,0]
        dummy2=[0,0,0,0]
        for i in range(0,10):
            if (len(df)>100000):
                test=df.sample(100000).groupby('userId')
            else:
                test=df.groupby('userId')
            data={}
            for key, grp in test:
                Test=grp.drop('userId',axis=1)
                data[key]=Test.set_index('movieId').T.to_dict('records')[0]
            model = DictDataModel(data)
            similarity = ItemSimilarity(model,topicSimilarityCache,topicDistribution=joblib.load('cache/JSD.pkl'),movieIndex=movieId)
            items_strategy=PreferredItemsNeighborhoodStrategy()
            recSys = ItemRecommender(model, similarity, items_strategy)
            evaluator=AverageAbsoluteDifferenceRecommenderEvaluator()
            temp=Parallel(n_jobs=3)(delayed(parallel)(evaluator,recSys,model,i) for i in range(6,10))
            for a in range(0,4):
                dummy[a]+=temp[a]
            similarity = ItemSimilarity(model,sim_euclidian)
            items_strategy=PreferredItemsNeighborhoodStrategy()
            recSys = ItemRecommender(model, similarity, items_strategy)
            evaluator=AverageAbsoluteDifferenceRecommenderEvaluator()
            temp=Parallel(n_jobs=3)(delayed(parallel)(evaluator,recSys,model,i) for i in range(6,10))
            for a in range(0,4):
                dummy2[a]+=temp[a]
        dummy2=[str(x/10) for x in dummy2]
        dummy=[str(x/10) for x in dummy]
        print "LDA: "+' '.join(dummy)
        print "Item-Based: "+' '.join(dummy2)
        print
        label+=1

