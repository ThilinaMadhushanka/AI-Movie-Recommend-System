import streamlit as st

st.set_page_config(
    page_title="AI Movie Recommend System", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# TMDb API Key 
TMDB_API_KEY = "18d30687ee60c61c7325e8ad3c8dbee9"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Custom CSS for premium UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #e11d48 0%, #fbbf24 50%, #14b8a6 100%);
        min-height: 100vh;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom container */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    /* Hero section */
    .hero-section {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 3rem 2rem;
        margin-bottom: 3rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: shimmer 4s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { transform: rotate(0deg); }
        50% { transform: rotate(180deg); }
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 2;
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 300;
        position: relative;
        z-index: 2;
    }
    
    /* Search section */
    .search-section {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 3rem;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .search-label {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        font-weight: 600;
        color: #4a5568;
        margin-bottom: 1rem;
        display: block;
    }
    
    /* Custom input styling */
    .stTextInput > div > div > input {
        background: linear-gradient(145deg, #f8fafc, #e2e8f0);
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        font-size: 1.1rem;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.06);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        transform: translateY(-1px);
    }
    
    /* Custom button */
    .stButton > button {
        background: linear-gradient(145deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        width: 100%;
        margin-top: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(145deg, #5a67d8, #6b46c1);
    }
    
    /* Movie cards */
    .movie-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    .movie-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 1rem;
        line-height: 1.3;
    }
    
    .movie-poster {
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        max-height: 300px;
        object-fit: cover;
    }
    
    .movie-poster:hover {
        transform: scale(1.05);
    }
    
    .info-tag {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin: 0.25rem 0.5rem 0.25rem 0;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        border: 1px solid transparent;
        transition: all 0.3s ease;
    }
    
    .tag-genres {
        background: linear-gradient(135deg, #ffecd2, #fcb69f);
        color: #8b4513;
        border-color: #fcb69f;
    }
    
    .tag-director {
        background: linear-gradient(135deg, #a8edea, #fed6e3);
        color: #2d3748;
        border-color: #fed6e3;
    }
    
    .tag-cast {
        background: linear-gradient(135deg, #d299c2, #fef9d7);
        color: #4a5568;
        border-color: #fef9d7;
    }
    
    .tag-rating {
        background: linear-gradient(135deg, #89f7fe, #66a6ff);
        color: #1a365d;
        font-weight: 600;
        border-color: #66a6ff;
    }
    
    .movie-overview {
        background: linear-gradient(135deg, #f093fb, #f5576c);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-style: italic;
        line-height: 1.6;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
    }
    
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* Loading animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv("data/movies.csv")
    for col in ['genres', 'overview', 'keywords', 'cast', 'director']:
        df[col] = df[col].fillna('')
    df['combined_features'] = (
        df['genres'] + ' ' +
        df['overview'] + ' ' +
        df['keywords'] + ' ' +
        df['cast'] + ' ' +
        df['director']
    )
    return df

# Get poster using TMDb API
def get_movie_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return IMAGE_BASE_URL + poster_path
    return None

# Recommend similar movies
def recommend_movies(title, n=5):
    idx = title_to_index.get(title)
    if idx is None:
        return pd.DataFrame([{"Error": "Movie not found in dataset."}])
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:n+1]
    movie_indices = [i[0] for i in sim_scores]
    return movies_df.iloc[movie_indices]

# Load & compute similarity
movies_df = load_data()
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies_df['combined_features'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
title_to_index = pd.Series(movies_df.index, index=movies_df['title']).drop_duplicates()

# Main UI
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">🎬 AI Movie Recommend System</h1>
    <p class="hero-subtitle">Discover your next favorite movie with intelligent recommendations</p>
</div>
""", unsafe_allow_html=True)

# Search Section
st.markdown('<label class="search-label">🎭 What movie did you enjoy?</label>', unsafe_allow_html=True)

movie_input = st.text_input(
    "Movie Input", 
    value="", 
    key="movie_input", 
    placeholder="Enter a movie title...",
    help="Type any movie title from our extensive database",
    label_visibility="collapsed"
)

recommend_clicked = st.button("✨ Find Similar Movies")
st.markdown('</div>', unsafe_allow_html=True)

# Results Section
if recommend_clicked:
    if movie_input:
        with st.spinner('🔮 Finding perfect matches...'):
            results_df = recommend_movies(movie_input)
            
        if "Error" in results_df.columns:
            st.error(f"🎬 {results_df['Error'].iloc[0]} Please try another title.")
        else:
            st.markdown('<h2 class="section-title">🌟 Recommended For You</h2>', unsafe_allow_html=True)
            
            for i, (_, row) in enumerate(results_df.iterrows()):
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                
                cols = st.columns([1, 2])
                
                with cols[0]:
                    poster_url = get_movie_poster(row['id'])
                    if poster_url:
                        st.markdown(f'<img src="{poster_url}" class="movie-poster" style="width: 100%;">', unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #667eea, #764ba2); 
                                    height: 300px; border-radius: 12px; display: flex; 
                                    align-items: center; justify-content: center; color: white; 
                                    font-size: 3rem;">🎬</div>
                        """, unsafe_allow_html=True)
                
                with cols[1]:
                    st.markdown(f'<h3 class="movie-title">{row["title"]}</h3>', unsafe_allow_html=True)
                    
                    # Tags
                    if row['genres']:
                        st.markdown(f'<span class="info-tag tag-genres">🎭 {row["genres"]}</span>', unsafe_allow_html=True)
                    
                    if row['director']:
                        st.markdown(f'<span class="info-tag tag-director">🎬 {row["director"]}</span>', unsafe_allow_html=True)
                    
                    if row['cast']:
                        cast_preview = row['cast'][:100] + "..." if len(row['cast']) > 100 else row['cast']
                        st.markdown(f'<span class="info-tag tag-cast">👥 {cast_preview}</span>', unsafe_allow_html=True)
                    
                    # Rating
                    rating = row['vote_average']
                    votes = row['vote_count']
                    st.markdown(f'<span class="info-tag tag-rating">⭐ {rating}/10 ({votes:,} votes)</span>', unsafe_allow_html=True)
                    
                    # Overview
                    if row['overview']:
                        st.markdown(f'<div class="movie-overview">"{row["overview"]}"</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("🎭 Please enter a movie title to get personalized recommendations!")

st.markdown('</div>', unsafe_allow_html=True)