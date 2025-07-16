from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [movies.iloc[i[0]].title for i in movie_list]

@app.route('/', methods=['GET', 'POST'])
def index():
    movie_names = movies['title'].values
    selected_movie = None
    recommendations = []

    if request.method == 'POST':
        selected_movie = request.form['movie']
        recommendations = recommend(selected_movie)

    return render_template('index.html',
                           movie_names=movie_names,
                           selected_movie=selected_movie,
                           recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
