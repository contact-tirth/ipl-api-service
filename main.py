from flask import Flask, jsonify, request;
import pandas as pd
import numpy as np

import ipl

app = Flask(__name__)

@app.route('/')
def temp_fun():
    return 'Jay Swamianrayan Tirth'

@app.route('/teamsname')
def get_teams_name():
    final_team_name=ipl.unique_teams_api()
    return jsonify(final_team_name)

@app.route('/get_teams_record')
def get_teams_record():
    team1=request.args.get('team1')
    team2=request.args.get('team2')
    # return team1+team2
    response = ipl.teams_record(team1, team2)
    return jsonify(response)

app.run(debug=True)