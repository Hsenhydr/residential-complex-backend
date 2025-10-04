from extensions import db

class ResidentialComplex(db.Model):
    __tablename__ = "residential_complexes"
    
    id = db.Column(db.Integer, primary_key=True)
    identity = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255))
    campaign_info = db.Column(db.String(255))
    admin_id = db.Column(db.Integer, db.ForeignKey("admins.id"))
    buildings = db.relationship("Building", backref="complex", lazy=True)
