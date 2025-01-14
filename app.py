from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "chave_secreta_para_sessoes"

# Lista de cafeterias com nomes e imagens
cafeterias = [
    {"name": "Torra Café", "image": "/static/Torra.jpg"},
    {"name": "Greta Café", "image": "/static/Greta.jpg"},
    {"name": "Padoca", "image": "/static/Padoca.png"},
    {"name": "Le Pain Le Cafe", "image": "/static/Lepain.jpg"},
    {"name": "Benévolo Café", "image": "/static/Benevolo.jpg"},
    {"name": "Matina Café", "image": "/static/Matina.png"},
    {"name": "Casa Pâine", "image": "/static/Paine.jpg"},
    {"name": "Acclamé Café", "image": "/static/Acclame.jpg"},
]

@app.route("/")
def index():
    session["cafeterias"] = cafeterias.copy()  # Reinicia a lista de cafeterias
    random.shuffle(session["cafeterias"])  # Embaralha a lista de cafeterias
    session["current_champion"] = None  # Reseta o campeão
    return render_template("index.html")

@app.route("/battle", methods=["GET", "POST"])
def battle():
    if request.method == "POST":
        winner_name = request.form.get("winner")

        # Se não houver vencedor informado, redireciona ao início
        if not winner_name:
            return redirect(url_for("index"))

        # Recupera o par atual de batalha
        current_pair = session.get("current_pair")
        if not current_pair:
            return redirect(url_for("index"))

        # Define o campeão como a cafeteria vencedora
        winner = next((caf for caf in current_pair if caf["name"] == winner_name), None)
        if not winner:
            return redirect(url_for("index"))

        session["current_champion"] = winner

        # Remove o desafiante derrotado da lista
        session["cafeterias"] = [caf for caf in session["cafeterias"] if caf["name"] != winner_name]

        # Se não houver mais cafeterias para desafiar, o campeão é o vencedor final
        if session["current_champion"] and not session["cafeterias"]:
            return redirect(url_for("winner", winner_name=session["current_champion"]["name"]))

    # Seleciona o campeão atual ou define o primeiro café como campeão
    if session["current_champion"] is None:
        if session["cafeterias"]:
            champion = session["cafeterias"].pop(0)
            session["current_champion"] = champion  # Define o primeiro campeão
        else:
            return redirect(url_for("index"))

    else:
        champion = session["current_champion"]

    # Se não houver mais desafiante, o campeão vence
    if not session["cafeterias"]:
        return redirect(url_for("winner", winner_name=champion["name"]))

    # Seleciona um desafiante aleatório
    challenger = random.choice(session["cafeterias"])
    session["cafeterias"].remove(challenger)  # Remove o desafiante selecionado para evitar repetição
    session["current_pair"] = [champion, challenger]

    return render_template("battle.html", cafeteria1=champion, cafeteria2=challenger)

@app.route("/winner/<winner_name>")
def winner(winner_name):
    return render_template("winner.html", winner_name=winner_name)

if __name__ == "__main__":
    app.run(debug=True)
