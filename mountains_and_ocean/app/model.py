from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class BaseModel(object):
    '''创建及更新时间'''
    create_time = db.Column(db.DateTime,default=datetime.now)
    update_time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)

class User(BaseModel,db.Model):
    '''用户模型类'''
    __tablename__ = "user"

    id = db.Column(db.Integer,primary_key=True)
    phone = db.Column(db.String(11),unique=True,nullable=False)
    password_hash = db.Column(db.String(128),nullable=False)
    name = db.Column(db.String(30),default='')
    head_portrait = db.Column(db.String(280),default='')
    intro = db.Column(db.String(200),default='')
    level = db.Column(db.Enum("1","2","3","4","5"),default="1")

    @property
    def password(self):
        '''读取密码时触发'''
        return AttributeError("无法读取密码属性")

    @password.setter
    def password(self,val):
        '''设置密码时加密'''
        self.password_hash = generate_password_hash(val)

    def check_password(self,val):
        '''校验密码是否正确'''
        return check_password_hash(self.password_hash,val)

class Banner(BaseModel,db.Model):
    '''轮播图模型类'''
    __tablename__ = "banner"
    id = db.Column(db.Integer,primary_key=True)
    image = db.Column(db.String(280),nullable=False)
    link_url = db.Column(db.String(280),default="")

class Attribute(BaseModel,db.Model):
    '''属性模型类'''
    __tablename__ = "attribute"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10),nullable=False,unique=True)
    image = db.Column(db.String(280), nullable=False)
    intro = db.Column(db.String(200),default='')
    role = db.relationship("Role")
    beast = db.relationship("Beast")

    def getSelect(self):
        select = {
            "value":self.id,
            "label":self.name,
        }
        return select

class Site(BaseModel,db.Model):
    '''地区模型类'''
    __tablename__ = "site"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(25),nullable=False,unique=True)
    image = db.Column(db.String(280),nullable=False)
    intro = db.Column(db.String(200),default="")
    role = db.relationship("Role")
    beast = db.relationship("Beast")

    def getSelect(self):
        select = {
            "value":self.id,
            "label":self.name
        }
        return select

class Role(BaseModel,db.Model):
    '''角色模型类'''
    __tablename__ = 'role'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    head_portrait = db.Column(db.String(280),nullable=False)
    gender = db.Column(db.Enum("0","1"),default="0")
    age = db.Column(db.Integer,default=18)
    attribute = db.Column(db.Integer,db.ForeignKey("attribute.id"),nullable=False)
    site = db.Column(db.Integer,db.ForeignKey("site.id"),nullable=False)
    intro = db.Column(db.String(680),default="")
    image_list = db.Column(db.String(280*4),default="")#最多4张图片
    college = db.Column(db.Integer,db.ForeignKey("college.id"))
    group = db.Column(db.Integer, db.ForeignKey("group.id"))

    def getAttr(id):
        attr = Attribute.query.get(id)
        return {
            "id": attr.id,
            "name": attr.name,
            "image": attr.image
        }

    def getSite(id):
        site = Site.query.get(id)
        return {
            "id":site.id,
            "name":site.name,
            "image":site.image
        }

class Beast(BaseModel,db.Model):
    __tablename__ = "beast"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    head_portrait = db.Column(db.String(280), nullable=False)
    attribute = db.Column(db.Integer, db.ForeignKey("attribute.id"), nullable=False)
    site = db.Column(db.Integer, db.ForeignKey("site.id"), nullable=False)
    intro = db.Column(db.String(680), default="")
    image_list = db.Column(db.String(280 * 4), default="")  # 最多4张图片

    def getAttr(id):
        attr = Attribute.query.get(id)
        return {
            "id":attr.id,
            "name":attr.name,
            "image":attr.image
        }

    def getSite(id):
        site = Site.query.get(id)
        return {
            "id":site.id,
            "name":site.name,
            "image":site.image
        }

class College(BaseModel,db.Model):
    __tablename__ = "college"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False,unique=True)
    image = db.Column(db.String(280),nullable=False)
    site = db.Column(db.Integer,db.ForeignKey("site.id"),nullable=False)
    intro = db.Column(db.String(680),default='')
    level = db.Column(db.Enum("初级","二级","一级","Z级"),default="初级")
    role = db.relationship("Role")

    def getSelect(self):
        info = {
            "value":self.id,
            "label":self.name
        }
        return info

class Group(BaseModel,db.Model):
    __tablename__ = "group"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    image = db.Column(db.String(280), nullable=False)
    site = db.Column(db.Integer, db.ForeignKey("site.id"), nullable=False)
    intro = db.Column(db.String(680), default='')
    level = db.Column(db.Enum("初级", "二级", "一级", "Z级"), default="初级")
    role = db.relationship("Role")

    def getSelect(self):
        info = {
            "value":self.id,
            "label":self.name
        }
        return info