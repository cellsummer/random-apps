from os import replace
import requests


class Movies:
    def __init__(self, type_id) -> None:
        LOAD_LIMIT = 30
        self.type_id = type_id
        self.end_point = f"https://movie.douban.com/j/chart/top_list?type={type_id}&interval_id=100%3A90&action=&start=0&limit={LOAD_LIMIT}"
        # print(self.end_point)

    def get_movies(self):
        headers = {
            "User-Agent": "M",
        }
        doc = requests.get(self.end_point, headers=headers).text
        doc = doc.replace("true", "True")
        doc = doc.replace("false", "False")
        # movies = doc.json()
        # print(doc)
        # print(doc.text)
        # movies = eval(doc)
        # print(movies)
        movies = eval(doc)
        # movies["cover_url"] = movies["cover_url"].replace("\\", "/")
        # print(movies[0]["cover_url"])
        return movies


if __name__ == "__main__":
    movies = Movies(3).get_movies()
    for movie in movies:
        print(movie["title"])
        print(movie["release_date"])
        print(movie["score"])
        movie["cover_url"] = movie["cover_url"].replace("\\", "/")
        print(movie["cover_url"])
