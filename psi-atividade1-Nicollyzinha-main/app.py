from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
import models

app = Flask(__name__)
app.secret_key = "Nicolly" 

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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nome = request.form.get("nome")
        senha = request.form.get("senha")

        user = None
        for usuario in models.usuarios:
            if usuario.get("nome") == nome:
                user = usuario
                break

        if user and user.get("senha") == senha:
            session["user"] = user["nome"]
            session["id"] = user["id"]
            return redirect(url_for("list")) 
        else:
            flash("Nome ou senha incorreta")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("id", None)
    session.pop("carrinho", None)
    flash("Você saiu da sua conta com sucesso!")
    return redirect(url_for("login"))


@app.route("/list")
def list():
    usuarios = models.usuarios
    return render_template("list.html", usuarios=usuarios)