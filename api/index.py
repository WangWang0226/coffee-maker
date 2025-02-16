from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from coffeemaker import make_coffee_with
from flask_socketio import SocketIO

load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    summary, profile_pic_url = make_coffee_with(name=name, socketio=socketio)
    return jsonify(
        {
            "summary_and_questions": summary.to_dict(),
            "picture_url": profile_pic_url,
        }
    )
    
# Required for Vercel
app.debug = True

if __name__ == "__main__":
    socketio.run(
        app, host="0.0.0.0", port=5000, debug=True
    )
