from flask import Flask
from bs4 import BeautifulSoup
import httpx


app = Flask(__name__)
URL = "https://www.pensador.com/"


@app.route("/api/")
@app.route("/api/<query>/")
@app.route("/api/<query>/<int:page>/")
def api(query: str = "", page: int = 1) -> str:

    phrases = []
    if query == "":
        return {"message": "provide an author name or keyword"}, 400
    if page > 1:
        response = httpx.get(url=f"{URL}{query}/{page}/")
    else:
        response = httpx.get(url=f"{URL}{query}/")

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        p_phrase = soup.find_all("p", "frase")
        span_author = soup.find_all("span", "author-name")

        for phrase, author in zip(p_phrase, span_author):
            phrases.append({
                "phrase": phrase.text,
                "author": author.text
            })

        return phrases
    else:
        return {"status": response.status_code}


if __name__ == "__main__":
    app.run(debug=True)
