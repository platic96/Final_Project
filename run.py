import ssl
from flask import Flask
<<<<<<< HEAD
from views import main,login,talkBot
=======
from views import main, login, talkBot
>>>>>>> fe48297063478d88153e75b3baf0ff800e9614f3

app = Flask(__name__)

app.secret_key = 'Kjd7XuRjnwmHHMmaMHDjzNjUTjqwpFjHtw0C8Wjd'

# --------------------------------- [edit] ---------------------------------- #    
app.register_blueprint(main.bp)
app.register_blueprint(login.bp)
app.register_blueprint(talkBot.bp)
# --------------------------------------------------------------------------- #    

if __name__ == '__main__':
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(certfile='/usr/test/openssl-1.1.1k/private.crt',keyfile='/usr/test/openssl-1.1.1k/BitasBit.pem',password='1234')
    app.run(debug=False,host="0.0.0.0",port=443,ssl_context=ssl_context)
