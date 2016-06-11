# -*- coding: utf-8 -*- 
import numpy as np
import re
from collections import defaultdict
import itertools
import string
import copy 
import operator
import joblib
import multiprocessing
from scipy import stats
from numpy import zeros, array
from math import sqrt, log

def KL_divergence(p, q):
		""" Compute KL divergence of two vectors, K(p || q)."""
		return sum(_p * log(_p / _q) for _p, _q in zip(p, q) if _p != 0)
def Jensen_Shannon_divergence(p, q):
		""" Returns the Jensen-Shannon divergence. """
		JSD = 0.0
		weight = 0.5
		average = zeros(len(p)) #Average
		for x in range(len(p)):
			average[x] = weight * p[x] + (1 - weight) * q[x]
			JSD = (weight * KL_divergence(array(p), average)) + ((1 - weight) * KL_divergence(array(q), average))
		return 1-(JSD/sqrt(2 * log(2)))

model=joblib.load('cache/model.pkl')
dialogue=joblib.load('cache/movie.dict')

dictionary = corpora.Dictionary(dialogue.values())

result={}
keys=map(str,sorted(map(int,dialogue.keys())))
inputStuff={}
for val in keys:
	topic=model[dictionary.doc2bow(dialogue[val])]
	temp=[]
	key, value=zip(*topic)
	for i in range(0,149):
		if i in key:
			temp.append(value[key.index(i)])
		else:
			temp.append(0.0)
	inputStuff[val]=temp
for i in range(len(keys)):
	for j in range(i+1,len(keys)):
		result[str(keys[i])+'|'+str(keys[j])]=Jensen_Shannon_divergence(inputStuff[keys[i]],inputStuff[keys[j]])
joblib.dump(result,'cache/JSD.pkl')