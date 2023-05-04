import maskpass
import mysql.connector
from os import system, name
import sys

def line():
      print("+-"*15)

def clear():
      if name == 'nt':
            _ = system('cls')

def continue_():
      continue_process = int(input("Continue Process(yes=1/no=0) >>> "))

      if continue_process == 1:
            pass
      elif continue_process == 0:
            sys.exit(1)
            cur.close()
            conn.close()
      else:
            continue_()

def db_con():
      clear()
      
      global conn
      global cur

      
      try:
            db_pass = maskpass.askpass(prompt="Please enter database password\n>>> ")
            
            conn = mysql.connector.connect(
                  host = "127.0.0.1",
                  user = "root",
                  password = db_pass,
                  database = "passwm"
            )

            cur = conn.cursor()
            
      except mysql.connector.Error as e:
            print("Error ", e)
            db_con()
      else:
            main()
     
def create():
      
      # Create New Data
      print("Create a Password\n")
      try:  
            account = input("Enter your new account: ")
            password = input("Enter your new password: ")

            data_input = (account, password)

            sql = "INSERT INTO data (account,password) VALUES (%s,%s)"

            try:
                  cur.execute(sql, data_input)
                        
            except mysql.connector.DataError as e:
                  # Rollback data
                  conn.rollback()
                  print("Failed to Create: ", e)
            else:
                  # Melakukan commit data
                  conn.commit()
                  print("Successfully created")
      except mysql.connector.Error as e:
            print("Error ", e)
      else:
            pass

def read():
      
      # Read data
      print("Show Password List\n")

      try:
            sql = "SELECT * FROM data"

            try:
                  cur.execute(sql)
                  records = cur.fetchall()
                  print("Password Account Data")
                  for (Id, Account, Password) in records:
                        print(Id, '\t', Account, '\t', Password)
                        
            except mysql.connector.DataError as e:
                  # Rollback data
                  conn.rollback()
                  print("Failed to Read: ", e)
            else:
                  # Commit data
                  conn.commit()
      except mysql.connector.Error as e:
            print("Error: ", e)
      else:
            pass

def update():
      
      # Update data
      print("Change Account Data\n")

      read()

      try:
            line()
            idSearch = input("Enter the account id: ")
            passwordEdited = input("Enter new password: ")
            
            sql = "UPDATE data SET password = %s WHERE id = %s"
            val = (passwordEdited, idSearch)

            try:
                  cur.execute(sql, val)
            except mysql.connector.DataError as e:
                  # Rollback data
                  conn.rollback()
                  print("Failed to Update: ", e)
                  
            else:
                  # Commit data
                  conn.commit()
                  print("Successfully updated")
      except mysql.connector.Error as e:
            print("Error: ", e)
      else:
            pass
      
def delete():
      # Delete data
      print("Delete Account Data\n")

      read()
      
      try:
            line()
            idDeleted = input("Enter the account id: ")

            sql = f"DELETE FROM data WHERE id = {idDeleted}"

            try:
                  cur.execute(sql)
            except mysql.connector.DataError as e:
                  # Rollback data
                  conn.rollback()
                  print("Failed to Delete: ", e)
                  
            else:
                  # Commit data
                  conn.commit()
                  print("Successfully deleted")
                  
      except mysql.connector.Error as e:
            print("Error: ", e)
      else:
            pass

def main():
      
      while True:
            clear()
            
            print("Password Manager by Maszack\n")
            
            # Show option
            print("1. Create \n2. Read \n3. Update \n4. Delete \n5. Quit \nInteger input")

            # Store option
            opt = int(input(">>> "))

            # Branching
            if opt == 1:
                  clear()
                  create()
                  line()
                  continue_()
            elif opt == 2:
                  clear()
                  read()
                  line()
                  continue_()
            elif opt == 3:
                  clear()
                  update()
                  line()
                  continue_()
            elif opt == 4:
                  clear()
                  delete()
                  line()
                  continue_()
            elif opt == 5:
                  sys.exit(1)
                  cur.close()
                  conn.close()
            else:
                  print("Error")

if __name__ == "__main__":
      db_con()
