from db import db

class User(db.Model, UserMixin):
    UID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), unique=True)
    balance = db.Column(db.Float, nullable=False)
    
    def __str__(self):
        return f"User('{self.username}', '{self.password}', '{self.email}', '{self.balance}')"
    
    def get_id(self):
        return self.UID
    
    def get_all_users(self):
        return User.query.all()
    
class Orders(db.Model):
    OID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    UID = db.Column(db.Integer, db.ForeignKey('user.UID'), nullable=False)
    ticker = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    is_sold = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f"Orders('{self.UID}', '{self.ticker}', '{self.quantity}', '{self.is_sold}', '{self.date}')"
    
    def get_all_orders(self):
        return Orders.query.all()