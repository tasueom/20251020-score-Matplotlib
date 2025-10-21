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
app.secret_key = "secret_key123"

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
    plt.ylabel("점수")
    for i, value in enumerate(means.values):
        plt.text(x[i], value + 1, str(value), ha='center', va='bottom', color='black', fontsize=10)
    out_path = os.path.join(app.root_path, "static", "img", "subject_avg.png")
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    return "subject_avg.png"

@app.route("/")
def index():
    score_list = db.get_all_scores()
    fname = build_avg_plot()
    img_url = url_for("static", filename=f"img/{fname}") + f"?v={int(time.time())}"
    return ren("index.html", score_list=score_list, img_url=img_url)

@app.route("/add_score", methods=["POST"])
def add_score():
    sname = request.form["sname"]
    kor = int(request.form["kor"])
    eng = int(request.form["eng"])
    mat = int(request.form["mat"])
    db.insert_score(sname, kor, eng, mat)
    db.recalc_rank()
    return redirect(url_for('index'))

@app.route("/add_csv", methods=['POST'])
def add_csv():
    file = request.files["file"]
    try:
        df = pd.read_csv(file, encoding="utf-8-sig")
    except Exception:
        flash("CSV 파일을 읽는 중 오류가 발생했습니다.")
        return redirect(url_for("index"))

    required_cols = ["이름", "국어", "영어", "수학"]
    if list(df.columns) != required_cols:
        flash("CSV 칼럼명이 올바르지 않습니다. (이름, 국어, 영어, 수학 순서여야 합니다.)")
        return redirect(url_for("index"))

    for i in range(len(df)):
        sname = df.iloc[i]["이름"]
        try:
            kor = float(df.iloc[i]["국어"])
            eng = float(df.iloc[i]["영어"])
            mat = float(df.iloc[i]["수학"])
        except ValueError:
            flash(f"{sname} 행의 점수가 숫자가 아닙니다.")
            return redirect(url_for("index"))

        if not (0 <= kor <= 100 and 0 <= eng <= 100 and 0 <= mat <= 100):
            flash(f"{sname} 행의 점수가 0~100 범위를 벗어났습니다.")
            return redirect(url_for("index"))

        db.insert_score(sname, kor, eng, mat)

    db.recalc_rank()
    flash("CSV 업로드가 완료되었습니다.")
    return redirect(url_for("index"))

# Flask 서버 실행
if __name__ == "__main__":
    db.init_db()
    app.run(debug=True)