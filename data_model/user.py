

class User:

    id = 0
    first_name = ''
    last_name = ''
    login = ''
    password = ''
    email = ''

    def __init__(self, id:int, login:str, password:str, first_name:str="", last_name:str="", email:str=""):
        if id == 0:
            raise Exception('Error creating user object: bad id')

        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.login = login
        self.password = password
        self.email = email

