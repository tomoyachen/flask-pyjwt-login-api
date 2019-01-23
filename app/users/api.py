from flask import jsonify, request
from app.users.model import Users
from app.auth.auths import Auth
from .. import common

def init_api(app):
    @app.route('/register', methods=['POST'])
    def register():
        """
        用户注册
        :return: json
        """
        email = request.form.get('email')
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        if username is None or username == "" or username == "null":
            return jsonify(common.falseReturn('', '账号不能为空!'))
        if password is None or password == "" or password == "null":
            return jsonify(common.falseReturn('', '密码不能为空!'))
        if not(username.isalnum()) or is_Chinese(username):
            return jsonify(common.falseReturn('', '账号只能是字母或数字组成!'))
        if not(password.isalnum()) or is_Chinese(username):
            return jsonify(common.falseReturn('', '密码只能是字母或数字组成!'))
        # 最后一条记录及其ID
        lastUserRecord = Users.query.order_by('-id').first()
        if (lastUserRecord is None):
            newRecordId = 1
        else:
            newRecordId = lastUserRecord.id + 1

        user = Users(id=None, email=email, username=username, password=Users.set_password(Users, password))
        if (Users.getUsername(Users, user.username)):
            return jsonify(common.falseReturn('', '用户已存在')) 
        else:
            Users.add(Users, user)
        userInfo = Users.get(Users, user.id)
        if userInfo:
            returnUser = {
                'id': userInfo.id,
                'username': userInfo.username,
                'email': userInfo.email,
                'login_time': userInfo.login_time
            }
            return jsonify(common.trueReturn(returnUser, "用户注册成功"))
        else:
            return jsonify(common.falseReturn('', '用户注册失败'))

    def is_Chinese(word):
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False
	
    @app.route('/login', methods=['POST'])
    def login():
        """
        用户登录
        :return: json
        """
        username = request.form.get('username')
        password = request.form.get('password')
        if (not username or not password):
            return jsonify(common.falseReturn('', '用户名和密码不能为空'))
        else:
            return Auth.authenticate(Auth, username, password)


    @app.route('/user', methods=['GET'])
    def get():
        """
        获取用户信息
        :return: json
        """
        result = Auth.identify(Auth, request)
        if (result['status'] and result['data']):
            user = Users.get(Users, result['data'])
            returnUser = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'login_time': user.login_time
            }
            result = common.trueReturn(returnUser, "请求成功")
        return jsonify(result)
