#standard packages
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
from ast import literal_eval
import os

#Machine Learning libraries
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

#flask
import flask
from flask import render_template

#Here we import our dataframes from the file
path1 = os.getcwd()
path1 += "/files/tmdb_5000_movies.csv" #join current path with this files
path2 = os.getcwd()
path2 += "/files/tmdb_5000_credits.csv" #join current path with this files

#Create the Flask app
app = flask.Flask(__name__,)

#Find the dataframes
df_data = pd.read_csv(path1,error_bad_lines=False)
df_credits = pd.read_csv(path2,error_bad_lines=False)

#Drop useless columns from df_data
df_data_drop = df_data.drop(columns=['homepage','original_language','production_countries','spoken_languages','status','production_companies'],axis=1)

#Create own function to create dataframe with the 
#artists name the way we can use them to vectorize
def cast_columns_2(x):
    #Function to create dataframe cols based on the cast list
    cast = x['cast']
    crew = x['crew']
    eval_cast = literal_eval(cast) #Convert to list of dicts of cast
    eval_crew = literal_eval(crew) #Conver to list of dicts of crew
    x['cast'] = pd.Series(eval_cast[:], dtype='object')
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
    x['director'] = pd.Series(eval_crew[:], dtype='object')
    for i in x['director']:
        if i['job'] == 'Director':
           x['director'] = i['name']
           x['director'] = x['director'].replace(" ","")
    return x

#Execute the recently built function
df_credits = df_credits.apply(cast_columns_2,axis=1)
df_credits = df_credits.drop(columns=['cast','crew','title'], axis=1)

#untangle keywords and genres from list of terms to 
#single terms
def keyword_and_genre_cols(x):
    #Function to create genre and feelings columns on our original df
    keywords = x['keywords']
    genres = x['genres']
    eval_keys = literal_eval(keywords) #Convert to list of dicts of cast
    eval_genres = literal_eval(genres) #Conver to list of dicts of crew
    x['keywords'] = pd.Series(eval_keys[:], dtype='object')
    x['keywords'] = [i['name'] for i in x['keywords']]
    x['genres'] = pd.Series(eval_genres[:], dtype='object')
    x['genres'] = [i['name'] for i in x['genres']]
    return x

#Execute the recently built function
df_drop = df_data_drop.apply(keyword_and_genre_cols, axis=1)
df_drop = df_drop.rename(columns={"id":"movie_id"})

#Merge dataframes on movie id
df_merge = df_drop.merge(df_credits, on=['movie_id'])
df_merge = df_merge.drop(columns=['original_title'],axis=1)

#Convert release date to datetime
df_merge['release_date'] = pd.to_datetime(df_merge['release_date'])

#Fill values before delivering file
df_merge['overview'] = df_merge['overview'].fillna("")
df_merge['keywords'] = [" ".join(map(str,l)) for l in df_merge['keywords']]
df_merge['genres'] = [" ".join(map(str,l)) for l in df_merge['genres']]
df_merge['cast_all'] = df_merge.apply(lambda row: str(row.cast1) + " " + str(row.cast2) + " " + str(row.cast3), axis=1)
df_merge['soup'] = df_merge.apply(lambda row: str(row.cast_all).lower() + " " + str(row.genres).lower() + " " + str(row.keywords).lower(), axis=1)

"""
This section is dedicated for the soup vectrizer itself
"""
#So we don't make permanent change to the created dataframe
df_vector = df_merge.copy()

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df_vector['soup'])
cosine_sim = cosine_similarity(count_matrix, count_matrix)

indices = pd.Series(df_vector.index, index=df_vector['title'])
all_titles = [df_vector['title'][i] for i in range(len(df_vector['title']))]
def content_recommender(title, cosine_sim=cosine_sim, df=df_vector, indices=indices):
    #We supply a movie and the function returns a recommendation
    idx = indices[title] #Index of the movie
    sim_scores = list(enumerate(cosine_sim[idx])) #get the pairwise similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[0:20]
    movie_indices = [i[0] for i in sim_scores]
    df = df.iloc[movie_indices]
    df = df.sort_values(['vote_average'], ascending=False)
    return df[['title']].iloc[1:6]

#Set up flask app
@app.route('/', methods=['GET','POST'])
def main():
    if flask.request.method == "GET":
        return flask.render_template('home.html')
    
    if flask.request.method == "POST":
        movie_name = flask.request.form['movie_name']
        movie_name = movie_name.title()
        if movie_name not in all_titles:
            return 'not here'
        else:
            result_final = content_recommender(movie_name)
            names = []
            for i in range(5):
                names.append(result_final.iloc[i][0])
            return flask.render_template('positive.html', movie_names=names, search_name=movie_name)

if __name__ == '__main__':
    app.run(debug=True)