from flask import Flask, render_template, request
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/novoaluno", methods=["POST"])
def inserir_aluno():
    ra = request.form['ra']
    nome = request.form['nome']
    tempoestudo = request.form['tempoestudo']
    rendafamiliar = request.form['rendafamiliar']
    
    return render_template("index.html", ra=ra)

if __name__ == "__main__":
    app.run(debug=True)

