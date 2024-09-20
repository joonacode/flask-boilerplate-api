from datetime import datetime, timezone

from api.extensions import db


class Blog(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(128))
    content = db.Column(db.Text())
    status = db.Column(db.Integer(), default=0)
    user_id = db.Column(db.ForeignKey("user.id"))
    user = db.relationship('User', lazy=True)
    created_at = db.Column(db.DateTime(), default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(), default=datetime.now(timezone.utc))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_all_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def delete_by_id(cls, id):
        blog = cls.query.get(id)
        db.session.delete(blog)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def toDICT(self):
        cls_dict = {}
        cls_dict["id"] = self.id
        cls_dict["title"] = self.title
        cls_dict["content"] = self.content
        cls_dict["status"] = self.status
        cls_dict["created_at"] = self.created_at
        cls_dict["user_id"] = self.user_id
        cls_dict["updated_at"] = self.updated_at

        return cls_dict

    def toJSON(self):
        return self.toDICT()
