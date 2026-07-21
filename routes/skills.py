from flask import Blueprint, render_template

skills = Blueprint("skills", __name__)


@skills.route("/skills")
def view_skills():
    return render_template("skills.html")


@skills.route("/skills/add")
def add_skill():
    return render_template("add_skill.html")


@skills.route("/skills/edit/<int:id>")
def edit_skill(id):
    return f"Edit Skill ID: {id}"


@skills.route("/skills/delete/<int:id>")
def delete_skill(id):
    return f"Delete Skill ID: {id}"