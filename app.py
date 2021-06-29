from flask import Flask
from views import main
    
app = Flask(__name__)

# --------------------------------- [edit] ---------------------------------- #    
app.register_blueprint(main.bp)
# --------------------------------------------------------------------------- #    
