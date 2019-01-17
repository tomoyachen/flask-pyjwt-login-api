from app import create_app
import pymysql
pymysql.install_as_MySQLdb()

app = create_app('app.config')

if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])

