from extenction import db

class  Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    post_id= db.Column(db.Integer,db.ForeignKey('posts.id'),nullable=False)
    value = db.Column(db.Integer,nullable=False,)
    __table_args__ = (
        db.CheckConstraint('value IN (-1, 1)', name='check_vote_value'),
        db.UniqueConstraint('user_id', 'post_id', name='unique_user_vote_per_post')
    )

    @staticmethod
    def vote(user_id, post_id, value):    
        exist = Vote.query.filter_by(user_id=user_id, post_id=post_id).first()

        if exist:        
            if value != exist.value:
                exist.value = value
                db.session.commit()
                return "Vote mis à jour"
            else:            
                return "Déjà voté avec cette valeur"
        else:        
            new_vote = Vote(user_id=user_id, post_id=post_id, value=value)
            db.session.add(new_vote)
            db.session.commit()
            return "Vote ajouté"
    
    @staticmethod
    def unVote(user_id,post_id):
        exist= Vote.query.filter_by(user_id=user_id, post_id=post_id).first()
        if not exist:
            return "vote n'existe pas"
        db.session.delete(exist)
        db.session.commit()
        return "vote supprimer"
        
            

