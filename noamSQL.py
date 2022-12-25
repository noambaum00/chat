import sqlite3
###noam 152433!qwe azure admin username & password

def admin_sign_in(username, password):
  # Connect to the database
  conn = sqlite3.connect('users.db')
  cursor = conn.cursor()

  # Query the database to see if the username and password are correct
  query = 'SELECT * FROM admins WHERE username=? AND password=?'
  cursor.execute(query, (username, password))

  # If the query returns a result, the sign in was successful
  if cursor.fetchone():
    print('{username} Sign in successful!')
  else:
    print('{username}  Sign in failed. Incorrect username or password.')

  # Clean up
  cursor.close()
  conn.close()


def client_sign_in(username, password):
  # Connect to the database
  conn = sqlite3.connect('users.db')
  cursor = conn.cursor()

  # Query the database to see if the username and password are correct
  query = 'SELECT * FROM users WHERE username=? AND password=?'
  cursor.execute(query, (username, password))

  # If the query returns a result, the sign in was successful
  if cursor.fetchone():
    print('Sign in successful!')
  else:
    print('Sign in failed. Incorrect username or password.')

  # Clean up
  cursor.close()
  conn.close()


def add_user(username, password, email):
  # Connect to the database
  conn = sqlite3.connect('users.db')
  cursor = conn.cursor()

  # Insert the new user into the users table
  query = 'INSERT INTO users (username, password, email) VALUES (?, ?, ?)'
  cursor.execute(query, (username, password, email))

  # Commit the changes to the database
  conn.commit()

  # Clean up
  cursor.close()
  conn.close()



def get_email(username):
  # Connect to the database
  conn = sqlite3.connect('users.db')
  cursor = conn.cursor()

  # Query the database for the user's password
  query = 'SELECT email FROM users WHERE username=?'
  cursor.execute(query, (username,))

  # Get the password from the result
  password = cursor.fetchone()[0]

  # Clean up
  cursor.close()
  conn.close()

  return password


def delete_user(username):
  # Connect to the database
  conn = sqlite3.connect('users.db')
  cursor = conn.cursor()

  # Delete the user from the users table
  query = 'DELETE FROM users WHERE username=?'
  cursor.execute(query, (username,))

  # Commit the changes to the database
  conn.commit()

  # Clean up
  cursor.close()
  conn.close()

def user_exists(username):
  # Connect to the database
  conn = sqlite3.connect('users.db')
  cursor = conn.cursor()

  # Query the database for the user
  query = 'SELECT * FROM users WHERE username=?'
  cursor.execute(query, (username,))

  # If the query returns a result, the user exists
  if cursor.fetchone():
    exists = True
  else:
    exists = False

  # Clean up
  cursor.close()
  conn.close()

  return exists

def change_password(username, old_password, new_password):
  # Connect to the SQL database
  conn = sqlite3.connect('users.db')

  # Query the database to check if the provided username and old password are valid
  query = "SELECT * FROM users WHERE username=? AND password=?"
  result = conn.execute(query, (username, old_password))

  # If the query returns a row, then the password can be changed
  if result.fetchone():
    # Update the password in the database
    update_query = "UPDATE users SET password=? WHERE username=?"
    conn.execute(update_query, (new_password, username))
    conn.commit()

    print("Password successfully updated!")
    return True
  else:
    print("Password change failed. Invalid username or password.")
    return False

