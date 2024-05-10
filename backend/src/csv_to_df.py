import pandas as pd


def init_db():
    books = pd.read_csv('data/BX-Book-Ratings.csv',
                        encoding='latin-1', sep=';')
    ratings = pd.read_csv('data/BX-Book-Ratings.csv',
                          encoding='latin-1', sep=';')
    books_data = books.merge(ratings, on="ISBN")

    df = books_data.copy()
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.drop(columns=["ISBN", "Year-Of-Publication", "Image-URL-S", "Image-URL-M"], axis=1, inplace=True)
    df.drop(index=df[df["Book-Rating"] == 0].index, inplace=True)
    df.to_csv('data/out.csv')
