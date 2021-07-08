import ssl
from app import app


if __name__ == '__main__':
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(certfile='/usr/test/openssl-1.1.1k/private.crt',keyfile='/usr/test/openssl-1.1.1k/bitasbit.key',password='1234')
    app.run(host='0.0.0.0',port=5000,ssl_context=ssl_context)
