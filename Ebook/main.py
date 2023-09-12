from app import *
from basicroutes import *
from authentication import *

with app.app_context():
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    app.run(debug = True)