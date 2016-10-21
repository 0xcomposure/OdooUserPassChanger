from passlib.context import CryptCto context
import psycopg2, getpass, signal, sys

"""Function to print a message when Ctrl+C is pressed."""
def handler(signum, frame):
    print ('\nLeaving the application...\nGood bye!')
    sys.exit(0)

signal.signal(signal.SIGINT, handler)

"""variables to get DB connection data, user you want to change de password and the new password for the user."""
dbname = input("Enter the DB name: ")
dbuser = input("Enter the DB user: ")
dbpass = getpass.getpass("Enter the password for " + dbuser + ": ")
dbhost = input("Enter the host[localhost]: ") or "localhost"

usertoupdate = input("Enter the user you want to change the password: ")
newpass = getpass.getpass("Enter the new password for "+usertoupdate+": ")

newpass_crypt = CryptContext(['pbkdf2_sha512']).encrypt(newpass)

"""
try to connect with the DB and make the update with the new password.
if the connection failed return a message.
"""
try:
    conn = psycopg2.connect("dbname='" + dbname + "' user='" + dbuser + "' host='" + dbhost + "' password='" + dbpass + "'")
    print ("Opened database successfully")
    cur = conn.cursor()
    cur.execute("UPDATE res_users SET password_crypt = '"+newpass_crypt+"' WHERE login = '"+usertoupdate+"'")
    conn.commit()
    conn.close()
    print("Password for "+usertoupdate+" has been updated successfully")
except:
    print ("Unable to connect to the database")
