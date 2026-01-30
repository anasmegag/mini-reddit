from extenction import db
from datetime import datetime
from sqlalchemy import func

class Post(db.Model):
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
    
    @staticmethod 
    def get_votes(post_id):
        from models.vote import Vote
        
        # On additionne toutes les "value" (1 et -1) pour ce post_id
        score = db.session.query(func.sum(Vote.value)).filter_by(post_id=post_id).scalar()
        
        # Si le post n'a aucun vote, MySQL rend None, on retourne donc 0
        return score if score is not None else 0
    
    @staticmethod
    def get_posts():        
        posts = Post.query.order_by(Post.publish_time.desc()).all()    
        res = []
        for post in posts:
            res.append({
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "user_id": post.user_id,
                "publish_time": post.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
                "score": Post.get_votes(post.id) # On utilise ta méthode de score ici !
            })
            
        return res