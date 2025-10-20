from flask import Flask, render_template as ren, request, redirect, url_for, flash
import db

app = Flask(__name__)

@app.route("/")
def index():
    return ren("index.html")

# Flask 서버 실행
if __name__ == "__main__":
    db.init_db()
    app.run(debug=True)