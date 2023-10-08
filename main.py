from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/cereg/PycharmProjects/homework3/main.py'
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    duration = db.Column(db.Integer)

@app.route('/names/', methods=['GET'])
def get_unique_names():
    unique_names = db.session.query(Customer.first_name).distinct()
    unique_names = [row[0] for row in unique_names]
    return jsonify(unique_names)

@app.route('/customers/', methods=['GET'])
def get_customers():
    query_parameters = request.args
    first_name = query_parameters.get('first_name')
    last_name = query_parameters.get('last_name')

    customers_query = Customer.query

    if first_name:
        customers_query = customers_query.filter(Customer.first_name.like(f'%{first_name}%'))

    if last_name:
        customers_query = customers_query.filter(Customer.last_name.like(f'%{last_name}%'))

    customers = customers_query.all()
    customers_list = [{'id': customer.id, 'first_name': customer.first_name, 'last_name': customer.last_name}
                      for customer in customers]
    return jsonify(customers_list)

@app.route('/tracks/count', methods=['GET'])
def get_track_count():
    track_count = Track.query.count()
    return jsonify({'count': track_count})

@app.route('/tracks/duration', methods=['GET'])
def get_track_duration():
    tracks = Track.query.all()
    track_list = [{'name': track.name, 'duration': track.duration} for track in tracks]
    return jsonify(track_list)

if __name__ == '__main__':
    app.run(debug=True)