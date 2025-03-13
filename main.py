from flask import Flask, jsonify, request;
import pandas as pd
import numpy as np

import campusx
import ipl

app = Flask(__name__)

@app.route('/')
def temp_fun():
    return 'Jay Swamianrayan Tirth'

@app.route('/teamsname')
def get_teams_name():
    final_team_name=ipl.unique_teams_api()
    return jsonify(final_team_name)

@app.route('/playername')
def get_players_name():
    final_player_name=ipl.unique_players()
    return jsonify(final_player_name)

@app.route('/get_teams_record')
def get_teams_record():
    team1=request.args.get('team1')
    team2=request.args.get('team2')
    # return team1+team2
    response = ipl.teams_record(team1, team2)
    return jsonify(response)

@app.route('/api/team-record')
def team_record():
    team_name = request.args.get('team')
    # response = campusx.teamAPI(team_name)
    response = ipl.team_analysis(team_name)
    return response

@app.route('/api/batsman_record')
def batsman_record():
    batsman_name=request.args.get('bats_name')
    # response_bat=ipl.batsman_analysis(batsman_name)
    response_bat = ipl.batsman_API(batsman_name)
    return response_bat


@app.route('/api/batsman_record_campusx')
def batsman_record_campusx():
    batsman_name=request.args.get('bats_name1')
    response_bat=campusx.batsmanAPI(batsman_name)
    return response_bat

app.run(debug=True)



