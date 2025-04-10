from flask import Flask, render_template
import requests
import random

app = Flask(__name__)

OMDB_API_KEY = "942b65ae"

def fetch_top_100_movies():
    movies = []
    for page in range(1, 6):  # Fetch movies from pages 1 to 5 (50 movies max)
        url = f"http://www.omdbapi.com/?s=movie&apikey={OMDB_API_KEY}&type=movie&page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            break

        data = response.json()
        if "Search" not in data:
            break

        # Add movies from the current page to the list
        movies.extend([{
            "title": movie["Title"],
            "poster": movie["Poster"],
            "year": movie["Year"],
            "imdb_id": movie["imdbID"]
        } for movie in data["Search"]])

    return movies

@app.route("/", methods=["GET"])
def home():
    movies = fetch_top_100_movies()
    if not movies:
        return "<h1>Failed to fetch movie data. Please try again later.</h1>"
    
    # Select 3 random movies
    selected_movies = random.sample(movies, 3)

    # Fetch additional details for each selected movie
    for movie in selected_movies:
        url = f"http://www.omdbapi.com/?i={movie['imdb_id']}&apikey={OMDB_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            movie["rating"] = data.get("imdbRating", "N/A")
            movie["genres"] = data.get("Genre", "N/A")

    return render_template("index.html", movies=selected_movies)

if __name__ == "__main__":
    app.run(debug=True)