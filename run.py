from web import create_app, connect_db


if __name__ == '__main__':

    app = create_app()
    connect_db(app)

    app.run(host='localhost', debug=True)
    # app.run()
