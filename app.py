from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    customer_name = request.form['customer_name']
    items = request.form.getlist('item')
    quantities = request.form.getlist('quantity')
    prices = request.form.getlist('price')

    for quantity, price in zip(quantities, prices):
        if not quantity.isdigit() or float(price) <= 0:
            return render_template('index.html', error_message='Invalid input. Please enter valid quantities and prices.')

    total_amount = sum([int(qty) * float(price) for qty, price in zip(quantities, prices)])

    invoice_number = datetime.now().strftime('%Y%m%d%H%M%S')
    current_date = datetime.now().strftime('%Y-%m-%d')

    invoice_data = zip(items, quantities, prices)

    return render_template('invoice.html', invoice_number=invoice_number, current_date=current_date,
                           customer_name=customer_name, invoice_data=invoice_data, total_amount=total_amount)

if __name__ == '__main__':
    app.run(debug=True)
