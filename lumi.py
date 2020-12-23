#Import packages
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
from ast import literal_eval

#Machine Learning libraries
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

path1 = ('../files/tmdb_5000_movies.csv')
path2 = ('../files/tmdb_5000_credits.csv')

df = pd.read_csv(path1)