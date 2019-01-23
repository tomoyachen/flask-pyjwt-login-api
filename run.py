#coding=utf8

from app import create_app
import pymysql
pymysql.install_as_MySQLdb()

app = create_app('app.config')
app.config['JSON_AS_ASCII'] = False #中文

if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])

