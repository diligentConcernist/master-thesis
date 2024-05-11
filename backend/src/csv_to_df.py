import pandas as pd

BOOK_TITLE = "book_title"
BOOK_RATING = "book_rating"
NUMBER_OF_VOTES = "number_of_votes"
AVERAGE_RATINGS = "average_ratings"
POPULARITY = "popularity"
IMAGE_URL = "image_url"
BOOK_AUTHOR = "book_author"


def init_raw_data():
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
    df = df.rename(columns={"ISBN": "isbn",
                            "Book-Title": BOOK_TITLE,
                            "Book-Author": BOOK_AUTHOR,
                            "Publisher": "publisher",
                            "Image-URL-L": IMAGE_URL,
                            "Year-Of-Publication": "year_of_publication",
                            "User-ID": "user_id",
                            "Book-Rating": BOOK_RATING
                            })
    df.to_csv('data/out.csv')


def popular_books(df):
    rating_count = df.groupby(BOOK_TITLE).count()[BOOK_RATING].reset_index()
    rating_count.rename(columns={BOOK_RATING: NUMBER_OF_VOTES}, inplace=True)

    rating_average = df.groupby(BOOK_TITLE)[BOOK_RATING].mean().reset_index()
    rating_average.rename(columns={BOOK_RATING: AVERAGE_RATINGS}, inplace=True)

    image_urls = df.groupby(BOOK_TITLE)[IMAGE_URL].apply(list).str[0].reset_index()

    popularBooks = rating_count.merge(rating_average, on=BOOK_TITLE)
    popularBooks = popularBooks.merge(image_urls, on=BOOK_TITLE)

    def weighted_rate(x):
        v = x[NUMBER_OF_VOTES]
        R = x[AVERAGE_RATINGS]

        return ((v * R) + (m * C)) / (v + m)

    C = popularBooks[AVERAGE_RATINGS].mean()
    m = popularBooks[NUMBER_OF_VOTES].quantile(0.90)

    popularBooks = popularBooks[popularBooks[NUMBER_OF_VOTES] >= 250]
    popularBooks[POPULARITY] = popularBooks.apply(weighted_rate, axis=1)
    popularBooks = popularBooks.sort_values(by=POPULARITY, ascending=False)
    popularBooks = popularBooks[[BOOK_TITLE, NUMBER_OF_VOTES, AVERAGE_RATINGS, POPULARITY]].reset_index(drop=True)

    popularBooks.to_csv('data/popular_books.csv')


def get_books_with_average_rating(df):
    rating_count = df.groupby(BOOK_TITLE).count()[BOOK_RATING].reset_index()
    rating_count.rename(columns={BOOK_RATING: NUMBER_OF_VOTES}, inplace=True)

    rating_average = df.groupby(BOOK_TITLE)[BOOK_RATING].mean().reset_index()
    rating_average.rename(columns={BOOK_RATING: AVERAGE_RATINGS}, inplace=True)

    image_urls = df.groupby(BOOK_TITLE)["image_url"].apply(list).str[0].reset_index()

    book_authors = df.groupby(BOOK_TITLE)[BOOK_AUTHOR].apply(list).str[0].reset_index()

    books_with_rating = rating_count.merge(rating_average, on=BOOK_TITLE)
    books_with_rating = books_with_rating.merge(image_urls, on=BOOK_TITLE)
    books_with_rating = books_with_rating.merge(book_authors, on=BOOK_TITLE)

    def weighted_rate(x):
        v = x[NUMBER_OF_VOTES]
        R = x[AVERAGE_RATINGS]

        return ((v * R) + (m * C)) / (v + m)

    C = books_with_rating[AVERAGE_RATINGS].mean()
    m = books_with_rating[NUMBER_OF_VOTES].quantile(0.90)

    books_with_rating[POPULARITY] = books_with_rating.apply(weighted_rate, axis=1)
    books_with_rating = books_with_rating.sort_values(by=POPULARITY, ascending=False)

    books_with_rating.to_csv('data/rated_books.csv')
