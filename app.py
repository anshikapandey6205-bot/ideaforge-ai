from flask import Flask, render_template, request, jsonify
from data.projects import PROJECTS

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_projects():

    data = request.get_json()

    skills = data.get("skills", [])
    interests = data.get("interests", [])
    difficulty = data.get("difficulty", "Any")
    project_type = data.get("project_type", "Any")

    results = []

    for project in PROJECTS:

        score = 0

        # Match skills
        for skill in skills:
            if skill.lower() in [s.lower() for s in project["skills"]]:
                score += 2

        # Match interests
        for interest in interests:
            if interest.lower() in [i.lower() for i in project["interests"]]:
                score += 2

        # Match difficulty
        if difficulty == "Any" or project["difficulty"].lower() == difficulty.lower():
            score += 2

        # Match project type
        if project_type == "Any" or project["type"].lower() == project_type.lower():
            score += 2

        if score > 0:
            project_copy = project.copy()
            project_copy["score"] = score
            results.append(project_copy)

    results.sort(key=lambda x: x["score"], reverse=True)

    return jsonify({
        "success": True,
        "projects": results[:5]
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)