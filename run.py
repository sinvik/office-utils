import os.path

from web import create_app, connect_db


if __name__ == '__main__':

    app = create_app()
    connect_db(app)

    CERT_PATH = os.path.join(os.path.dirname(__file__), os.path.pardir, 'certs')
    print(CERT_PATH)

    #app.run(host='localhost', debug=True)
    app.run()
