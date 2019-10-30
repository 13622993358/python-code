from app import createApp,db
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from flask_cors import CORS

app = createApp("product")

manage = Manager(app)
Migrate(app,db)
manage.add_command('db',MigrateCommand)

CORS(app,supports_credentials=True)

if __name__ == '__main__':
    manage.run()