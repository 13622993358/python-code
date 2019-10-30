from flask import Blueprint

api =Blueprint("api",__name__)

from . import user,upload_img,attribute,site,banner,role,beast,college,group