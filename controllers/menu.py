from flask import jsonify,g,request
from models import auth,menu
from utils.access import Access


class MenuController:
    def __init__(self):
        self.menu_model = menu.MenuModel()
        pass

    def get_menu(self):
        return jsonify(self.menu_model.get_menu()),200

    def post_to_menu(self,data):
        if data is None:
            return jsonify({'error':'No Json Data received. '}), 400
        if not "title" in data or not "description" in data or not "amount" in data:
            return jsonify({'error':'bad or corrupted data.'}),200
        else:
            title = data["title"]
            description = data["description"]
            amount = data["amount"]
            if "img_url" in data:
                if len(data["img_url"]) > 5:
                    img_url = data["img_url"]
                else:
                    img_url = "http://placehold.it/200x200"
            else:
                img_url = "http://placehold.it/200x200"
            dbresult = self.menu_model.create_menu_item(title,description,amount,img_url)
            if dbresult:
                return jsonify({'status':'success','message':'menu item  added successfully'}),200
            else:
                return jsonify({'status':'error','message':'database error'}),400

    def delete_menu_item(self,id):
        if not self.menu_model.get_menu(id) is None:
            self.menu_model.remove_menu_item(id)
            return jsonify({'success':'menu item '+id+' deleted'}),200
        else:
            return jsonify({'error':'menu item '+id+' does not exist'}),200
