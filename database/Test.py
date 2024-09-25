# import mysql.connector

# mydb = mysql.connector.connect(
#   host="localhost",
#   port="3306",
#   user="root",
#   password="password",
#   database="uni"
# )

# print(mydb)

# mycursor = mydb.cursor()
# mycursor.execute("SELECT firstname, no_of_years(dob) as 'years' FROM tblUser")

# db = mycursor.fetchall()

# for i in db:
#   print(i)

# mycursor.execute("SELECT ID, zID FROM tblAcademic")

# db = mycursor.fetchall()

# for i in db:
#   print(i)

from sqlalchemy import create_engine, inspect

engine = create_engine("mysql+mysqlconnector://root:password@localhost:3306/uni")
insp = inspect(engine)

print(insp.get_table_names())
