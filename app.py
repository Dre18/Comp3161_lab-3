from flask import Flask, request, make_response
import mysql.connector
from comp3161_lab3 import insert_queries


app = Flask(__name__)
def db_connection():
    
    conn = mysql.connector.connect(host = "localhost",
                                   user = "root",
                                   password = "Geniu$29",
                                   database = "Comp3161_lab_3"
                                   )
    return conn





@app.route('/customers', methods=['GET'])
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

@app.route('/customer/<customer_id>', methods=['GET'])
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


@app.route('/add_customer', methods=['POST'])
def add_customer():
    try:
        with db_connection() as db:
            cursor = db.cursor()

            content = request.json
            customer_data = (
                content.get("CustomerID"),
                content.get("Gender"),
                content.get("Age"),
                content.get("AnnualIncome"),
                content.get("SpendingScore"),
                content.get("Profession"),
                content.get("WorkExperience"),
                content.get("FamilySize"),
            )

            cursor.execute(f"INSERT INTO customer (CustomerId, Gender, Age , Annual_Income, Spending_Score, Profession, Work_Experience, Family_Size ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", customer_data)
            db.commit()  
            d = insert_queries()

            return make_response({"success": "Customer added"}, 201)

    except Exception as e:
        
        return make_response({'error': 'An error has occurred'}, 400)


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

    
@app.route('/total_income_report', methods=['GET'])
def get_total_income():
    try:
        with db_connection() as db:
            cursor = db.cursor()
            cursor.execute(f"select sum(Annual_Income) as TotalIncome, Profession from customer group by Profession ;")
            customer_list = []
            
            for total_Income, profession in cursor:
                response_data = {
                    "Profession": profession,
                    "TotalIncome": total_Income
                    }
                customer_list.append(response_data)
            cursor.close()
            db.close()
            return make_response(customer_list, 200)
    except Exception as e:
         return make_response({'error': str(e)}, 400)
     
     
@app.route('/average_spending_score/<profession>', methods=['GET'])
def get_avg_spending_score(profession):
    try:
        with db_connection() as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT Gender, AVG(Spending_Score) AS AverageSpendingScore FROM customer WHERE Profession = '{profession}' GROUP BY Gender;")
            customer_list = []
            
            for gender, spendingScore in cursor:
                response_data = {
                    "Gender": gender,
                    "AverageSpendingScore": spendingScore
                    }
                customer_list.append(response_data)
            cursor.close()
            db.close()
            return make_response(customer_list, 200)
    except Exception as e:
         return make_response({'error': str(e)}, 400)
     
     
     
@app.route('/average_work_experience', methods=['GET'])
def get_avg_experience():
    try:
        with db_connection() as db:
            cursor = db.cursor()

            cursor.execute(f"SELECT Profession, round(AVG(Work_Experience)) AS AverageExperience FROM customer WHERE Age < 35 AND Annual_Income > 50000 GROUP BY Profession;")
            response_data = [
                {
                "Profession": profession, 
                "AverageExperience": experience
                 }
                for profession, experience in cursor
            ]

            return make_response(response_data, 200)

    except Exception as e:
        print(e)
        return make_response({'error': 'An error has occurred'}, 400)

    
if __name__ == '__main__':
    app.run(port=5000)
   