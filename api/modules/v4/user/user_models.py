from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from api.extensions import db


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text())
    token = db.Column(db.Text())
    status = db.Column(db.Integer(), default=0)
    created_at = db.Column(db.DateTime(), default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(), default=datetime.now(timezone.utc))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update_email(self, new_email):
        self.email = new_email

    @classmethod
    def get_all(cls):
        return cls.query.get_all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_by_token(cls, token):
        return cls.query.filter_by(token=token).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def toDICT(self):

        cls_dict = {}
        cls_dict["_id"] = self.id
        cls_dict["name"] = self.name
        cls_dict["email"] = self.email
        cls_dict["status"] = self.email

        return cls_dict

    def toJSON(self):
        return self.toDICT()

    @property
    def blogs(self):
        from ..blog.blog_models import Blog

        return db.relationship(Blog, back_populates="user")
