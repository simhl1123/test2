from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'employee'


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('AddEmp.html')


@app.route("/about", methods=['POST'])
def about():
    return render_template('www.intellipaat.com')


@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    Payscale = request.form['Payscale']
    Department = request.form['Department']
    Hire_Date = request.form['Hire_Date']
    emp_image_file = request.files['emp_image_file']

    insert_sql = "INSERT INTO test1 VALUES (%s, %s, %s, %s, %s)"                     #CHANGE NAME
    cursor = db_conn.cursor()

    if emp_image_file.filename == "":
        return "Please select a file"

    try:

        cursor.execute(insert_sql, (emp_id, first_name, Payscale, Department, Hire_Date))
        db_conn.commit()
        empl_id = "" + emp_id 
        emp_name = "" + first_name 
        emp_Payscale = "" + Payscale 
        emp_Department = "" + Department 
        emp_Hire_Date = "" + Hire_Date 
        # Uplaod image file in S3 #
        emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                emp_image_file_name_in_s3)

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('AddEmpOutput.html', id=empl_id, name=emp_name, Payscale=emp_Payscale, Department=emp_Department, Date=emp_Hire_Date)


@app.route("/addemp1", methods=['GET', 'POST'])
def addemp1():
    return render_template('AddEmp.html')

@app.route("/getemp", methods=['GET', 'POST'])
def addemp1():
    return render_template('GetEmp.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
