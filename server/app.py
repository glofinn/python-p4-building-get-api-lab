#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    baked_goods = []
    for baked_good in Bakery.query.all():

        baked_good_dict = baked_good.to_dict()
        baked_goods.append(baked_good_dict)

    response = make_response(
        jsonify(baked_goods),
        200
        )
    
    response.headers["Content-Type"] = "application/json"
    
    return response
    


@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    
    baked_goods = Bakery.query.filter(Bakery.id==id).first()
    baked_goods_dict = baked_goods.to_dict()

    response = make_response(
        jsonify(baked_goods_dict),
        200
    )

    response.headers["Content-Type"] = "application/json"

    return response



@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = []
    for baked_good in BakedGood.query.order_by(desc(BakedGood.price)).all():
        baked_goods_dict = baked_good.to_dict()
        baked_goods.append(baked_goods_dict)

    response = make_response(
        jsonify(baked_goods),
        200
    )

    response.headers["Content-Type"] = "application/json"

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_baked_good = BakedGood.query.order_by(desc(BakedGood.price)).first()
    most_expensive_baked_good_dict = most_expensive_baked_good.to_dict()

    response = make_response(
        jsonify(most_expensive_baked_good_dict),
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=555, debug=True)
