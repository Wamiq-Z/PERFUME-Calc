from config import db

class Compounds(db.Model):
    # __tablename__ = "compounds"
    # __table_args__ = {"schema": "perfume"}
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True, nullable = False)
    price_perkg = db.Column(db.Float, nullable = False)

    def __repr__(self):
        return f"Compound: {self.name},{self.price_perkg}" 
