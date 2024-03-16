from flask import Flask, request, make_response
import mysql.connector
from comp3161_lab3 import *


app = Flask(__name__)
def db_connection():
    
    conn = mysql.connector.connect(host = "localhost",
                                   user = "root",
                                   password = "Geniu$29",
                                   database = "Comp3161_lab_3"
                                   )
    return conn





@app.route('/hello_world', methods=['GET'])
def hello_world():
    return "hello world"






@app.route('/get_customers', methods=['GET'])
def get_customers():
    try:
        with db_connection() as db:
            cursor = db.cursor()
            cursor.execute('SELECT * from customer;')
            customer_list = []
            for customer_id, gender, age , annualIncome, spendingScore, profession,workExperience, familySize in cursor:
                customer = {}
                customer['customer_id'] = customer_id
                customer['Gender'] = gender
                customer['Age'] = age
                customer['AnnualIncome'] = annualIncome
                customer['SpendingScore'] = spendingScore
                customer['Profession'] = profession
                customer['WorkExperience'] = workExperience
                customer['Family'] = familySize
                customer_list.append(customer)
            cursor.close()
            db.close()
            return make_response(customer_list, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/get_customer/<customer_id>', methods=['GET'])
def get_customer(customer_id):
    try:
        with db_connection() as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT * from customer WHERE customerID={customer_id};")
            col = cursor.fetchone()
            customer = {}
            if col is not None:
                customer_id, gender, age , anualIncome, spendingScore, profession,workExperience, familySize = col
                customer['customer_id'] = customer_id
                customer['Gender'] = gender
                customer['Age'] = age
                customer['AnnualIncome'] = anualIncome
                customer['SpendingScore'] = spendingScore
                customer['Profession'] = profession
                customer['WorkExperience'] = workExperience
                customer['Family'] = familySize
                cursor.close()
                db.close()
                return make_response(customer, 200)
            else:
                return make_response({'error': 'customer not found'}, 400)
    except:
        return make_response({'error': 'An error has occured'}, 400)

# @app.route('/add_customer', methods=['POST'])
# def add_customer():
#     try:
#         db = mysql.connector.connect(
#             host = "localhost",
#             user = "root",
#             password = "Geniu$29",
#             database = "Comp3161_lab_3")
#         cursor = db.cursor()
#         content = request.json
#         # insert_queries()
#         CustomerID = content["CustomerID"]
#         Gender = content["Gender"]
#         Age = content["Age"]
#         Annual_Income = content["AnnualIncome"]
#         Spending_Score = content["SpendingScore"]
#         Profession = content["Profession"]
#         Work_Experience = content["WorkExperience"]
#         Family_Size = content["Family_Size"]
        
#         cursor.executemany(f"INSERT INTO customer (CustomerId, Gender, Age , Annual_Income, Spending_Score, Profession, Work_Experience, Family_Size ) VALUES ({CustomerID}, '{Gender}', {Age} , {Annual_Income}, {Spending_Score}, '{Profession}', {Work_Experience}, {Family_Size}")
#         db.commit()
#         cursor.close()
#         db.close()
#         return make_response({"success" : "customer added"}, 201)
#     except Exception as e:
#         print(e)
#         return make_response({'error': 'An error has occured'}, 400)

@app.route('/update_profession/<customer_id>', methods=['PUT'])
def update_profession(customer_id):
    try:
        
        with db_connection() as db:
            cursor = db.cursor()
            content = request.json
            profession = content['Profession']
            cursor.execute(f"UPDATE customer SET Profession ='{profession}' WHERE customerID={customer_id};")
            db.commit()
            return make_response({"success" : "customer updated"}, 202)
    except Exception as e:
       
        return make_response({'error': str(e)}, 400)
    
@app.route('/highest_income_report', methods=['GET'])
def get_highest_income():
    try:
        with db_connection() as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT CustomerID,Annual_Income,Profession FROM customer ORDER BY Annual_Income desc limit 3;")
            customer_list = []
            
            for customer_id, annualIncome, profession in cursor:
                # customer = {}                
                # customer['AnnualIncome'] = annualIncome
                # customer['customer_id'] = customer_id
                # customer['Profession'] = profession
                response_data = {
                    "CustomerID": customer_id,
                    "AnnualIncome": annualIncome,
                    "Profession": profession}
                customer_list.append(response_data)
            cursor.close()
            db.close()
            return make_response(customer_list, 200)
            
    except Exception as e:
         return make_response({'error': str(e)}, 400)


# @app.route('/highest_income_report', methods=['GET'])
# def get_highest_income():
#     try:
#         with db_connection() as db:
#             cursor = db.cursor()

#             # Find the customer with the highest income
#             cursor.execute("SELECT CustomerID, Annual_Income, Profession FROM customer ORDER BY Annual_Income desc limit 3;")
#             customer = cursor  # Fetch only the single highest-income row

#             # Check if a customer was found
#             while customer is not None:
#                 customer_id, annual_income, profession = customer
#                 response_data = {
#                     "CustomerID": customer_id,
#                     "AnnualIncome": annual_income,
#                     "Profession": profession
#                 }
#                 return make_response(response_data, 200)
#             else:
#                 # Handle the case where no customer exists (optional)
#                 return make_response({'message': 'No customer found'}, 404)

#     except Exception as e:
#         return make_response({'error': str(e)}, 400)       

# @app.route('/delete_customer/<customer_id>', methods=['DELETE'])
# def delete_customer(customer_id):
#     try:
#         db = mysql.connector.connect(user='uwi_user', password='uwi876',
#                                             host='127.0.0.1',
#                                             database='uwi')
#         cursor = db.cursor()
#         cursor.execute(f"DELETE FROM customers WHERE customerID={customer_id}")
#         db.commit()
#         cursor.close()
#         db.close()
#         return make_response({"success" : "customer deleted"}, 200)
#     except Exception as e:
#         return make_response({'error': str(e)}, 400)


# @app.route('/address_report', methods=['GET'])
# def get_addresses():
#     try:
#         db = mysql.connector.connect(user='uwi_user', password='uwi876',
#                                             host='127.0.0.1',
#                                             database='uwi')
#         cursor = db.cursor()
#         cursor.execute(f"SELECT * FROM ALL_ADRESSESS")
#         address_lst = []
#         for add in cursor:
#             address = {}
#             address['Address'] = add[0]
#             address_lst.append(address)
#         return make_response(address_lst, 200)
#     except Exception as e:
#         return make_response({'error': str(e)}, 400)
    
if __name__ == '__main__':
    app.run(port=5000)