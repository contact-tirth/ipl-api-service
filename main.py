from flask import Flask;

app = Flask(__name__)

@app.route('/')
def temp_fun():
    print('Jay Swamianrayan Tirth')