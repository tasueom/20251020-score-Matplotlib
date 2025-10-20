from flask import Flask, render_template as ren, request, redirect, url_for, flash

app = Flask(__name__)

@app.route("/")
def index():
    return ren("index.html")

# Flask 서버 실행
if __name__ == "__main__":
    app.run(debug=True)