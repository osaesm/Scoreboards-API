from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import desc, asc

from datetime import datetime

import os

# Init app
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Individual NBA Game
class NBA_Game(db.Model):
    __tablename__ = "nba_games"
    game = db.Column(db.Integer, primary_key=True)
    home = db.Column(db.String(100))
    away = db.Column(db.String(100))
    homescore = db.Column(db.Integer)
    awayscore = db.Column(db.Integer)
    # matches = db.relationship('NBA', backref='nba_game', lazy=True)

    def __init__(self, game, home, away, homescore, awayscore):
        self.game = game
        self.home = home
        self.away = away
        self.homescore = homescore
        self.awayscore = awayscore

class GameSchema(ma.Schema):
    class Meta:
        fields = ('game', 'home', 'away', 'homescore', 'awayscore') # Add matches?

game_schema = GameSchema(strict=True)
games_schema = GameSchema(many=True, strict=True)

# NBA Matches Class/Model
class NBA(db.Model):
    __tablename__ = "NBA_Matches"
    id = db.Column(db.Integer, primary_key = True)
    team_name = db.Column(db.String(50))
    date = db.Column(db.DateTime)
    # game_id = db.Column(db.Integer, db.ForeignKey('nba_games.game'))
    game_id = db.Column(db.Integer)


    def __init__(self, team_name, date, game_id):
        self.team_name = team_name
        self.date = date
        self.game_id = game_id


# Product Schema
class NBASchema(ma.Schema):
    class Meta:
        fields = ('id', 'team_name', 'date', 'game_id')

nba_schema = NBASchema(strict=True) # 1 game
nbas_schema = NBASchema(many=True, strict=True) #multiple games



# Create a game for a team
@app.route('/matches', methods=['POST'])
def add_match():
    team_name = request.json['team_name']
    date = request.json['date']
    datetime_obj = datetime.strptime(date, "%Y-%m-%d")
    date = datetime_obj
    game_id = request.json['game_id']

    new_match = NBA(team_name , date, game_id)

    db.session.add(new_match)
    db.session.commit()

    return nba_schema.jsonify(new_match)

@app.route('/matches', methods=['GET'])

def get_match():
    all_matches = NBA.query.order_by(desc(NBA.date)).all()
    result = nbas_schema.dump(all_matches)
    return jsonify(result.data)

@app.route('/matches/<team>', methods=['GET'])

def get_match_by_team(team):
    all_matches = NBA.query.filter_by(team_name=team).order_by(desc(NBA.date)).all()
    result = nbas_schema.dump(all_matches)
    return jsonify(result.data)


@app.route('/games', methods=['POST'])
def create_game():
    game_id = request.json['game_id']
    home = request.json['home']
    away = request.json['away']
    homescore = request.json['homescore']
    awayscore = request.json['awayscore']


    new_game = NBA_Game(game_id , home, away, homescore, awayscore)

    db.session.add(new_game)
    db.session.commit()

    return game_schema.jsonify(new_game)


@app.route('/games', methods=['GET']) # Get team game stats of the all games in database
def get_games():
    all_games = NBA_Game.query.all()
    result = games_schema.dump(all_games)
    return jsonify(result.data)

@app.route('/games/<game_id>', methods=['GET']) # Get team game stats of specific game in database
def get_game(game_id):
    game = NBA_Game.query.get(game_id)
    return game_schema.jsonify(game)

@app.route('/matches/all/<team>') # Get all the team game stats of a specific team
def get_team_games(team):
    game_ids = [match.game_id for match in NBA.query.filter_by(team_name=team).order_by(desc(NBA.date)).all()]
    print(game_ids)
    query = NBA_Game.query.filter(NBA_Game.game.in_(game_ids)).all()
    result = games_schema.dump(query)
    return jsonify(result.data)

@app.route('/matches/all/<team>/<date>') # Get all the team game stats of a specific team on a specific date
def get_team_game_by_date(team, date):
    date = datetime.strptime(date, "%Y-%m-%d")
    game_ids = [match.game_id for match in NBA.query.filter_by(team_name=team, date=date).all()]
    # print(game_ids)
    query = NBA_Game.query.filter(NBA_Game.game.in_(game_ids)).all()
    result = games_schema.dump(query)
    return jsonify(result.data)


@app.route('/matches/date/<date1>/<date2>') # Get all the team game stats of a specific team between a specific date
def get_games_by_date(date1, date2):
    date1 = datetime.strptime(date1, "%Y-%m-%d")
    date2 = datetime.strptime(date2, "%Y-%m-%d")
    game_ids = [match.game_id for match in NBA.query.filter(NBA.date>=date1, NBA.date<=date2).all()]
    # print(game_ids)
    query = NBA_Game.query.filter(NBA_Game.game.in_(game_ids)).all()
    result = games_schema.dump(query)
    return jsonify(result.data)

@app.route('/matches/<team>/<date1>/<date2>') # Get all the team game stats of a specific team between dates
def get_team_games_between_date(team, date1, date2):
    date1 = datetime.strptime(date1, "%Y-%m-%d")
    date2 = datetime.strptime(date2, "%Y-%m-%d")
    game_ids = [match.game_id for match in NBA.query.filter(NBA.date>=date1, NBA.date<=date2).filter_by(team_name=team).all()]
    # print(game_ids)
    query = NBA_Game.query.filter(NBA_Game.game.in_(game_ids)).all()
    result = games_schema.dump(query)
    return jsonify(result.data)

    
# Run Server
if __name__ == "__main__":
    app.run(debug=True)