from main import app
from flask import render_template, redirect, request, session, url_for
from werkzeug.security import check_password_hash
import sqlite3
from sqlite3 import IntegrityError

@app.route("/criar", methods=["GET", "POST"])
def criacao_de_tarefas():

    if "usuario_id" not in session:
        return redirect("/login")

    usuario_id = session["usuario_id"]

    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        data_criacao = request.form["data_criacao"]
        data_conclusao = request.form["data_conclusao"]
        status = request.form["status"]
        categoria_id = request.form["categoria_id"]

        con = sqlite3.connect("todolist.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO tarefas (titulo, descricao, data_criacao, data_conclusao, status, categoria_id, usuario_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (titulo, descricao, data_criacao, data_conclusao, status, categoria_id, usuario_id))
        con.commit()
        con.close()

        return render_template("criar.html", mensagem="Tarefa criada com sucesso!")


    con = sqlite3.connect("todolist.db")
    cur = con.cursor()
    cur.execute("SELECT id, nome FROM categorias")
    categorias = cur.fetchall()
    con.close()

    return render_template("criar.html", categorias=categorias)

@app.route("/tarefas")
def ver_tarefas_em_lista():
    if "usuario_id" not in session:
        return redirect("/login")

    usuario_id = session["usuario_id"]
    status = request.args.get("status", "")
    busca = request.args.get("busca", "")
    data_criacao = request.args.get("data_criacao", "")
    data_conclusao = request.args.get("data_conclusao", "")
    categoria_id = request.args.get("categoria_id", "")

    con = sqlite3.connect("todolist.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    # 🔹 Carrega todas as categorias (sempre!)
    cur.execute("SELECT id, nome FROM categorias")
    categorias = cur.fetchall()

    query = """
        SELECT 
            tarefas.id,
            tarefas.titulo,
            tarefas.descricao AS descricao_tarefa,
            tarefas.data_criacao,
            tarefas.data_conclusao,
            tarefas.status,
            categorias.nome AS nome_categoria
        FROM tarefas
        LEFT JOIN categorias ON tarefas.categoria_id = categorias.id
        WHERE tarefas.usuario_id = ?
    """

    params = [usuario_id]

    if status:
        query += " AND tarefas.status = ?"
        params.append(status)

    if busca:
        query += " AND (tarefas.titulo LIKE ? OR tarefas.descricao LIKE ?)"
        busca_param = f"%{busca}%"
        params.extend([busca_param, busca_param])

    if data_criacao:
        query += " AND tarefas.data_criacao = ?"
        params.append(data_criacao)
        
    if data_conclusao:
        query += " AND tarefas.data_conclusao = ?"
        params.append(data_conclusao)

    if categoria_id:
        query += " AND tarefas.categoria_id = ?"
        params.append(categoria_id)
    

    query += " ORDER BY tarefas.data_criacao DESC"

    cur.execute(query, params)
    tarefas = cur.fetchall()
    con.close()
    return render_template("tarefas.html", tarefas=tarefas, categorias=categorias, busca=busca, data_conclusao=data_conclusao, categoria_id=categoria_id)

@app.route("/excluir/<int:id>")
def deletar_tarefas_criadas(id):
    con = sqlite3.connect("todolist.db")
    cur = con.cursor()

    if "usuario_id" not in session:
        return render_template("login.html")
    usuario_id = session["usuario_id"]

    cur.execute("DELETE FROM tarefas WHERE id=?",(id,))
    con.commit()
    con.close()

    return redirect("/tarefas")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_tarefas_criadas(id):
    con = sqlite3.connect("todolist.db")
    cur = con.cursor()
    if "usuario_id" not in session:
        return render_template("login.html")
    
    usuario_id = session["usuario_id"]

    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        data_criacao = request.form["data_criacao"]
        data_conclusao = request.form["data_conclusao"]
        status = request.form["status"]
        categoria_id = request.form["categoria_id"]

        cur.execute("UPDATE tarefas SET titulo = ?, descricao = ?, data_criacao = ?, data_conclusao = ?, status = ?, categoria_id = ? WHERE id=?",(titulo, descricao, data_criacao, data_conclusao, status, categoria_id, id))
        con.commit()
        con.close()

        return redirect("/tarefas")
    
    cur.execute("SELECT titulo, descricao, data_criacao, data_conclusao, status, categoria_id FROM tarefas WHERE id = ?", (id,))
    tarefa = cur.fetchone()
    con.close()

    con = sqlite3.connect("todolist.db")
    cur = con.cursor()
    cur.execute("SELECT id, nome FROM categorias")
    categorias = cur.fetchall()
    con.close()


    return render_template("editar.html", tarefa=tarefa, id=id, categorias=categorias)

@app.route("/concluir/<int:id>")
def concluir_tarefa(id):  
    con = sqlite3.connect("todolist.db")
    cur = con.cursor()

    if "usuario_id" not in session:
        return render_template("login.html")
    
    usuario_id = session["usuario_id"]

    # Atualiza o status da tarefa para "Concluída"
    cur.execute("UPDATE tarefas SET status = 'concluida' WHERE id=? AND usuario_id=?", (id, usuario_id))
    con.commit()
    con.close()

    return redirect("/tarefas")
