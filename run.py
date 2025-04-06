from web import create_app, connect_db


app = create_app()


if __name__ == '__main__':

    connect_db(app)

    app.run()

