from flask import Flask, render_template, request, make_response
import pdfkit

app = Flask(__name__)

def custom_zip(*iterables):
    return zip(*iterables)

app.jinja_env.filters['custom_zip'] = custom_zip

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    invoice_number = request.form['invoice_number']
    customer_name = request.form['customer_name']
    items = request.form.getlist('item')
    quantities = [int(quantity) for quantity in request.form.getlist('quantity')]
    prices = [float(price) for price in request.form.getlist('price')]

    rendered_invoice = render_template('invoice.html', invoice_number=invoice_number, customer_name=customer_name,
                                       items=items, quantities=quantities, prices=prices)


    pdf = pdfkit.from_string(rendered_invoice, False,configuration=pdfkit.configuration(wkhtmltopdf='C:\Program Files\wkhtmltopdf/bin/wkhtmltopdf.exe'))

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=invoice.pdf'

    return response

if __name__ == '__main__':
    app.run(debug=True)
