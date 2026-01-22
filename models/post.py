from extenction import db
from datetime import datetime

class Post(db.model):
    __tablename__ = 'posts'
    id = id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    title = db.Columnn(db.String(50),nullable=False)
    content = db.Column(db.String(1000),nullable=False)
    publish_time = db.Column(db.DateTime,default=datetime.utcnow)

    @staticmethod
    def addPost(user_id,title,content):
        new_post = Post(user_id=user_id,title=title,content=content)
        db.session.add(new_post)
        db.session.commit()
        return new_post.id
    
    @staticmethod
    def deletePost(user_id,post_id):
        exist= Post.query.filter_by(id=post_id).first()
        if not exist:
            return "post n'existe pas"
        if exist.user_id==user_id:
            db.session.delete(exist)
            db.session.commit()
            return "suppression reussite"
        return "pas ton poste pour supprimer"