try:
    from models import db
except:
    from .models import db

try:
    from __init__ import app
except:
    from .__init__ import app

try:
    from user_profile import user_profile
except:
    from .user_profile import user_profile

try:
    from course import course
except:
    from .course import course

try:
    from projects import projects
except:
    from .projects import projects

try:
    from admin import admin
except:
    from .admin import admin

db.init_app(app)
app.register_blueprint(user_profile)
app.register_blueprint(course)
app.register_blueprint(projects)
app.register_blueprint(admin)

if __name__ == '__main__':
    app.run('localhost', 6969)