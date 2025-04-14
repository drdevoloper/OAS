# Vehicle Auction Web App

A dynamic web-based vehicle auction platform where users can register, add vehicles for auction, place real-time bids, and complete the checkout process upon winning. The system is built using Flask, MongoDB, HTML, CSS, and JavaScript.

---

## Features

- **User Authentication**
  - User Registration & Login
  - Separate Admin Login & Access

- **Vehicle Management**
  - Add vehicles with images and details
  - Store vehicle data in MongoDB
  - Dynamically display listed vehicles

- **Real-time Bidding**
  - Bidding form with bidder name & amount
  - Real-time bid updates displayed as animated cards
  - Auction countdown timer
  - Bids stored in MongoDB

- **Checkout & Transactions**
  - Automatically redirect winning bidder to checkout
  - Display winner details and transaction summary
  - Loading animation on checkout
  - Comment & Payment Section

- **Admin Dashboard**
  - View all transactions
  - View active users and vehicles

---

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python Flask  
- **Database:** MongoDB  
- **Libraries/Tools:** Flask-PyMongo, Bcrypt, Werkzeug


---

## Setup Instructions

1. Clone the Repository
   ```bash
   git clone https://github.com/yourusername/vehicle-auction-app.git
   cd vehicle-auction-app

2. Install Requirements
   pip install -r requirements.txt

3. Start MongoDB (locally or connect with MongoDB Atlas)

4. Run the Flask App
     python app.py


---

Authors
Barath Kumaran SB
SRM Institute of Science and Technology
Vijay TS
SRM Institute of Science and Technology
