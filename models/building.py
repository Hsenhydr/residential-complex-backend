from extensions import db

class Building(db.Model):
    __tablename__ = "buildings"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    complex_id = db.Column(db.Integer, db.ForeignKey("residential_complexes.id"), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey("admins.id"))
