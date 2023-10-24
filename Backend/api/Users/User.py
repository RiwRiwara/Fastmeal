import datetime

class User:
    def __init__(self, id, name, email, password, role, phone) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.phone = phone
        self.isDeleted = False
        self.createdAt = None  # Initialize with None
        self.updatedAt = None  # Initialize with None
        self.set_created_at()
        self.set_updated_at()

    def getJson(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "phone": self.phone,
            "isDeleted": self.isDeleted,
            "createdAt": self.createdAt,  
            "updatedAt": self.updatedAt  
        }

    def set_created_at(self):
        self.createdAt = datetime.datetime.utcnow()

    def set_updated_at(self):
        self.updatedAt = datetime.datetime.utcnow()
