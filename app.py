from flask import Flask, render_template as ren, request, redirect, url_for, flash
import db
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family = font_name)
plt.rcParams['axes.unicode_minus'] = False

app = Flask(__name__)

@app.route("/")
def index():
    score_list = db.get_all_scores()
    return ren("index.html", score_list=score_list)

@app.route("/add_score", methods=["POST"])
def add_score():
    sname = request.form["sname"]
    kor = int(request.form["kor"])
    eng = int(request.form["eng"])
    mat = int(request.form["mat"])
    db.insert_score(sname, kor, eng, mat)
    return redirect(url_for('index'))

# Flask 서버 실행
if __name__ == "__main__":
    db.init_db()
    app.run(debug=True)