from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"

db = SQLAlchemy(app)

class TODO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    done = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

@app.route("/todos", methods=["GET"])
def get_todos():
    todos = TODO.query.all()
    return jsonify([{"id": t.id, "text": t.text, "done": t.done} for t in todos])

@app.route("/todos", methods=["POST"])
def add_todos():
    data = request.json
    new_todo = TODO(text=data["text"])

    db.session.add(new_todo)
    db.session.commit()

    return jsonify({"id": new_todo.id, "text": new_todo.text, "done": new_todo.done}), 201

@app.route("/todos/<id>", methods=["PUT"])
def get_specific_todo(id):
    data = request.json
    todo = TODO.query.get(id)

    if "text" in data:
        todo.text = data["text"]
    if "done" in data:
        todo.done = data["done"]

    db.session.commit()

    return jsonify({"id": todo.id, "text": todo.text , "done": todo.done})

@app.route("/todos/<id>", methods=["DELETE"])
def delete_todo(id):
    todo = TODO.query.get(id)

    db.session.delete(todo)
    db.session.commit()

    return jsonify({"message": "Todo deleted"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)