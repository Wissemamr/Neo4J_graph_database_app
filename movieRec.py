import streamlit as st
from neo4j import GraphDatabase

# Neo4j connection setup
uri = "bolt://localhost:7687"  # Default Neo4j URI
username = "neo4j"
password = "12345678"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Function to fetch movies by title
def fetch_movies_by_title(search_query):
    query = """
    MATCH (movie:Movie)
    WHERE movie.title CONTAINS $search_query OR $search_query = ''
    OPTIONAL MATCH (movie)-[:FEATURES]->(actor:Actor)
    OPTIONAL MATCH (movie)-[:DIRECTED_BY]->(director:Director)
    RETURN movie.title AS title, movie.year AS year, COLLECT(DISTINCT actor.name) AS actors,
           COLLECT(DISTINCT director.name) AS directors
    """
    with driver.session() as session:
        results = session.run(query, search_query=search_query)
        return [
            {
                "title": record["title"],
                "year": record["year"],
                "actors": record["actors"],
                "directors": record["directors"]
            }
            for record in results
        ]

# Function to fetch recommendations
def get_recommended_movies(movie_title):
    query = """
    MATCH (movie1:Movie {title: $movie_title})
MATCH (movie2:Movie)
WHERE movie1 <> movie2
WITH movie1, movie2, 
    CASE WHEN movie1.genre = movie2.genre THEN 1 ELSE 0 END AS genre_match,
    CASE WHEN abs(movie1.year - movie2.year) <= 5 THEN 1 ELSE 0 END AS year_proximity
OPTIONAL MATCH (movie1)-[:FEATURES]->(actor:Actor)<-[:FEATURES]-(movie2)
WITH movie1, movie2, genre_match, year_proximity, COUNT(DISTINCT actor) AS shared_actors
OPTIONAL MATCH (movie1)-[:DIRECTED_BY]->(director:Director)<-[:DIRECTED_BY]-(movie2)
WITH movie1, movie2, genre_match, year_proximity, shared_actors, COUNT(DISTINCT director) AS shared_directors
WITH movie1, movie2, 
    (shared_actors * 0.2 + 
     shared_directors * 0.3 + 
     genre_match * 0.4 + 
     year_proximity * 0.1) AS similarity_score
RETURN movie2.title AS RecommendedMovie, 
       similarity_score, 
       movie2.genre AS genre, 
       movie2.year AS year
ORDER BY similarity_score DESC
LIMIT 5
    """
    with driver.session() as session:
        results = session.run(query, movie_title=movie_title)
        return [
            {"title": record["RecommendedMovie"], "score": record["similarity_score"]}
            for record in results
        ]
def get_random_movie():
    query = """
    MATCH (movie:Movie)
    WITH movie, rand() AS random_order
    ORDER BY random_order
    LIMIT 1
    OPTIONAL MATCH (movie)-[:FEATURES]->(actor:Actor)
    OPTIONAL MATCH (movie)-[:DIRECTED_BY]->(director:Director)
    RETURN movie.title AS title, movie.year AS year,
           COLLECT(DISTINCT actor.name) AS actors,
           COLLECT(DISTINCT director.name) AS directors
    """
    with driver.session() as session:
        result = session.run(query)
        record = result.single()
        if record:
            return {
                "title": record["title"],
                "year": record["year"],
                "actors": record["actors"],
                "directors": record["directors"],
            }
        return None


# Custom CSS styling
def set_custom_css():
    st.markdown(
        """
        <style>
        body {
            background-color: #141414;
            color: #ffffff;
        }
        .stApp {
            background-color: #141414;
        }
        h1, h2, h3, h4 {
            color: #e50914;
        }
        .stTextInput > div > div > input, .stSelectbox > div > div > div > div > div {
            background-color: #333333;
            color: white;
        }
        .stButton > button {
            background-color: #e50914;
            color: white;
        }
        .stButton > button:hover {
            background-color: #f40612;
        }
        .movie-card {
            background-color: #1c1c1c;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Apply CSS
set_custom_css()

# Header
st.markdown(
    """
    <h1 style="text-align: center;">🎬 Movie Recommendation System </h1>
    <p style="text-align: center; color: #e50914;">Explore movies and get personalized recommendations.</p>
    """,
    unsafe_allow_html=True,
)

# Search box
search_query = st.text_input("🔍 Search for a Movie by Title:")

# Search functionality
if search_query:
    searched_movies = fetch_movies_by_title(search_query)
    if searched_movies:
        # Display searched movies
        for movie in searched_movies:
            st.markdown(
                f"""
            <div class="movie-card">
                <h2>{movie['title']} ({movie['year']})</h2>
                <p><strong>Actors:</strong> {', '.join(movie['actors']) if movie['actors'] else 'No actors found'}</p>
                <p><strong>Director:</strong> {', '.join(movie['directors']) if movie['directors'] else 'No directors found'}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
            
            # Fetch and display recommendations for each movie
            try:
                recommended_movies = get_recommended_movies(movie["title"])
                if recommended_movies:
                    st.markdown(f"### 🎥 Recommendations for {movie['title']}:")
                    for rec in recommended_movies:
                        st.markdown(
                            f"""
                            <div class="movie-card">
                                <h3>{rec['title']}</h3>
                              <!--  <p><strong>Similarity Score:</strong> {rec['score']:.2f}</p>-->
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                else:
                    st.warning(f"No recommendations found for {movie['title']}")
            except Exception as e:
                st.error(f"Error fetching recommendations: {e}")
    else:
        st.error("No movies found.")

# Surprise Me button
if st.button("🎲 Surprise Me!"):
    random_movie = get_random_movie()  # Call the new function
    if random_movie:
        st.markdown(
            f"""
            <div class="movie-card">
                <h2>{random_movie['title']} ({random_movie['year']})</h2>
                <p><strong>Actors:</strong> {', '.join(random_movie['actors']) if random_movie['actors'] else 'No actors found'}</p>
                <p><strong>Directors:</strong> {', '.join(random_movie['directors']) if random_movie['directors'] else 'No directors found'}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error("Could not find any movies. Please try again.")
