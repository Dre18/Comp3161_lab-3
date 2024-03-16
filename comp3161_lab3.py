import mysql.connector
import csv

def db_connection():
    
    conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Geniu$29",
    database = "Comp3161_lab_3"
    )
    return conn
def create_tables():
    with open('created_customer_tables.sql', 'w') as file:
        # file.write(f"create database Comp3161_lab_3;\n")
        file.write(f"use Comp3161_lab_3;\n")
        file.write(f"create table customer (CustomerID int primary key ,Gender varchar(255) not null ,Age int not null ,Annual_Income int not null,Spending_Score int not null ,Profession varchar(255),Work_Experience int not null ,Family_Size int not null);\n")
        file.close()
def import_file():
    with open('customers.csv', 'r') as file:
        customer = csv.reader(file)
        customer_list = list(customer)
        customer_list = customer_list[1:]
        # file.close()
        return customer_list
        
def insert_queries():
    with db_connection() as db:
        mycursor = db.cursor()
        for c in import_file():
            customer = (int(c[0]),str(c[1]),int(c[2]),int(c[3]),int(c[4]),str(c[5]),int(c[6]),int(c[7]))
            customers = "INSERT INTO customer (CustomerId, Gender, Age , Annual_Income, Spending_Score, Profession, Work_Experience, Family_Size ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            mycursor.execute(customers,customer)
        db.commit()
        db.close()
        
    
if __name__ == "__main__":
    global customer_list
    create_tables()
    import_file()
    insert_queries()
    
    
