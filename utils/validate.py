import re
menuids = ['12','123','1']
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

result = Validate("password",None).is_atleast(6) \
                                    .is_atmost(25) \
print result.status
print result.message

result = Validate("password","strongpassword").is_atleast(6) \
                                    .is_atmost(25) \
print result.status
print result.message

result = Validate("email","wrongmail").is_atleast(6) \
                                    .is_atmost(25) \
                                    .is_an_email() \
print result.status
print result.message

result = Validate("full name","weird name1").is_atleast(6) \
                                    .is_atmost(25) \
                                    .has_no_numbers()
print result.status
print result.message

result = Validate("items",["123,123,123"]).is_a_list() \
                                    .has_items() \
                                    .has_valid_order_items()
print result.status
print result.message
