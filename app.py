from flask import Flask, redirect
from flask_cors import CORS

from bot import run_bot

app = Flask(__name__)
CORS(app)



import routes

app.register_blueprint(routes.bp_auth)
app.register_blueprint(routes.bp_properties)


@app.route('/')
def index():
    return redirect('https://xtremezz.xyz/discord')

if __name__ == '__main__':
    run_bot()
    app.run(debug=False, host='0.0.0.0', port=80)

