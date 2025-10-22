from flask import Flask, render_template as ren, request, redirect, url_for, flash
import db
import os, time
import matplotlib
matplotlib.use("Agg")  # 서버 환경에서 GUI 없이 사용
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family = font_name)
plt.rcParams['axes.unicode_minus'] = False

app = Flask(__name__)
app.secret_key = "secret_key123"

def build_avg_plot():
    """과목별 평균 점수를 막대 그래프로 생성"""
    rows = db.get_all_scores()
    df = pd.DataFrame(rows, columns=["sname","kor","eng","mat","total","avg","rank"])
    cols = ["kor","eng","mat"]
    df = df[cols]
    means = df.mean().round(2)
    
    x = np.arange(1,4)
    plt.figure()
    plt.bar(x,means.values, color=["#FF6B46","#51FF8B","#5599FF"])
    plt.ylim(0,100)
    plt.xticks(x, ["국어","영어","수학"])
    plt.ylabel("점수")
    
    # 각 막대 위에 평균 점수 값 표시
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
    # 캐시 방지를 위해 타임스탬프 추가
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
    """CSV 파일을 업로드하여 여러 학생의 점수를 일괄 추가"""
    file = request.files["file"]
    
    try:
        df = pd.read_csv(file, encoding="utf-8-sig")
    except Exception:
        flash("CSV 파일을 읽는 중 오류가 발생했습니다.")
        return redirect(url_for("index"))

    # 필수 칼럼명 검증
    required_cols = ["이름", "국어", "영어", "수학"]
    if list(df.columns) != required_cols:
        flash("CSV 칼럼명이 올바르지 않습니다. (이름, 국어, 영어, 수학 순서여야 합니다.)")
        return redirect(url_for("index"))

    # 각 행의 데이터 검증 및 저장
    for i in range(len(df)):
        sname = df.iloc[i]["이름"]
        
        try:
            kor = float(df.iloc[i]["국어"])
            eng = float(df.iloc[i]["영어"])
            mat = float(df.iloc[i]["수학"])
        except ValueError:
            flash(f"{sname} 행의 점수가 숫자가 아닙니다.")
            return redirect(url_for("index"))

        # 점수 범위 검증 (0~100점)
        if not (0 <= kor <= 100 and 0 <= eng <= 100 and 0 <= mat <= 100):
            flash(f"{sname} 행의 점수가 0~100 범위를 벗어났습니다.")
            return redirect(url_for("index"))

        db.insert_score(sname, kor, eng, mat)

    db.recalc_rank()
    flash("CSV 업로드가 완료되었습니다.")
    return redirect(url_for("index"))

@app.route("/export")
def export():
    """현재 데이터베이스의 모든 점수 데이터를 CSV 파일로 내보내기"""
    rows = db.get_all_scores()
    df = pd.DataFrame(rows, columns=["이름","국어","영어","수학","총점","평균","석차"])
    
    try:
        df.to_csv("scores.csv", encoding="utf-8-sig")
        flash("내보내기 성공")
    except:
        flash("내보내기 도중 오류가 발생하였습니다.")
    
    return redirect(url_for("index"))

if __name__ == "__main__":
    db.init_db()
    app.run(debug=True)