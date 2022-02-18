from app import app, db
from app.models import *
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager,Shell,Server



# Creating app instance

manager = Manager(app)
manager.add_command('server',Server)
migrate = Migrate(app,db)

manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db)

if __name__ == '__main__':
    # manager.run()
    app.run()