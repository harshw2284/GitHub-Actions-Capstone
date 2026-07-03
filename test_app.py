from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def test_home():
    return render_template("index.html")


@app.route("/health")
def test_health():
    return {
        "status": "healthy",
        "application": "Simple Flask App"
    }


@app.route("/about")
def test_about():
    return {
        "developer": "Harsh Bhagat",
        "project": "DevSecOps Demo Pipeline"
    }


if __name__ == "__main__":
    app.run(port=80)