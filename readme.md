>>> from app import db
>>> from app.utils import db
>>> from app import create_app
>>> from app.models import *
>>> app = create_app()
>>> app.app_context().push()
>>> db.create_all()