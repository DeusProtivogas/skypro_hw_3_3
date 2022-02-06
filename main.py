from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import prettytable
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#
class User(db.Model):
    __tablename__ = "user_table"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text(200))
    last_name = db.Column(db.Text(200))
    age = db.Column(db.Integer)
    email = db.Column(db.Text(200))
    role = db.Column(db.Text(200))
    phone = db.Column(db.Integer)

    def inst_to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
        }


class Order(db.Model):
    __tablename__ = "order_table"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text(200))
    description = db.Column(db.Text(200))
    start_date = db.Column(db.Text(200))
    end_date = db.Column(db.Text(200))
    address = db.Column(db.Text(200))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user_table.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user_table.id'))
    customer = db.relationship('User', foreign_keys=[customer_id])
    executor = db.relationship('User', foreign_keys=[executor_id])

    def inst_to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id,
        }


class Offer(db.Model):
    __tablename__ = "offer_table"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order_table.id'))
    order = db.relationship('Order')
    executor_id = db.Column(db.Integer, db.ForeignKey('user_table.id'))
    executor = db.relationship('User')

    def inst_to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
        }


with db.session.begin():
    db.drop_all()
    db.create_all()

with open("users.json") as f:
    raw_json = f.read()

users = json.loads(raw_json)
# print(users)
for user in users:
    temp_user = User(
        id=user['id'],
        first_name=user['first_name'],
        last_name=user['last_name'],
        age=user['age'],
        email=user['email'],
        role=user['role'],
        phone=user['phone']
    )

    db.session.add(temp_user)

db.session.commit()

session = db.session()
cursor = session.execute("SELECT * FROM user_table").cursor
mytable = prettytable.from_db_cursor(cursor)
print(mytable)

###

with open("orders.json", encoding="utf-8") as f:
    raw_json = f.read()

orders = json.loads(raw_json)
print(orders)
# print(orders)
for order in orders:
    temp_order = Order(
        id=order['id'],
        name=order['name'],
        description=order['description'],
        start_date=order['start_date'],
        end_date=order['end_date'],
        address=order['address'],
        price=order['price'],
        customer_id=order['customer_id'],
        executor_id=order['executor_id'],
    )

    db.session.add(temp_order)

db.session.commit()

cursor = session.execute('SELECT * FROM order_table ').cursor
mytable = prettytable.from_db_cursor(cursor)
print(mytable)

###

with open("offers.json") as f:
    raw_json = f.read()

offers = json.loads(raw_json)
# print(users)
for offer in offers:
    temp_offer = Offer(
        id=offer['id'],
        order_id=offer['order_id'],
        executor_id=offer['executor_id'],
    )

    db.session.add(temp_offer)

db.session.commit()

session = db.session()
cursor = session.execute("SELECT * FROM offer_table").cursor
mytable = prettytable.from_db_cursor(cursor)
print(mytable)


@app.route("/users", methods=['GET', 'POST'])
def get_all_users():
    # all_users = User.query.all()
    if request.method == 'GET':
        return jsonify([x.inst_to_dict() for x in User.query.all()])
    if request.method == 'POST':
        new_data = json.loads(request.data)
        new_user = User(
            id=new_data['id'],
            first_name=new_data['first_name'],
            last_name=new_data['last_name'],
            age=new_data['age'],
            email=new_data['email'],
            role=new_data['role'],
            phone=new_data['phone']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify([x.inst_to_dict() for x in User.query.all()])


@app.route("/users/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def get_user(id):
    # all_users = User.query.all()
    if request.method == 'GET':
        return jsonify(User.query.get(id).inst_to_dict())
    if request.method == 'DELETE':
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return f"Deleted user {id}"
    if request.method == 'PUT':
        new_data = json.loads(request.data)
        user = User.query.get(id)
        user.first_name = new_data['first_name']
        user.last_name = new_data['last_name']
        user.first_name = new_data['first_name']
        user.age = new_data['age']
        user.email = new_data['email']
        user.role = new_data['role']
        user.phone = new_data['phone']
        db.session.add(user)
        db.session.commit()
        return jsonify(User.query.get(id).inst_to_dict())


@app.route("/orders", methods=['GET', 'POST'])
def get_all_orders():
    # all_users = User.query.all()
    if request.method == 'GET':
        return jsonify([x.inst_to_dict() for x in Order.query.all()])
    if request.method == 'POST':
        new_data = json.loads(request.data)
        new_order = Order(
            id=new_data['id'],
            name=new_data['name'],
            description=new_data['description'],
            start_date=new_data['start_date'],
            end_date=new_data['end_date'],
            address=new_data['address'],
            price=new_data['price'],
            customer_id=new_data['customer_id'],
            executor_id=new_data['executor_id'],
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify([x.inst_to_dict() for x in Order.query.all()])


@app.route("/orders/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def get_order(id):
    # all_users = User.query.all()
    # return jsonify( Order.query.get(id).inst_to_dict() )

    if request.method == 'GET':
        return jsonify(Order.query.get(id).inst_to_dict())
        # return jsonify( User.query.get(id).inst_to_dict() )
    if request.method == 'DELETE':
        order = Order.query.get(id)
        db.session.delete(order)
        db.session.commit()
        return f"Deleted order {id}"
    if request.method == 'PUT':
        new_data = json.loads(request.data)
        order = Order.query.get(id)

        order.id = new_data['id']
        order.name = new_data['name']
        order.description = new_data['description']
        order.start_date = new_data['start_date']
        order.end_date = new_data['end_date']
        order.address = new_data['address']
        order.price = new_data['price']
        order.customer_id = new_data['customer_id']
        order.executor_id = new_data['executor_id']

        db.session.add(order)
        db.session.commit()
        return jsonify(Order.query.get(id).inst_to_dict())


@app.route("/offers", methods=['GET', 'POST'])
def get_all_offers():
    # all_users = User.query.all()
    # print([x.inst_to_dict() for x in Offer.query.all()])

    if request.method == 'GET':
        return jsonify([x.inst_to_dict() for x in Offer.query.all()])
    if request.method == 'POST':
        new_data = json.loads(request.data)
        new_offer = Offer(
            id=new_data['id'],
            order_id=new_data['order_id'],
            executor_id=new_data['executor_id'],
        )
        db.session.add(new_offer)
        db.session.commit()
        return jsonify([x.inst_to_dict() for x in Offer.query.all()])


@app.route("/offers/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def get_offer(id):
    # all_users = User.query.all()

    if request.method == 'GET':
        return jsonify(Offer.query.get(id).inst_to_dict())
        # return jsonify( User.query.get(id).inst_to_dict() )
    if request.method == 'DELETE':
        offer = Offer.query.get(id)
        db.session.delete(offer)
        db.session.commit()
        return f"Deleted offer {id}"
    if request.method == 'PUT':
        new_data = json.loads(request.data)
        offer = Offer.query.get(id)

        offer.id = new_data['id']
        offer.order_id = new_data['order_id']
        offer.executor_id = new_data['executor_id']

        db.session.add(offer)
        db.session.commit()
        return jsonify(Offer.query.get(id).inst_to_dict())


if __name__ == "__main__":
    app.run()
