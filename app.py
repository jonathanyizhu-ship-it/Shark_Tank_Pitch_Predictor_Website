from flask import Flask, render_template, jsonify

app = Flask(__name__)

INPUT_DATA = [
   {
     'id': 1,
     'Title': 'Market Value',
     'Description': 'The total value of the market your company is involved in'

   },
   {
     'id': 2,
     'Title': 'Total Revenue',
     'Description': 'Total Sales/Revenue of the comapny'
   },
   {
     'id': 3,
     'Title': 'Profit Margin',
     'Description': 'Unit Cost of Mnufacturing/Selling Price of Product(in percetage, if 50% write 50)'
   },
   {
     'id': 4,
     'Title': 'Years of Operation',
     'Description': 'How many years has the company been in operation(Decimals are allowed)'
   },
   {
     'id': 5,
     'Title': 'Debt',
     'Description': 'What is the comapnies total debt?'
   },
   {
     'id': 6,
     'Title': 'Company Valuation',
     'Description': 'How much is your comapny worth?'
   }
 ]

@app.route("/")
def hello_world():
  return render_template('home.html',input_data = INPUT_DATA )

@app.route("/api/input_data")
def data_input():
  return jsonify(INPUT_DATA)

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug = True)