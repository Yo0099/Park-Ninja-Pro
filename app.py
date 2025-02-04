from flask import Flask, render_template, request, redirect, url_for, jsonify
import time

app = Flask(__name__)

# Simulated balance
user_balance = 20.0

# Parking fee: First 10 sec free, then RM 1 per min
parking_fee_per_min = 1.0
free_parking_time = 10  # seconds
parking_start_time = None
allocated_spot = None

@app.route("/")
def home():
    global parking_start_time, allocated_spot
    parking_start_time = time.time()  # Start timing
    allocated_spot = 4  # Simulating spot assignment
    return render_template("index.html", spot=allocated_spot)

@app.route("/payment")
def payment():
    global user_balance, parking_start_time
    parking_duration = int(time.time() - parking_start_time)
    chargeable_minutes = max(0, (parking_duration - free_parking_time) // 60)
    total_fee = chargeable_minutes * parking_fee_per_min

    return render_template("payment.html", 
                           duration=parking_duration, 
                           fee=total_fee, 
                           balance=user_balance)

@app.route("/process_payment", methods=["POST"])
def process_payment():
    global user_balance
    total_fee = float(request.form.get("fee"))

    if user_balance >= total_fee:
        user_balance -= total_fee
        return redirect(url_for("success", fee=total_fee, balance=user_balance))
    else:
        return redirect(url_for("failure", fee=total_fee, balance=user_balance))

@app.route("/success")
def success():
    fee = request.args.get("fee")
    balance = request.args.get("balance")
    return render_template("success.html", fee=fee, balance=balance)

@app.route("/failure")
def failure():
    fee = request.args.get("fee")
    balance = request.args.get("balance")
    return render_template("failure.html", fee=fee, balance=balance)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

