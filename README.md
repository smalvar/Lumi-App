# [Lumi-App](https://lumi-app.herokuapp.com/)

## Movie recommendation system app!

Remember when you decided you were gonna watch a movie, like, all those years ago, and now you have a small daughter named 
Ashley going to med school and you're just trying to fix the relationship with her because you've been absent all those years? <br>

Well, **fear no more!** <br>

For all the indecisive movie-choosers in the world, I bring you **Lumi App!** <br>

## How does it work?

By using Kaggle's **The Movie Dataset**, with over 5000 titles from the XXth century until 2019's titles, I was able to create columns with important parameters such as actors (the 3 top casted), director's name, genre and keywords, and then vectorize them using Scikit's CountVectorizer to then apply a Cosine Similarity and filter by proximity. <br>

The user then write's the title's name of the movie he wishes to get recommendation to similarity and the app returns a list of 5 titles. <br>

## Shoutout
*@inboxpraveen* who first posted this project on GitHub and Medium and served as inspiration and *@saramalvar* for being the tutor during the development.

## Current State of Development
The current state of development is improving the front-end and trying out different approaches to improve the recommendation since it isn't perfect yet <br>

Also some refactoring on the code is due and perhaps methodology testing. On previous versions I also used TfidfVectorizer, but the results weren't as good.

## In-Between

I used Pandas to filter out outliers and clean the data.
