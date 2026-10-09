from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///secretaria.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)



class Pedido(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nome_aluno = db.Column(db.String(150), nullable=False)
  dt_nascimento = db.Column(db.String(10), nullable=True)  
  nome_mae = db.Column(db.String(150), nullable=True)
  nome_pai = db.Column(db.String(150), nullable=True)
  nr_tel_celular = db.Column(db.String(15), nullable=True)
  conclusao = db.Column(db.String(15), nullable=False)
  date_added = db.Column(db.DateTime, default=datetime.utcnow)
  descricao = db.Column(db.String(240), nullable=False)
  
  owner = db.Column(db.String(100), nullable=False)

  
  status = db.Column(db.String(20), default="pendente")

 
  entries = db.relationship(
      "Entry", backref="pedido", lazy=True, cascade="all, delete-orphan"
  )

  def to_dict(self):
    return {
        "id": self.id,
        "nome_aluno": self.nome_aluno,
        "dt_nascimento": self.dt_nascimento,
        "nome_mae": self.nome_mae,
        "nome_pai": self.nome_pai,
        "nr_tel_celular": self.nr_tel_celular,
        "conclusao": self.conclusao,
        "date_added": self.date_added.strftime("%Y-%m-%d %H:%M:%S"),
        "descricao": self.descricao,
        "owner": self.owner,
        "status": self.status,
    }


class Entry(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  pedido_id = db.Column(
      db.Integer, db.ForeignKey("pedido.id"), nullable=False
  )
  text = db.Column(db.Text, nullable=False)
  date_added = db.Column(db.DateTime, default=datetime.utcnow)
  arquivo = db.Column(db.String(255), nullable=True) 
  author = db.Column(db.String(100), nullable=False)

  def to_dict(self):
    return {
        "id": self.id,
        "pedido_id": self.pedido_id,
        "text": self.text,
        "date_added": self.date_added.strftime("%Y-%m-%d %H:%M:%S"),
        "arquivo": self.arquivo,
        "author": self.author,
    }





@app.route("/")
def home():
  return jsonify(
      {"message": "API do Sistema de Solicitacao de Documentos - Secretaria"}
  )



@app.route("/api/pedidos", methods=["GET", "POST"])
def gerenciar_pedidos():
  if request.method == "GET":
    pedidos = Pedido.query.all()
    return jsonify([p.to_dict() for p in pedidos])

  if request.method == "POST":
    dados = request.json
    novo_pedido = Pedido(
        nome_aluno=dados.get("nome_aluno"),
        dt_nascimento=dados.get("dt_nascimento"),
        nome_mae=dados.get("nome_mae"),
        nome_pai=dados.get("nome_pai"),
        nr_tel_celular=dados.get("nr_tel_celular"),
        conclusao=dados.get("conclusao"),
        descricao=dados.get("descricao"),
        owner=dados.get("owner", "aluno_padrao"),
        status="pendente",
    )
    db.session.add(novo_pedido)
    db.session.commit()
    return jsonify(novo_pedido.to_dict()), 201



if __name__ == "__main__":
  with app.app_context():
    db.create_all()  
  app.run(debug=True)