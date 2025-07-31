from main import app
from flask import render_template, redirect, request, session, url_for
from werkzeug.security import check_password_hash
import sqlite3
from sqlite3 import IntegrityError
from tarefascrud import *

app = app

@app.route("/")
def homepage():
    if "usuario_id" not in session:
        return redirect("/login")

    return render_template("homepage.html")

@app.route("/login", methods=["GET", "POST"])
def login_de_usuarios():
    if "usuario_id" in session:
        return redirect("/")
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        con = sqlite3.connect("todolist.db")
        cur = con.cursor()

        cur.execute("SELECT id, username FROM usuarios WHERE email = ? AND senha = ?",(email, senha))
        user = cur.fetchone()
        con.close()
        if user:
            session["usuario_id"] = user[0]
            return redirect("/")
        else:
            return "Usuario ou senha Inválidos!"
    return render_template("login.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro_de_usuarios():
    if "usuario_id" in session:
        return redirect("/")
    
    if request.method == "POST":
        nome_completo = request.form["nome_completo"]
        username = request.form["username"]
        email = request.form["email"]
        senha = request.form["senha"]
        telefone = request.form["telefone"]
        data_nascimento = request.form["data_nascimento"]
        como_conheceu = request.form["como_conheceu"]

        con = sqlite3.connect('todolist.db')
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO usuarios (nome_completo, username, email, senha, telefone, data_nascimento, como_conheceu) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (nome_completo, username, email, senha, telefone, data_nascimento, como_conheceu))
            con.commit()
            return redirect("/login")
        except sqlite3.IntegrityError:
            return ("Erro: Usuário já cadastrado ou dados inválidos.")
    
        finally:
          con.close()
    return render_template('cadastro.html')

@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    return redirect('/')