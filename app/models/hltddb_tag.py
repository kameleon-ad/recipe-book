from sqlalchemy import and_
# from sqlalchemy.orm import backref
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db


class HltddbTag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hltddb_pid = db.Column(UUID, db.ForeignKey('hltddb.pid'), nullable=False)
    tag_pid = db.Column(UUID, db.ForeignKey('tag.pid'), nullable=False)

    # hltddb = db.relationship('Hltddb', backref=backref('hltddb_tag', lazy=True))
    # tag = db.relationship('Tag', backref=backref('hltddb_tag', lazy=True))

    @staticmethod
    def get(hltddb_pid, tag_pid):
        hltddb_pid, tag_pid = str(hltddb_pid), str(tag_pid)
        return HltddbTag.query\
            .filter(and_(HltddbTag.hltddb_pid == hltddb_pid, HltddbTag.tag_pid == tag_pid)).first()

    @staticmethod
    def insert(hltddb_pid, tag_pid):
        hltddb_pid, tag_pid = str(hltddb_pid), str(tag_pid)

        hltddb_tag = HltddbTag.get(hltddb_pid, tag_pid)

        if hltddb_tag is None:
            hltddb_tag = HltddbTag(hltddb_pid=hltddb_pid, tag_pid=tag_pid)
            db.session.add(hltddb_tag)
            db.session.commit()

        return hltddb_tag

    @staticmethod
    def update(hltddb_pid, old_tag_pid, new_tag_pid):
        hltddb_pid, old_tag_pid, new_tag_pid = str(hltddb_pid), str(old_tag_pid), str(new_tag_pid)
        hltddb_tag: HltddbTag = HltddbTag.get(hltddb_pid, old_tag_pid)
        hltddb_tag.tag_pid = new_tag_pid
        db.session.commit()
        return hltddb_tag

    @property
    def raw(self):
        return {'hltddb_pid': str(self.hltddb_pid)}
