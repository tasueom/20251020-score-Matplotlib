from flask import Flask, render_template as ren, request, redirect, url_for, flash
import db
import os, time
import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family = font_name)
plt.rcParams['axes.unicode_minus'] = False

app = Flask(__name__)

def build_avg_plot():
    rows = db.get_all_scores()
    df = pd.DataFrame(rows, columns=["sname","kor","eng","mat","total","avg","rank"])
    cols = ["kor","eng","mat"]
    df = df[cols]
    means = df.mean()
    x = np.arange(1,4)
    plt.figure()
    plt.bar(x,means.values, color=["#FF6B46","#51FF8B","#5599FF"])
    plt.ylim(0,100)
    plt.xticks(x, ["국어","영어","수학"])
    plt.title("과목별 평균")
    plt.ylabel("점수")
    out_path = os.path.join(app.root_path, "static", "img", "subject_avg.png")
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    return means.round(2).to_dict(), "subject_avg.png"

@app.route("/")
def index():
    score_list = db.get_all_scores()
    means, fname = build_avg_plot()
    img_url = url_for("static", filename=f"img/{fname}") + f"?v={int(time.time())}"
    return ren("index.html", score_list=score_list, means=means, img_url=img_url)

@app.route("/add_score", methods=["POST"])
def add_score():
    sname = request.form["sname"]
    kor = int(request.form["kor"])
    eng = int(request.form["eng"])
    mat = int(request.form["mat"])
    db.insert_score(sname, kor, eng, mat)
    db.recalc_rank()
    return redirect(url_for('index'))

# Flask 서버 실행
if __name__ == "__main__":
    db.init_db()
    app.run(debug=True)