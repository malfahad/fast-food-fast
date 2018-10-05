import db

class MenuModel:
    def __init__(self):
        self.menu_db = db.MenuDB()
        pass

    def create_menu_item(self,title,description,amount,img_url):
        self.title = title
        self.description = description
        self.amount = amount
        self.img_url = img_url
        return self.save()

    def save(self):
        return self.menu_db.insert_menu_item(self.json())

    def json(self):
        return {'title':self.title,'description':self.description,'amount':self.amount,'image_url':self.img_url}

    def get_menu(self,_id = None):
        if _id == None:
            rows = self.menu_db.get_menu()
        else:
            rows = self.menu_db.get_menu_item(_id)
            if rows == []:
                return None
        if rows == None:
            return rows
        result = {}
        for row in rows:
            result[row[0]] = {'id':row[0],
                              'title':row[1],
                              'description':row[2],
                              'amount':row[3],
                              'image_url':row[4]}
        return result

    def is_duplicate(self,title):
        title = title.strip()
        rows = self.menu_db.get_by_title(title)
        print rows
        if rows == None:
            return False
        if len(rows) == 0:
            return False
        return True

    def remove_menu_item(self,_id):
        return self.menu_db.delete_menu_item(_id)
