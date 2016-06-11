
# coding: utf-8

# In[86]:
import logging
from pymongo import MongoClient
import numpy as np
import re
from stop_words import get_stop_words
from collections import defaultdict
import itertools
from gensim import corpora
from gensim.models import LdaMulticore
from gensim.models.ldamodel import LdaModel
from gensim.models.hdpmodel import HdpModel
import string
import copy 
import operator
from joblib import Parallel, delayed  
import multiprocessing
from gensim.models import LdaMulticore
from gensim.models.hdpmodel import HdpModel


# In[2]:

client = MongoClient('localhost')
db = client.ISOM

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# In[3]:

def clean_essay(string, lower=False):
    string = re.sub(r"\\t", " ", string)   
    string = re.sub(r"\\n", " ", string)   
    string = re.sub(r"\\r", " ", string)   
    string = re.sub(r"[^A-Za-z']", " ", string)   
    string = re.sub(r"\s{2,}", " ", string)
    if lower:
        string = string.lower()
    return string.strip()


# In[4]:

def processingWords(word):
    if ((word.lower() not in stop_words) and (len(word)>3)and (not word.isupper())):
        return word.lower()
    else:
        return None


# In[6]:

names=['james', 'john', 'robert', 'michael', 'william', 'david', 'richard', 'charles', 'joseph', 'thomas',
       'christopher', 'daniel', 'paul', 'mark', 'donald', 'george', 'kenneth', 'steven', 'edward', 'brian',
       'ronald', 'anthony', 'kevin', 'jason', 'matthew', 'gary', 'timothy', 'jose', 'larry', 'jeffrey', 'frank',
       'scott', 'eric', 'stephen', 'andrew', 'raymond', 'gregory', 'joshua', 'jerry', 'dennis', 'walter', 'patrick',
       'peter', 'harold', 'douglas', 'henry', 'carl', 'arthur', 'ryan', 'roger', 'joe', 'juan', 'jack', 'albert',
       'jonathan', 'justin', 'terry', 'gerald', 'keith', 'samuel', 'willie', 'ralph', 'lawrence', 'nicholas', 'roy',
       'benjamin', 'bruce', 'brandon', 'adam', 'harry', 'fred', 'wayne', 'billy', 'steve', 'louis', 'jeremy', 'aaron',
       'randy', 'howard', 'eugene', 'carlos', 'russell', 'bobby', 'victor', 'martin', 'ernest', 'phillip', 'todd',
       'jesse', 'craig', 'alan', 'shawn', 'clarence', 'sean', 'philip', 'chris', 'johnny', 'earl', 'jimmy', 'antonio',
       'danny', 'bryan', 'tony', 'luis', 'mike', 'stanley', 'leonard', 'nathan', 'dale', 'manuel', 'rodney', 'curtis',
       'norman', 'allen', 'marvin', 'vincent', 'glenn', 'jeffery', 'travis', 'jeff', 'chad', 'jacob', 'lee', 'melvin',
       'alfred', 'kyle', 'francis', 'bradley', 'jesus', 'herbert', 'frederick', 'ray', 'joel', 'edwin', 'don',
       'eddie', 'ricky', 'troy', 'randall', 'barry', 'alexander', 'bernard', 'mario', 'leroy', 'francisco', 'marcus',
       'micheal', 'theodore', 'clifford', 'miguel', 'oscar', 'jay', 'jim', 'tom', 'calvin', 'alex', 'jon', 'ronnie',
       'bill', 'lloyd', 'tommy', 'leon', 'derek', 'warren', 'darrell', 'jerome', 'floyd', 'leo', 'alvin', 'tim',
       'wesley', 'gordon', 'dean', 'greg', 'jorge', 'dustin', 'pedro', 'derrick', 'dan', 'lewis', 'zachary', 'corey',
       'herman', 'maurice', 'vernon', 'roberto', 'clyde', 'glen', 'hector', 'shane', 'ricardo', 'sam', 'rick',
       'lester', 'brent', 'ramon', 'charlie', 'tyler', 'gilbert', 'gene', 'mary', 'patricia', 'linda', 'barbara',
       'elizabeth', 'jennifer', 'maria', 'susan', 'margaret', 'dorothy', 'lisa', 'nancy', 'karen', 'betty', 'helen',
       'sandra', 'donna', 'carol', 'ruth', 'sharon', 'michelle', 'laura', 'sarah', 'kimberly', 'deborah', 'jessica',
       'shirley', 'cynthia', 'angela', 'melissa', 'brenda', 'amy', 'anna', 'rebecca', 'virginia', 'kathleen',
       'pamela', 'martha', 'debra', 'amanda', 'stephanie', 'carolyn', 'christine', 'marie', 'janet', 'catherine',
       'frances', 'ann', 'joyce', 'diane', 'alice', 'julie', 'heather', 'teresa', 'doris', 'gloria', 'evelyn', 'jean',
       'cheryl', 'mildred', 'katherine', 'joan', 'ashley', 'judith', 'rose', 'janice', 'kelly', 'nicole', 'judy',
       'christina', 'kathy', 'theresa', 'beverly', 'denise', 'tammy', 'irene', 'jane', 'lori', 'rachel', 'marilyn',
       'andrea', 'kathryn', 'louise', 'sara', 'anne', 'jacqueline', 'wanda', 'bonnie', 'julia', 'ruby', 'lois', 'tina',
       'phyllis', 'norma', 'paula', 'diana', 'annie', 'lillian', 'emily', 'robin', 'peggy', 'crystal', 'gladys',
       'rita', 'dawn', 'connie', 'florence', 'tracy', 'edna', 'tiffany', 'carmen', 'rosa', 'cindy', 'grace', 'wendy',
       'victoria', 'edith', 'kim', 'sherry', 'sylvia', 'josephine', 'thelma', 'shannon', 'sheila', 'ethel', 'ellen',
       'elaine', 'marjorie', 'carrie', 'charlotte', 'monica', 'esther', 'pauline', 'emma', 'juanita', 'anita',
       'rhonda', 'hazel', 'amber', 'eva', 'debbie', 'april', 'leslie', 'clara', 'lucille', 'jamie', 'joanne',
       'eleanor', 'valerie', 'danielle', 'megan', 'alicia', 'suzanne', 'michele', 'gail', 'bertha', 'darlene',
       'veronica', 'jill', 'erin', 'geraldine', 'lauren', 'cathy', 'joann', 'lorraine', 'lynn', 'sally', 'regina',
       'erica', 'beatrice', 'dolores', 'bernice', 'audrey', 'yvonne', 'annette', 'june', 'samantha', 'marion', 'dana',
       'stacy', 'ana', 'renee', 'ida', 'vivian', 'roberta', 'holly', 'brittany', 'melanie', 'loretta', 'yolanda',
       'jeanette', 'laurie', 'katie', 'kristen', 'vanessa', 'alma', 'sue', 'elsie', 'beth', 'claire', 'andy', 'joey',
       'doug', 'chuck', 'ben', 'oliver', 'ethan', 'franklin', 'natalie', 'miller', 'jenny', 'evan', 'kate', 'simon',
       'claude', 'sid', 'crawford', 'austin','ali','dylan','brad','nina','jake','lincoln','brad','stu','reilly','romeo',
       'neil','benny','willy','jackie','graham','ellie',"cont'd"]

# In[40]:

stop_words = get_stop_words('english')
stop_words+=list(string.ascii_lowercase)
cursor = db.movies.find({},{"dialogue":1})

documents=[]
for document in cursor:
    if document['dialogue']:
        temp= clean_essay(document['dialogue'].encode('utf-8')).decode('utf-8')
    documents.append(temp.split())


# In[41]:

documents = [[token.lower() for token in text if  len(token)>=3] for text in documents]


# In[42]:

occurance= defaultdict(int)
for text in documents:
    tmpToken= list(set(text))
    for val in tmpToken:
        occurance[val]+=1


# In[43]:

documents = [[token for token in text if  occurance[token]>10] for text in documents]


# In[44]:

frequency = defaultdict(int)
for text in documents:
    for token in text:
        frequency[token] += 1


# In[45]:

limit=sorted(frequency.iteritems(), key=operator.itemgetter(1), reverse=True)[100][1]
documents = [[token for token in text if  frequency[token]<limit] for text in documents]


# In[46]:

newTexts=[]
for text in documents:
    tmpText=list(set(text)-set(text).intersection(names))
    tmpResult=filter(lambda a: a in tmpText, text)
    newTexts.append(tmpResult)
  


# In[49]:

dictionary = corpora.Dictionary(newTexts)
corpus = [dictionary.doc2bow(text) for text in newTexts]


# In[59]:

newfrequency = defaultdict(int)
for text in newTexts:
    for token in text:
        newfrequency[token] += 1

# In[87]:

logger.info("Generating topics from LDA")

num_topics=100
model=LdaModel(num_topics=num_topics,corpus=corpus,id2word=dictionary,iterations=1500)
#model=LdaMulticore(num_topics=100,workers=3,corpus=corpus,id2word=dictionary,iterations=3000)
#model=HdpModel(corpus=corpus, id2word=dictionary)

# In[94]:

model.save('cache/model.pkl')


# In[96]:

cursor = db.movies.find({},{"movieId":1})
movieId=[]
for doc in cursor:
    movieId.append(doc['movieId'])


# In[97]:

movieDict={}
for i,val in enumerate(movieId):
    movieDict[val]=newTexts[i]


# In[98]:

import joblib
joblib.dump(movieDict,'cache/movie.dict')


# In[ ]:



