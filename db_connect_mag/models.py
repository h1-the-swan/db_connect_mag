from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from .db_connect_mag_201710 import get_db_connection
db = get_db_connection()
db.metadata.reflect(extend_existing=True)
Base = declarative_base(db.engine)

from sqlalchemy import Column, Integer, BigInteger, Text, SmallInteger, ForeignKey

class Paper(Base):
    __tablename__ = 'Papers'
    __table_args__ = {'autoload': True}

    # id = Column('Paper_ID', BigInteger)
    _rank = relationship("Rank", uselist=False)
    _tree = relationship("Tree", uselist=False, backref='paper')
    _journal = relationship("Journal", uselist=False)
    _conference = relationship("ConferenceSeries", uselist=False)
    _paa = relationship("PaperAuthorAffiliation", backref='paper')

    @hybrid_property
    def EF(self):
        if self._rank is None:
            return None
        return self._rank.EF

    @hybrid_property
    def cl(self):
        if self._tree is None:
            return None
        return self._tree.cl

    @hybrid_property
    def cl_toplevel(self):
        if self._tree is None:
            return None
        return self._tree.toplevel

    @hybrid_property
    def journal_or_conference_name(self):
        if self._journal:
            return self._journal.Display_name
        if self._conference:
            return self._conference.Display_name
        return None

    @hybrid_property
    def journal_id(self):
        if self._journal is None:
            return None
        return self._journal.Journal_ID

    @hybrid_property
    def conference_id(self):
        if self._conference is None:
            return None
        return self._conference.Conference_series_ID

    @hybrid_property
    def author_ids(self):
        return [paa.Author_ID for paa in self._paa]

    @hybrid_property
    def author_names(self):
        names = []
        for paa in self._paa:
            name = paa.Author_name or 'UNKNOWN'
            names.append(name)
        return names

    # # methods to assist in pickling
    # # see https://docs.python.org/3/library/pickle.html#pickling-class-instances
    # def __getstate__(self):
    #     # Copy the object's state from self.__dict__ which contains
    #     # all our instance attributes. Always use the dict.copy()
    #     # method to avoid modifying the original state.
    #     state = self.__dict__.copy()


class Rank(Base):
    __tablename__ = 'rank'
    __table_args__ = {'autoload': True}

class Tree(Base):
    __tablename__ = 'tree'
    __table_args__ = {'autoload': True}

    # _cl_meta_tree = relationship("ClustersMetaTree", uselist=False, viewonly=True)
    # _cl_meta_tree = relationship("ClustersMetaTree", uselist=False, backref='tree')
    _cl_meta_tree = relationship("ClustersMetaTree", backref='tree_collection')

class Journal(Base):
    __tablename__ = 'Journals'
    __table_args__ = {'autoload': True}

class ConferenceSeries(Base):
    __tablename__ = 'ConferenceSeries'
    __table_args__ = {'autoload': True}

class PaperAuthorAffiliation(Base):
    __tablename__ = 'PaperAuthorAffiliations'
    __table_args__ = {'autoload': True}

class ClustersMetaTree(Base):
    __tablename__ = 'clusters_meta_tree'
    __table_args__ = {'autoload': True}

    @hybrid_property
    def all_papers(self):
        if not self.tree_collection:
            return []
        return [t.paper for t in self.tree_collection]

class ClusterToplevelLink(Base):
    __tablename__ = 'cluster_toplevel_linklist'
    __table_args__ = {'autoload': True}
    source_toplevel = Column('source_toplevel', BigInteger, ForeignKey('clusters_meta_tree.toplevel_in_tree', name='source_cl_meta'))
    target_toplevel = Column('target_toplevel', BigInteger, ForeignKey('clusters_meta_tree.toplevel_in_tree', name='target_cl_meta'))
    source_cl_meta = relationship('ClustersMetaTree', foreign_keys=[source_toplevel], backref='cls_meta_citing')
    target_cl_meta = relationship('ClustersMetaTree', foreign_keys=[target_toplevel], backref='cls_meta_cited')

# class PaperAuthorAffiliation(Base):
#     __tablename__ = 'PaperAuthorAffiliation'
#     # __mapper_args__ = {
#     #     'primary_key': ['Paper_ID', 'Author_ID']
#     # }
#
#     _Paper = relationship("Paper", uselist=False)

class PaperReference(Base):
    __tablename__ = 'PaperReferences'
    __table_args__ = {'autoload': True}
    # __table_args__ = {'extend_existing': True}

    Paper_ID = Column('Paper_ID', BigInteger, ForeignKey('Papers.Paper_ID', name='paper_citing'), primary_key=True)
    Paper_reference_ID = Column('Paper_reference_ID', BigInteger, ForeignKey('Papers.Paper_ID', name='paper_cited'), primary_key=True)

    paper_citing = relationship('Paper', foreign_keys=[Paper_ID], backref='paperrefs_citing')
    paper_cited = relationship('Paper', foreign_keys=[Paper_reference_ID], backref='paperrefs_cited')
    #
    # papers_citing = relationship('Paper', primaryjoin="PaperReference.Paper_ID==Paper.Paper_ID", backref='papers_citing', foreign_keys=[Paper_ID])
    # papers_cited = relationship('Paper', primaryjoin="PaperReference.Paper_reference_ID==Paper.Paper_ID", backref='papers_cited', foreign_keys=[Paper_reference_ID])

    # papers_citing = relationship('Paper', primaryjoin="PaperReference.Paper_ID==Paper.Paper_ID", backref='papers_citing')
    # papers_cited = relationship('Paper', primaryjoin="PaperReference.Paper_reference_ID==Paper.Paper_ID", backref='papers_cited')
#
# class PaperReference2(Base):
#     __tablename__ = 'PaperReferences_txt_snapshot'
#
#     Paper_ID = Column('Paper_ID', BigInteger, ForeignKey('Papers.Paper_ID'), primary_key=True)
#     Paper_reference_ID = Column('Paper_reference_ID', BigInteger, ForeignKey('Papers.Paper_ID'), primary_key=True)
#
#     papers_citing_2 = relationship('Paper', primaryjoin="PaperReference2.Paper_ID==Paper.Paper_ID", backref='papers_citing_2', foreign_keys=[Paper_ID])
#     papers_cited_2 = relationship('Paper', primaryjoin="PaperReference2.Paper_reference_ID==Paper.Paper_ID", backref='papers_cited_2', foreign_keys=[Paper_reference_ID])
#
#     # papers_citing_2 = relationship('Paper', primaryjoin="PaperReference2.Paper_ID==Paper.Paper_ID", backref='papers_citing_2')
#     # papers_cited_2 = relationship('Paper', primaryjoin="PaperReference2.Paper_reference_ID==Paper.Paper_ID", backref='papers_cited_2')
