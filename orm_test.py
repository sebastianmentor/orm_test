from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask("__name__")

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/hockeybasen'
db = SQLAlchemy(app)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(80), unique=False, nullable=False)
    city = db.Column(db.String(80), unique=False, nullable=False)
    players = db.relationship('Player', backref='team', lazy=True)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(80), unique=False, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    jersey = db.Column(db.Integer, unique=False, nullable=False)
    team_id=db.Column(db.Integer, db.ForeignKey('team.id'),
        nullable=False)

# //Automatiskt skapa tabeller!!!
with app.app_context():
    db.create_all()
    db.session.connection()
    #db.init_app()
    while True:
        print("1. Skapa team")
        print("2. Skapa player")
        print("3. Lista alla teams")
        print("4. Skriv ut alla spealre")
        print("5. Uppdatera")
        print("6. Sök spelare")
        print("0. Avsluta")
        val = input(">>>")

        match val:
            case "0":
                break

            case "1":
                team = Team()
                team.namn = input("Ange namn:")
                team.city = input("Ange city:")
                db.session.add(team)
                db.session.commit()
                
            case "2":
                player = Player()
                player.namn = input("Ange namn:")
                player.jersey = int(input("Ange jersey:"))
                player.year = int(input("Ange år:"))
                for team in Team.query.all():
                    print(f"{team.id} {team.namn} {team.city}")

                player.team_id = int(input("Ange team id:"))
                db.session.add(player)
                db.session.commit()

            case "3":
                for team in Team.query.all():
                    print(f"{team.id} {team.namn} {team.city}")

            case "4":
                for team in Team.query.all():
                    print(f"{team.id} {team.namn} {team.city}")
                    for player in team.players:
                        print(f"\t{player.id} {player.jersey} {player.namn}")

            case "5":
                for team in Team.query.all():
                    print(f"{team.id} {team.namn} {team.city}")

                sel = int(input("Vilket teamid vill du uppdatera?"))

                team = Team.query.filter_by(id=sel).first()
                if not team: continue
                team.namn = input("Ange nytt namn:")
                team.city = input("Ange nytt city:")
                db.session.commit()

            case "6":
                search = input("Sök efter: ")
                print("Sökresultat----->")
                for m in Player.query.filter(Player.namn.contains(search)).all():
                    print(f"{m.id} {m.namn}")
                print("Slut.......")

            

