import os
import psycopg2
import urlparse

class DB:
    def __init__ (self,url):
        db_params = urlparse.urlparse(url)
        self.conn = psycopg2.connect(
                                    database= db_params.path[1:],
                                    host = db_params.hostname,
                                    user = db_params.username,
                                    password = db_params.password,
                                    port = db_params.port,
                                    sslmode = 'require'
                                        )
        self.cursor = self.conn.cursor()
        self.make_tables()

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
        command = """CREATE TABLE IF NOT EXISTS Orders(order_id TEXT NOT NULL,
                                                    orderedBy TEXT NOT NULL,
                                                    items TEXT[] NOT NULL,
                                                    total INT NOT NULL,
                                                    status TEXT NOT NULL,
                                                    PRIMARY KEY (order_id) ); """

        self.cursor.execute(command);
        command = """CREATE TABLE IF NOT EXISTS Menu( _id TEXT NOT NULL,
                                                    title TEXT NOT NULL,
                                                    description TEXT NOT NULL,
                                                    amount INT NOT NULL,
                                                    image_url TEXT NOT NULL,
                                                    PRIMARY KEY (_id) ); """

        self.cursor.execute(command);
        command = """CREATE TABLE IF NOT EXISTS Admins(username TEXT NOT NULL,
                                                    password TEXT NOT NULL,
                                                    full_name TEXT NOT NULL,
                                                    PRIMARY KEY (username) ); """
        self.cursor.execute(command);

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
        self.command = """ INSERT INTO Orders(order_id,items,orderedBy,total,status) VALUES (%(order_id)s,%(items)s,%(orderedBy)s,%(total)s,%(status)s); """
        return self.execute()
    def get_order(self,order_id):
        self.values = {'order_id':order_id};
        self.command = """ SELECT * FROM Orders WHERE order_id=%(order_id)s ; """
        return self.execute('SELECT')
    def get_orders_by_client_id(self,client_id):
        self.values = {'order_id':client_id};
        self.command = """ SELECT * FROM Orders WHERE order_by=%(client_id)s ; """
        return self.execute('SELECT')
    def get_orders(self):
        self.values = {'order_id':None};
        self.command = """ SELECT * FROM Orders ; """
        return self.execute('SELECT')
    def update_order_status(self,order_id,status):
        self.values = {'order_id':order_id,'status':status};
        self.command = """ UPDATE Orders SET status=%(status)s WHERE order_id=%(order_id)s ; """
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
        self.command = """ INSERT INTO Menu(_id,title,description,amount,image_url) VALUES (%(id)s,%(title)s,%(description)s,%(amount)s,%(image_url)s); """
        return self.execute()
    def get_menu_item(self,menu_id):
        self.values = {'menu_id':menu_id};
        self.command = """ SELECT * FROM Menu WHERE _id=%(menu_id)s ; """
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

    def insert_admin(self,full_name,username,password):
        self.values = {'username':username,'password':password,'full_name':full_name};
        self.command = """ INSERT INTO Admins(username,password,full_name) VALUES (%(username)s,%(password)s,%(full_name)s); """
        return self.execute()

    def get_admin(self,username,password):
        self.values = {'username':username,'password':password};
        self.command = """ SELECT username,password FROM Admins WHERE username=%(username)s AND password=%(password)s ; """
        return self.execute('SELECT')

    def delete_admin(self,username):
        self.values = {'username':username};
        self.command = """ DELETE FROM Users WHERE username=%(username)s ; """
        return self.execute('DELETE')



db_url = os.environ['DATABASE_URL']
#usersDB = UsersDB()
#adminsDB = AdminsDB()
#menuDB = MenuDB()
#ordersDB = OrdersDB()
#db = DB(db_url)
#db.drop_table('Orders')
