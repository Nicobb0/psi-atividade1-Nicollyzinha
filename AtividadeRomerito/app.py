from flask import Flask, render_template
import models

app = Flask(__name__)
app.secret_key = "romerito" 

@app.route("/")
def index():
  livros = models.buscar_livros()
  return render_template("index.html", livros=livros)


@app.route("/livro/<int:livro_id>")
def detalhe_livro(livro_id):
  livro = models.buscar_livro(livro_id)

  if livro is None:
    return "Livro não encontrado", 404

  resenhas = models.resenhas_do_livro(livro_id)
  return render_template("livro.html", livro=livro, resenhas=resenhas)
