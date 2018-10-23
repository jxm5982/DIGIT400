import pymysql

def connection():
    conn = pymysql.connect(host="localhost",
                            user="root",
                            passwd="your password", #password goes here
                            db = "demo")
    c = conn.cursor()
    
    return c, conn
