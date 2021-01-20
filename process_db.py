#Import packages
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
from ast import literal_eval

path1 = ('./static/tmdb_5000_movies.csv')
path2 = ('./static/tmdb_5000_credits.csv')

df_data = pd.read_csv(path1,error_bad_lines=False)
df_credits = pd.read_csv(path2,error_bad_lines=False)

df_data_drop = df_data.drop(columns=['homepage','original_language','production_countries','spoken_languages','status','production_companies'],axis=1)

def cast_columns_2(x):
    #Function to create dataframe cols based on the cast list
    cast = x['cast']
    crew = x['crew']
    eval_cast = literal_eval(cast) #Convert to list of dicts of cast
    eval_crew = literal_eval(crew) #Conver to list of dicts of crew
    x['cast'] = pd.Series(eval_cast[:])
    for i in x['cast']: #ugly but works
        if i['order'] == 0:
            x['cast1'] = i['name']
            x['cast1'] = x['cast1'].replace(" ","")
        if i['order'] == 1:
            x['cast2'] = i['name']
            x['cast2'] = x['cast2'].replace(" ","")
        if i['order'] == 2:
            x['cast3'] = i['name']
            x['cast3'] = x['cast3'].replace(" ","")
    x['director'] = pd.Series(eval_crew[:])
    for i in x['director']:
        if i['job'] == 'Director':
           x['director'] = i['name']
           x['director'] = x['director'].replace(" ","")
    return x

df_credits = df_credits.apply(cast_columns_2,axis=1)
df_credits = df_credits.drop(columns=['cast','crew','title'], axis=1)

def keyword_and_genre_cols(x):
    #Function to create genre and feelings columns on our original df
    keywords = x['keywords']
    genres = x['genres']
    eval_keys = literal_eval(keywords) #Convert to list of dicts of cast
    eval_genres = literal_eval(genres) #Conver to list of dicts of crew
    x['keywords'] = pd.Series(eval_keys[:])
    x['keywords'] = [i['name'] for i in x['keywords']]
    x['genres'] = pd.Series(eval_genres[:])
    x['genres'] = [i['name'] for i in x['genres']]
    return x

df_drop = df_data_drop.apply(keyword_and_genre_cols, axis=1)
df_drop = df_drop.rename(columns={"id":"movie_id"})

df_merge = df_drop.merge(df_credits, on=['movie_id'])
df_merge = df_merge.drop(columns=['original_title'],axis=1)

df_merge['release_date'] = pd.to_datetime(df_merge['release_date'])

#Fill values before delivering
df_merge['overview'] = df_merge['overview'].fillna("")
df_merge['keywords'] = [" ".join(map(str,l)) for l in df_merge['keywords']]
df_merge['genres'] = [" ".join(map(str,l)) for l in df_merge['genres']]
df_merge['cast_all'] = df_merge.apply(lambda row: str(row.cast1) + " " + str(row.cast2) + " " + str(row.cast3), axis=1)
df_merge['soup'] = df_merge.apply(lambda row: str(row.cast_all).lower() + " " + str(row.genres).lower() + " " + str(row.keywords).lower(), axis=1)

df_merge.to_csv("processed.csv")