from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from dateutil import parser
import pytz
import os
import time
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img/uploads'
app.secret_key = 'supersecretkey'

ist = pytz.timezone('Asia/Kolkata')
print(datetime.now(ist))

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

client = MongoClient('mongodb://localhost:27017/')
db = client['auction_system']
vehicles_collection = db['vehicles']
user_collections = db['register']

try:
    client.admin.command('ping')
    print("✅ MongoDB connection successful!")
except Exception as e:
    print("❌ MongoDB connection failed:", e)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = user_collections.find_one({'username': username, 'password': password})
        if user:
            session['username'] = user['username']
            session['role'] = user.get('role', 'user') 

            flash('Login successful!')

            if user.get('role') == 'admin':
                return redirect(url_for('admin_dashboard'))  
            else:
                return redirect(url_for('home'))  
            
        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        gmail = request.form.get('gmail')
        phno = request.form.get('phno')
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')  

        if username and password:
            if user_collections.find_one({'username': username}):
                flash('Username already exists. Try another one.')
                return redirect(url_for('register'))

            user_collections.insert_one({
                'username': username,
                'password': password,
                'gmail': gmail,
                'ph.no': phno,
                'role': role
            })
            flash('User registered successfully!')
            return redirect(url_for('login'))  
        else:
            flash('Please fill all fields.')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/add')
def add_page():
    return render_template('add.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    name = request.form.get('name')
    vehicle_type = request.form.get('vehicle_type')
    brand = request.form.get('brand')
    vehicle_name = request.form.get('vehicle_name')
    about = request.form.get('about')
    phone = request.form.get('phone')
    price = request.form.get('price')
    bid_end = request.form.get('bid_end')
    images = request.files.getlist('images')

    image_urls = []
    for image in images:
        if image:
            filename = secure_filename(image.filename)
            timestamp = str(int(time.time()))
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
            image_urls.append(filepath.replace('\\', '/'))  

    bid_end_time = parser.parse(bid_end).astimezone(ist)

    vehicle_data = {
        'name': name,
        'vehicle_type': vehicle_type,
        'brand': brand,
        'vehicle_name': vehicle_name,
        'about': about,
        'phone': phone,
        'price': int(price),
        'bid_end': bid_end_time.strftime("%Y-%m-%dT%H:%M:%S"),
        'images': image_urls,
        'created_at': datetime.now(ist),
        'bids': []
    }

    vehicles_collection.insert_one(vehicle_data)
    return redirect(url_for('bid_vehicle'))


@app.route('/bid')
def bid_vehicle():
    vehicles = list(vehicles_collection.find())
    current_time = datetime.now(ist)
    updated_vehicles = []

    for vehicle in vehicles:
        try:
            bid_end = vehicle.get('bid_end')
            if bid_end:
                bid_end_time = parser.parse(bid_end).astimezone(ist)
                if current_time > bid_end_time:
                    bids = vehicle.get('bids', [])
                    winner = None
                    amount = None
                    if bids:
                        highest_bid = max(bids, key=lambda b: b['amount'])
                        winner = highest_bid['name']
                        amount = highest_bid['amount']

                    vehicles_collection.update_one(
                        {'_id': vehicle['_id']},
                        {'$set': {
                            'is_expired': True,
                            'winner': winner,
                            'winning_amount': amount
                        }}
                    )
                    vehicle['is_expired'] = True
                    vehicle['winner'] = winner
                    vehicle['winning_amount'] = amount
                else:
                    vehicle['is_expired'] = False
        except Exception as e:
            print("⚠️ Error parsing bid_end:", e)

        updated_vehicles.append(vehicle)

    return render_template('bid.html', vehicles=updated_vehicles)


@app.route('/submit_bid/<vehicle_id>', methods=['POST'])
def submit_bid(vehicle_id):
    bidder_name = request.form.get('bidder_name')
    amount = request.form.get('amount')

    if not amount:
        return "Bid amount is required", 400

    try:
        bid_amount = int(amount)
    except ValueError:
        return "Invalid bid amount", 400

    vehicle = vehicles_collection.find_one({'_id': ObjectId(vehicle_id)})
    if not vehicle:
        return "Vehicle not found", 404

    bid_end_str = vehicle.get('bid_end')
    if bid_end_str:
        bid_end_time = parser.parse(bid_end_str).astimezone(ist)
        if datetime.now(ist) >= bid_end_time:
            return "Bidding has ended for this vehicle.", 400

    bids = vehicle.get('bids', [])
    highest_existing_bid = max([b['amount'] for b in bids], default=vehicle['price'])

    if bid_amount <= highest_existing_bid:
        return "Bid must be higher than the current highest bid", 400

    new_bid = {
        'name': bidder_name,
        'amount': bid_amount,
        'timestamp': datetime.now(ist)
    }
    vehicles_collection.update_one(
        {'_id': ObjectId(vehicle_id)},
        {'$push': {'bids': new_bid}}
    )

    return redirect(url_for('bid_vehicle'))

@app.route('/checkout/', defaults={'vehicle_id': None})
@app.route('/checkout/<vehicle_id>')
def checkout(vehicle_id):
    if vehicle_id:
        vehicle = vehicles_collection.find_one({'_id': ObjectId(vehicle_id)})
        if not vehicle:
            return "Vehicle not found", 404
        vehicle['_id'] = str(vehicle['_id'])  
    else:
        vehicle = None  
    return render_template('checkout.html', vehicle=vehicle)


@app.route('/admin')
def admin_dashboard():
    vehicles = list(vehicles_collection.find())     
    return render_template('admin.html', vehicles=vehicles)

@app.route('/delete_vehicle/<vehicle_id>', methods=['POST'])
def delete_vehicle(vehicle_id):
    vehicle = vehicles_collection.find_one({'_id': ObjectId(vehicle_id)})
    if vehicle and 'images' in vehicle:
        image_folder = app.config['UPLOAD_FOLDER']
        for image_filename in vehicle['images']:
            image_path = os.path.join(image_folder, secure_filename(image_filename))
            if os.path.exists(image_path):
                os.remove(image_path) 

    vehicles_collection.delete_one({'_id': ObjectId(vehicle_id)})
    return redirect(url_for('admin_dashboard'))


@app.route('/end_bid/<vehicle_id>', methods=['POST'])
def end_bid(vehicle_id):
    vehicles_collection.update_one(
        {'_id': ObjectId(vehicle_id)},
        {'$set': {'is_expired': True}}
    )
    print("Bid Ended for:", vehicle_id)
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    app.run(debug=True)



