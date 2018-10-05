import re


class Validate:
    def __init__(self,field,data):
        self.status = True
        self.data = data
        self.field = field

    def is_atleast(self,count):
        if not self.status:
            return self
        self.status = len(self.data) > count if self.data != None else False
        if self.status:
            self.message = "Ok"
            return self
        else:
            self.message = self.field+" is too short."
            return self

    def is_atmost(self,count):
        if not self.status:
            return self
        self.status = len(self.data) < count if self.data != None else False
        if self.status:
            self.message = "Ok"
            return self
        else:
            self.message = self.field+" is too short. please rectify"
            return self
    def has_no_numbers(self):
        if not self.status:
            return self
        self.status = re.compile('(?=.*?\d)').search(self.data) == None  if self.data != None else False
        if self.status:
            self.message = "Ok"
            return self
        else:
            self.message = self.field+" contains numbers. please rectify"
            return self
    def is_a_list(self):
        if not self.status:
            return self
        self.status = type(self.data) == type([])  if self.data != None else False
        if self.status:
            self.message = "Ok"
            return self
        else:
            self.message = self.field+" is not a list of items. please rectify"
            return self
    def is_a_number(self):
        if not self.status:
            return self
        try:
            int(self.data)
            self.status = True
        except:
            self.status = False
        if self.status:
            self.message = "Ok"
            return self
        else:
            self.message = self.field+" is not a valid number. please rectify"
            return self

    def has_items(self):
        if not self.status:
            return self
        self.status = len(self.data) > 0  if self.data != None else False
        if self.status:
            self.message = "Ok"
            return self
        else:
            self.message = self.field+" has to have atleast one item. please rectify"
            return self
    def is_an_email(self):
        if not self.status:
            return self
        parts = self.data.split('@')
        check1 = len(parts) == 2
        check2 = False
        if check1:
            check2 = len(parts[1].split('.')) == 2
        self.status = check1 and check2
        if self.status:
            self.message = "Ok"
            return self
        else:
            self.message = "email is invalid. please rectify. "
            return self

class Validation:
    def __init__(self):
        pass
    def validate_admin_usename(self,name):
        result = Validate("username",name).is_atleast(4) \
                                            .is_atmost(25)
        return result
    def validate_email(self,name):
        result = Validate("email",name).is_atleast(7) \
                                            .is_atmost(25) \
                                            .is_an_email()
        return result

    def validate_password(self,password):
        result = Validate("password",password).is_atleast(7) \
                                        .is_atmost(20)
        return result

    def validate_name(self,name):
        result = Validate("Name",name).is_atleast(7) \
                                        .is_atmost(25) \
                                        .has_no_numbers()
        return result
    def validate_title(self,name):
        result = Validate("title",name).is_atleast(3) \
                                        .is_atmost(25) \
                                        .has_no_numbers()
        return result
    def is_a_number(self,number):
        result = Validate("amount",number).is_a_number()
        return result
    def validate_register(self,full_name,username,password):
        result1 = self.validate_name(full_name)
        if not result1.status:
            return result1
        result2 = self.validate_email(username)
        if not result2.status:
            return result2
        result3 = self.validate_password(password)
        if not result3.status:
            return result3
        return result1
