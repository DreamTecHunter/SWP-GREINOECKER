import datetime

from flask import Flask, request, jsonify
from sqlalchemy import Column, Integer, Text, Float, DateTime, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func
from flask_restful import Resource, Api
from dataclasses import dataclass
import json
from flask_cors import CORS, cross_origin

Base = declarative_base()  # Basisklasse aller in SQLAlchemy verwendeten Klassen
metadata = Base.metadata

# engine = create_engine('sqlite:///catalog.db') #sqlite
engine = create_engine('mysql+pymysql://swp-greinoecker:swp-greinoecker@localhost/catalog')  # mysql

db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
Base.query = db_session.query_property()  # Dadurch hat jedes Base - Objekt (also auch ein GeoInfo) ein Attribut query für Abfragen
app = Flask(__name__)  # Die Flask-Anwendung
cors = CORS(app)  # Ohne dieser Anweisung darf man von Webseiten aus nicht zugrfeifen
api = Api(app)  # Die Flask API


@dataclass  # Diese ermoeglicht das Schreiben als JSON mit jsonify
class CatalogProgress(Base):
    __tablename__ = 'progress'  # Abbildung auf diese Tabelle
    id: int
    card_id: int
    description: str
    datetime: DateTime

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer)
    description = Column(Text)
    datetime = Column(DateTime)


class CatalogProgressREST(Resource):
    def get(self, id):
        info = CatalogProgress.query.get(id)
        return jsonify(info)

    def put(self, id):
        data = request.get_json(force=True)['params']
        info = CatalogProgress(card_id=id, description=data['description'], datetime=datetime.datetime.now())
        print(info)
        db_session.add(info)
        db_session.flush()
        return jsonify(info)

    def delete(self, id):
        info = CatalogProgress.query.get(id)
        if info is None:
            return jsonify({'message': 'object with id %d does not exist' % id})
        db_session.delete(info)
        db_session.flush()
        return jsonify({'message': '%d deleted' % id})

    def patch(self, id):
        print(request.json)
        info = CatalogProgress.query.get(id)
        if info is None:
            return jsonify({'message': 'object with id %d does not exist' % id})
        description = request.json['params']['description']
        info.description = description
        db_session.add(info)
        db_session.flush()
        return jsonify({'message': 'object with id %d modified' % id})

    @app.route('/cat-search/<q>')
    def cat_search(q):
        infos = CatalogProgress.query.filter(CatalogProgress.description.contains(q)).all()
        return jsonify(infos)

    @app.route('/card-search/<q>')
    def card_id_search(q):
        infos = CatalogProgress.query.filter(CatalogProgress.card_id.contains(q)).all()
        return jsonify(infos)


api.add_resource(CatalogProgressREST, '/card-item/<int:id>')


@app.teardown_appcontext
def shutdown_session(exception=None):
    print("Shutdown Session")
    db_session.remove()


if __name__ == '__main__':
    app.run(debug=True, port=5002)
