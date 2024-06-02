from flask import Flask
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
url = "https://www.pensador.com/frases_de_motivacao/"

@app.route("/api/<page>")
def api(page):
    frases = []
    req = requests.get(url=f"{url}{page}")

    if req.status_code == 200:
        soup = BeautifulSoup(req.content,"html.parser")
        p_frase = soup.find_all("p","frase")
        span_autor = soup.find_all("span","author-name")

        for frase,autor in zip(p_frase,span_autor):
            frases.append({
                "frase": frase.text,
                "autor": autor.text
            })

        return frases
    else:
        return {"status: 400"}

if __name__ == "__main__":
    app.run(debug=True)
