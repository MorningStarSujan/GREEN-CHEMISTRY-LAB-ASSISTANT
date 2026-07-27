from flask import Flask, render_template, request, jsonify
from utils.file_handler import load_json, add_history
from utils.chemical_loader import load_all_chemicals
from models.ai_engine import AIEngine

app = Flask(__name__)
ai = AIEngine()


@app.route("/")
def splash():
    return render_template("splash.html")


@app.route("/dashboard")
def dashboard():

    experiments = load_json("experiments.json")
    chemicals = load_all_chemicals()
    safety = load_json("safety_rules.json")
    history = load_json("history.json")

    return render_template(
        "dashboard.html",
        experiments_count=len(experiments),
        chemicals_count=len(chemicals),
        safety_count=len(safety),
        history_count=len(history),
        recent_history=history[:5],
    )


@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():

    question = ""
    answer = ""

    if request.method == "POST":

        question = request.form.get("question", "").strip()

        if question:
            answer = ai.get_response(question)

    return render_template("chatbot.html", question=question, answer=answer)


@app.route("/ask_ai", methods=["POST"])
def ask_ai():

    question = request.form.get("question", "").strip()

    if not question:
        return jsonify({"answer": "Please enter a question."})

    answer = ai.get_response(question)

    add_history("AI Assistant", f'Asked: "{question}"')

    return jsonify({"answer": answer})


@app.route("/add_history", methods=["POST"])
def add_history_route():

    module = request.form.get("module", "")
    activity = request.form.get("activity", "")

    if module and activity:
        add_history(module, activity)

    return jsonify({"status": "success"})


@app.route("/experiment")
def experiment():

    experiments = load_json("experiments.json")

    return render_template("experiment.html", experiments=experiments)


@app.route("/experiment/<int:experiment_id>")
def experiment_details(experiment_id):

    experiments = load_json("experiments.json")

    selected_experiment = None

    for experiment in experiments:

        if experiment["id"] == experiment_id:
            selected_experiment = experiment
            break

    if selected_experiment:

        add_history("Experiment Guide", f'Viewed: {selected_experiment["name"]}')

    return render_template("experiment_details.html", experiment=selected_experiment)


@app.route("/recommendation")
def recommendation():

    chemicals = load_all_chemicals()

    return render_template("recommendation.html", chemicals=chemicals)


@app.route("/recommendation/<int:index>")
def recommendation_details(index):

    chemicals = load_all_chemicals()

    if index < 0 or index >= len(chemicals):
        return "Chemical not found", 404

    chemical = chemicals[index]

    add_history("Green Recommendations", f'Viewed Recommendation: {chemical["name"]}')

    return render_template("recommendation_details.html", chemical=chemical)


@app.route("/safety")
def safety():

    chemicals = load_all_chemicals()

    return render_template("safety.html", chemicals=chemicals)


@app.route("/safety/<int:index>")
def safety_details(index):

    chemicals = load_all_chemicals()

    if index < 0 or index >= len(chemicals):
        return "Chemical not found", 404

    chemical = chemicals[index]

    add_history("Safety Checker", f'Viewed Safety: {chemical["name"]}')

    return render_template("safety_details.html", chemical=chemical)


@app.route("/calculator")
def calculator():
    return render_template("calculator.html")


@app.route("/history")
def history():

    history_data = load_json("history.json")

    return render_template("history.html", history=history_data)


@app.route("/about")
def about():
    return render_template("about.html")


import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
