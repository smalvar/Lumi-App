#standard packages
import pandas as pd
import json
from ast import literal_eval
import os

#Machine Learning libraries
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

#flask
import flask
from flask import render_template, Flask

#Create the Flask app
app = Flask(__name__, template_folder='templates')

#Find the dataframes
df_vector = pd.read_csv("./files/processed.csv",error_bad_lines=False)

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
    app.run()