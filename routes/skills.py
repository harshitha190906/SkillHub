from flask import Blueprint, render_template, request, redirect, url_for, session
from models.skill import Skill

skills = Blueprint("skills", __name__)

mysql = None

def init_mysql(db):
    global mysql
    mysql = db


@skills.route("/skills")
def view_skills():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    data = Skill.get_all_skills(mysql, session["user_id"])

    return render_template("skills.html", skills=data)


@skills.route("/skills/add", methods=["GET", "POST"])
def add_skill():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        skill_name = request.form["skill_name"]
        skill_level = request.form["skill_level"]
        description = request.form["description"]

        Skill.add_skill(
            mysql,
            session["user_id"],
            skill_name,
            skill_level,
            description
        )

        return redirect(url_for("skills.view_skills"))

    return render_template("add_skill.html")


@skills.route("/skills/edit/<int:id>", methods=["GET", "POST"])
def edit_skill(id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        skill_name = request.form["skill_name"]
        skill_level = request.form["skill_level"]
        description = request.form["description"]

        Skill.update_skill(
            mysql,
            id,
            skill_name,
            skill_level,
            description
        )

        return redirect(url_for("skills.view_skills"))

    skill = Skill.get_skill_by_id(mysql, id)

    return render_template("edit_skill.html", skill=skill)


@skills.route("/skills/delete/<int:id>")
def delete_skill(id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    Skill.delete_skill(mysql, id)

    return redirect(url_for("skills.view_skills"))