
# coding: utf-8

# In[117]:

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


# In[16]:

df=pd.read_csv('ratings.csv')


# In[39]:

client = MongoClient('localhost')
db = client.ISOM
cursor = db.movies.find({},{"movieId":1})
movieId=[]
for document in cursor:
    movieId.append(int(document['movieId']))


# In[44]:

filteredDf=df[df['movieId'].isin(movieId)]


# In[104]:

bytag = filteredDf.groupby('userId').aggregate(np.count_nonzero)
tags = bytag[bytag.movieId >= 500].index #remove movies with ratings fewer than 500
df=filteredDf[filteredDf['userId'].isin(tags)]


# In[107]:

test=df.groupby('userId')


# In[108]:

data={}


# In[109]:

for key, grp in test:
    Test=grp.drop('userId',axis=1)
    data[key]=Test.set_index('movieId').T.to_dict('records')[0]
    


# In[110]:

model = DictDataModel(data)


# In[111]:

similarity = ItemSimilarity(model,sim_euclidian)


# In[113]:

items_strategy=PreferredItemsNeighborhoodStrategy()


# In[114]:

recSys = ItemRecommender(model, similarity, items_strategy)


# In[118]:

evaluator=AverageAbsoluteDifferenceRecommenderEvaluator()


# In[120]:

result=[]
for i in range(1,10):
    result.append(evaluator.evaluate(recSys,model,0.1*i,1-(0.1*i)))
with open('result.txt', 'w') as f:
    for s in result:
        f.write(str(s) + '\n')

