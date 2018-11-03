import os
import psycopg2
import urlparse
import config

class DB:
    def __init__ (self,url):
        db_params = urlparse.urlparse(url)
        self.conn = psycopg2.connect(
                                    database= db_params.path[1:],
                                    host = db_params.hostname,
                                    user = db_params.username,
                                    password = db_params.password,
                                    port = db_params.port
                                    #,sslmode = 'require'
                                        )

        #self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.conn.cursor()
        self.make_tables()
        self.drop_table('menu')

    def drop_table(self,tablename):
        self.command = "DROP TABLE "+tablename+";"
        self.values = {'tablename':tablename}
        self.cursor.execute(self.command);
        self.conn.commit()
        print tablename+' Dropped'

    def make_tables(self):
        command = """CREATE TABLE IF NOT EXISTS Users(email TEXT NOT NULL,
                                                    password TEXT NOT NULL,
                                                    full_name TEXT NOT NULL,
                                                    PRIMARY KEY (email) ); """
        self.cursor.execute(command);
        self.conn.commit()
        command = """CREATE TABLE IF NOT EXISTS Orders(order_id SERIAL,
                                                    ordered_by TEXT NOT NULL,
                                                    items TEXT[] NOT NULL,
                                                    total INT NOT NULL,
                                                    status TEXT NOT NULL,
                                                    PRIMARY KEY (order_id) ); """

        self.cursor.execute(command);
        self.conn.commit()
        command = """CREATE TABLE IF NOT EXISTS Menu( _id SERIAL,
                                                    title TEXT NOT NULL,
                                                    description TEXT NOT NULL,
                                                    amount INT NOT NULL,
                                                    image_url TEXT NOT NULL,
                                                    PRIMARY KEY (_id) ); """

        self.cursor.execute(command);
        self.conn.commit()
        command = """CREATE TABLE IF NOT EXISTS Admins(username TEXT NOT NULL,
                                                    password TEXT NOT NULL,
                                                    full_name TEXT NOT NULL,
                                                    PRIMARY KEY (username) ); """
        self.cursor.execute(command);
        self.conn.commit()

    def execute(self,operation = 'INSERT'):
        try:
            self.cursor.execute(self.command,(self.values))
            self.conn.commit()
            if operation == 'SELECT':
                return self.cursor.fetchall()
            print 'operation passed'
            return True
        except (Exception, psycopg2.DatabaseError) as error :
            print ' operation failed {}'.format(error)
            return False



class UsersDB(DB):
    def __init__(self):
        DB.__init__(self,db_url)
        self.remove_test_data()

    def remove_test_data(self):
        self.values = {'email':'john.doe@gmail.com'}
        self.command = """ DELETE FROM Users WHERE email=%(email)s; """
        response = self.execute('DELETE')
        print response

    def get_next_id(self):
        self.values = {}
        self.command = """ SELECT email FROM Users; """
        response = self.execute('SELECT')
        return len(response)+1

    def insert_user(self,full_name,email,password):
        self.values = {'email':email,'password':password,'full_name':full_name};
        self.command = """ INSERT INTO Users(email,password,full_name) VALUES (%(email)s,%(password)s,%(full_name)s); """
        return self.execute()
    def get_user(self,email,password):
        self.values = {'email':email,'password':password};
        self.command = """ SELECT email,password FROM Users WHERE email=%(email)s AND password=%(password)s ; """
        return self.execute(operation ='SELECT')
    def check_user(self,email):
        self.values = {'email':email};
        self.command = """ SELECT email FROM Users WHERE email=%(email)s ; """
        return self.execute(operation ='SELECT')
    def update_user_password(self,full_name,email,password):
        self.values = {'full_name':full_name,'email':email,'password':password};
        self.command = """ UPDATE Users SET full_name=%(full_name)s, email=%(email)s,password=%(password)s WHERE email=%(email)s ; """
        return self.execute('SELECT')
    def delete_user(self,email):
        self.values = {'email':email};
        self.command = """ DELETE FROM Users WHERE email=%(email)s ; """
        return self.execute('DELETE')



class OrdersDB(DB):
    def __init__(self):
        DB.__init__(self,db_url)

    def insert_order(self,order_values):
        self.values = order_values;
        self.command = """ INSERT INTO Orders(items,ordered_by,total,status) VALUES (%(items)s,%(ordered_by)s,%(total)s,%(status)s); """
        return self.execute()
    def get_order(self,order_id):
        self.values = {'order_id':order_id};
        self.command = """ SELECT * FROM Orders WHERE order_id=%(order_id)s ; """
        print self.command
        return self.execute('SELECT')
    def get_orders_by_username(self,username):
        self.values = {'ordered_by':username};
        self.command = """ SELECT * FROM Orders WHERE ordered_by=%(ordered_by)s ; """
        return self.execute('SELECT')
    def get_orders(self):
        self.values = {'order_id':None};
        self.command = """ SELECT * FROM Orders ; """
        return self.execute('SELECT')
    def update_order_status(self,order_id,status):
        self.values = {'order_id':order_id,'status':status};
        self.command = """ UPDATE Orders SET status=%(status)s WHERE order_id=%(order_id)s ; """
        print self.command
        return self.execute('UPDATE')
    def delete_order(self,order_id):
        self.values = {'order_id':order_id};
        self.command = """ DELETE FROM Orders WHERE order_id=%(order_id)s ; """
        return self.execute('DELETE')


class MenuDB(DB):
    def __init__(self):
        DB.__init__(self,db_url)
    def insert_menu_item(self,menu_item_values):
        self.values = menu_item_values;
        self.command = """ INSERT INTO Menu(title,description,amount,image_url) VALUES (%(title)s,%(description)s,%(amount)s,%(image_url)s); """
        return self.execute()
    def get_menu_item(self,menu_id):
        self.values = {'menu_id':menu_id};
        self.command = """ SELECT * FROM Menu WHERE _id=%(menu_id)s ; """
        return self.execute('SELECT')
    def get_by_title(self,title):
        self.values = {'title':title};
        self.command = """ SELECT _id FROM Menu WHERE title=%(title)s ; """
        return self.execute('SELECT')

    def get_menu(self):
        self.values = {'menu_id':None};
        self.command = """ SELECT * FROM Menu ; """
        return self.execute('SELECT')
    def delete_menu_item(self,menu_id):
        self.values = {'menu_id':menu_id};
        self.command = """ DELETE FROM Menu WHERE _id=%(menu_id)s ; """
        return self.execute('DELETE')


class AdminsDB(DB):
    def __init__(self):
        DB.__init__(self,db_url)
        self.remove_test_data()

    def remove_test_data(self):
        self.values = {'username':'john.admin@gmail.com'}
        self.command = """ DELETE FROM Admins WHERE username=%(username)s; """
        response = self.execute('DELETE')
        print response

    def get_next_id(self):
        self.values = {}
        self.command = """ SELECT * FROM Admins; """
        response = self.execute('SELECT')
        return len(response)+1

    def insert_admin(self,full_name,username,password):
        self.values = {'username':username,'password':password,'full_name':full_name};
        self.command = """  INSERT INTO Admins(username,password,full_name) VALUES (%(username)s,%(password)s,%(full_name)s); """
        return self.execute()


    def get_admin(self,username,password):
        self.values = {'username':username,'password':password};
        self.command = """ SELECT username,password FROM Admins WHERE username=%(username)s AND password=%(password)s ; """
        return self.execute('SELECT')

    def delete_admin(self,username):
        self.values = {'username':username};
        self.command = """ DELETE FROM Users WHERE username=%(username)s ; """
        return self.execute('DELETE')


#read database url from enviroment variable
FLASK_ENV = os.environ.get('FLASK_ENV')
print FLASK_ENV
db_url = config.PRODUCTION_DB_URL
#db_url = "postgress://postgres:postgres@localhost:5432/fastfoodfastlocal"
if FLASK_ENV == 'development':
    db_url = config.DEVELOPMENT_DB_URL

print 'CURRENT DB URL is '+db_url
