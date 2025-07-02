# AI Movie Recommend System

A visually stunning AI-powered movie recommendation web app built with Streamlit. Enter a movie you like and get intelligent recommendations with posters, genres, cast, director, and more!

## Features

- Search for any movie in the dataset
- Get top-N similar movie recommendations
- See movie posters, genres, cast, director, ratings, and overview
- Beautiful, modern UI with custom CSS
- Uses TF-IDF and cosine similarity for recommendations
- Fetches posters from TMDb API

## Setup

1. **Clone the repository**

    ```sh
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2. **Install dependencies**

    ```sh
    pip install -r requirements.txt
    ```

3. **Download the dataset**

    Place your `movies.csv` file in the `data/` directory. The CSV should have columns: `id`, `title`, `genres`, `overview`, `keywords`, `cast`, `director`, `vote_average`, `vote_count`.

4. **Set TMDb API Key**

    The API key is set in [`app.py`](app.py) as `TMDB_API_KEY`. Replace it with your own TMDb API key if needed.

5. **Run the app**

    ```sh
    streamlit run app.py
    ```

6. **Open in your browser**

    Visit [http://localhost:8501](http://localhost:8501) to use the app.

## File Structure

- [`app.py`](app.py): Main Streamlit app
- [`data/movies.csv`](data/movies.csv): Movie dataset (not included)
- [`requirements.txt`](requirements.txt): Python dependencies

## Example
![Screenshot 2025-06-30 221623](https://github.com/user-attachments/assets/15b79e00-22f8-4539-9959-25bab99e169b)
![Screenshot 2025-06-30 221529](https://github.com/user-attachments/assets/1568594f-6c1c-4ff8-9c7e-70cfe4f6decc)



**Enjoy discovering your next
