from .import db
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index =True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    bio = db.Column(db.String(5000))
    profile_pic_path = db.Column(db.String)
    pass_secure = db.Column(db.String(255))       
    date_joined = db.Column(db.DateTime,default=datetime.utcnow)

    pitches = db.relationship('Pitch',backref = 'user',lazy = "dynamic")

    comments = db.relationship('Comment',backref = 'user',lazy = "dynamic")

    @property
    def password(self):
            raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
            self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
            return check_password_hash(self.pass_secure,password)



    def __repr__(self):
        return f'User {self.username}'

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'

class Pitch(db.Model):
    __tablename__ = 'pitch'
    id = db.Column(db.Integer,primary_key = True)
    title_pitch = db.Column(db.String(255)) 
    content_pitch = db.Column(db.String(500)) 
    category = db.Column(db.String)
    post = db.Column(db.DateTime,default=datetime.utcnow) 
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer) 

    comments = db.relationship('Comment',backref ='pitch_id',lazy = "dynamic")
    def save_pitch(self):
      db.session.add(self)
      db.session.commit()


    @classmethod
    def get_pitches(cls,category):
      pitches = Pitch.query.filter_by(category = category).all()

      return pitches

    @classmethod
    def get_pitch(cls,id):
     pitch = Pitch.query.filter_by(id=id).first()
     return pitch


    @ classmethod
    def pitches_count(cls,uname):
     user = User.query.filter_by(username=uname).first()
     pitches = Pitch.query.filter_by(user_id=user.id).all()
     count_pitches = 0
     for pitch in pitches:
        count_pitches += 1

     return count_pitches

class Comment(db.Model):
    __tablename__= 'comments'
    id = db.Column(db.Integer,primary_key = True)
    Comment = db.Column(db.String(100))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comment(cls,pitch):
        comment = Comment.query.filter_by (pitch_id=pitch).all()
        return comment
 