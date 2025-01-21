# Importing Libraries
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix

ratings = pd.read_csv("home/diin/HocKi_6/He_ra_quyet_dinh/dataMovie/ratings.csv")
movies = pd.read_csv("home/diin/HocKi_6/He_ra_quyet_dinh/dataMovie/movies.csv")

#Matrix using scipy csr matrix
def create_matrix(df):
    N = len(df['userId'].unique())
    M = len(df['movieId'].unique())
    # Map Ids to indices
    user_mapper = dict(zip(np.unique(df["userId"]), list(range(N))))
    movie_mapper = dict(zip(np.unique(df["movieId"]), list(range(M))))
    # Map indices to IDs
    user_inv_mapper = dict(zip(list(range(N)), np.unique(df["userId"])))
    movie_inv_mapper = dict(zip(list(range(M)), np.unique(df["movieId"])))
    user_index = [user_mapper[i] for i in df['userId']]
    movie_index = [movie_mapper[i] for i in df['movieId']]
    X = csr_matrix((df["rating"], (movie_index, user_index)), shape=(M, N))
    return X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper

def find_similar_movies(movie_id, X, k, metric='cosine', show_distance=False):
    neighbour_ids = []

    movie_ind = movie_mapper[movie_id]
    movie_vec = X[movie_ind]
    k += 1
    kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
    kNN.fit(X)
    movie_vec = movie_vec.reshape(1, -1)
    neighbour = kNN.kneighbors(movie_vec, return_distance=show_distance)
    for i in range(0, k):
        n = neighbour.item(i)
        neighbour_ids.append(movie_inv_mapper[n])
    neighbour_ids.pop(0)
    return neighbour_ids

def similar_ids_movie(movie_id):
    movie_titles = dict(zip(movies['movieId'], movies['title']))
    similar_ids = find_similar_movies(movie_id, X, k=5)
    movie_title = movie_titles[movie_id]
    print(f"Bạn đã xem {movie_title}")
    for i in similar_ids:
        print(movie_titles[i])
def recommend_movies_for_user(user_id, X, user_mapper, movie_mapper, movie_inv_mapper, k=10):
    df1 = ratings[ratings['userId'] == user_id]

    if df1.empty:
        print(f"Người dùng với ID{user_id} Không tồn tại.")
        return

    movie_id = df1[df1['rating'] == max(df1['rating'])]['movieId'].iloc[0]

    movie_titles = dict(zip(movies['movieId'], movies['title']))

    similar_ids = find_similar_movies(movie_id, X, k)
    movie_title = movie_titles.get(movie_id, "Bộ phim không tìm thấy.")

    if movie_title == "Bộ phim không tìm thấy.":
        print(f"Bộ phim với ID {movie_id} không tìm thấy.")
        return

    print(f"Bạn đã xem {movie_title}, Có thể bạn sẽ thích:")
    for i in similar_ids:
        print(movie_titles.get(i, "Bộ phim không tìm thấy."))

if __name__ == '__main__':
    X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper = create_matrix(ratings)
    movie_id = int(input("Nhập ID bộ phim cần tìm: "))
    similar_ids_movie(movie_id)
    user_id = int(input("Nhập ID người dùng: "))
    recommend_movies_for_user(user_id, X, user_mapper, movie_mapper, movie_inv_mapper, k=5)