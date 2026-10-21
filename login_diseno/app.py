from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return "<h2 style='font-family:sans-serif;padding:2rem'>Holaaaaaaaaaa</h2>"


if __name__ == "__main__":
    app.run(debug=True)
