from flask import jsonify,g,request
from models import auth,menu
from utils.access import Access
from utils.validate import Validation


check_valid = Validation()


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
            return jsonify({'error':'required field is missing.'}),400
        else:
            title = data["title"].strip()
            description = data["description"]
            amount = data["amount"]
            result = self.menu_model.is_duplicate(title);
            if result:
                return jsonify({'error':title+'  already on the menu.'}),400
            val_result = check_valid.validate_title(title)
            if not val_result.status:
                return jsonify({'error':val_result.message}),400
            val_result = check_valid.is_a_number(amount)
            if not val_result.status:
                return jsonify({'error':val_result.message}),400
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
            return jsonify({'success':'menu item with id '+id+' deleted'}),200
        else:
            return jsonify({'error':'menu item with  id '+id+' does not exist'}),200
