from app.controller import *
import pymysql
from werkzeug.routing import BaseConverter
from flask import jsonify, abort
import base64
import jwt
import datetime
from jinja2 import Template

dbs = {
    "api": {
        'host': 'localhost',
        'port': 3306,
        'database': 'supersql',
        'user': 'supersql',
        'password': 'bQDDCBx2EkbGfaHW'
    },
    "srf": {
        'host': 'localhost',
        'port': 3306,
        'database': 'small_red_flower',
        'user': 'small_red_flower',
        'password': 'Pxsk3xd47hmpAHf5'
    }
}


def connect_db(db_name):
    conn = pymysql.connect(
        host=dbs[db_name]["host"],  # 主机名（或IP地址）
        port=dbs[db_name]["port"],  # 端口号，默认为3306
        user=dbs[db_name]["user"],  # 用户名
        password=dbs[db_name]["password"],  # 密码
        charset='utf8mb4'  # 设置字符编码
    )
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    conn.select_db(dbs[db_name]["database"])
    return conn, cursor


def check_uri(path):
    conn, cur = connect_db("api")
    cur.execute(
        "SELECT * FROM api_config LEFT JOIN api_db_config"
        " ON api_config.api_db_id = api_db_config.db_id "
        "WHERE api_config.api_uri = '%s' " % path)
    api_info = cur.fetchone()
    # print(api_info)
    if api_info is None:
        return abort(400, description=jsonify({"msg": "api error or not exist"}))
    return api_info


def get_auth(auth_id):
    conn, cur = connect_db("api")
    cur.execute(
        "SELECT * FROM api_authentication where authentication_id = '%s'" % auth_id
    )
    api_info = cur.fetchone()
    if api_info is None:
        return abort(400, description=jsonify({"msg": "api auth error or not exist"}))
    return api_info


def connect_api_db(api_info):
    conn = pymysql.connect(
        host=api_info["db_host"],  # 主机名（或IP地址）
        port=api_info["db_port"],  # 端口号，默认为3306
        user=api_info["db_user"],  # 用户名
        password=api_info["db_password"],  # 密码
        charset='utf8mb4'  # 设置字符编码
    )
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    conn.select_db(api_info["db_name"])
    return conn, cursor


def create_jwt(payload, secretkey, algorithm):
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    return jwt.encode(payload, secretkey, algorithm=algorithm)


def parse_jwt(token, secretkey, algorithm):
    try:
        payload = jwt.decode(token, secretkey, algorithms=algorithm)
    except jwt.ExpiredSignatureError:
        abort(401, description=jsonify({"msg": "令牌过期"}))
    except jwt.InvalidTokenError:
        abort(401, description=jsonify({"msg": "非法令牌"}))
    return payload


class WildcardConverter(BaseConverter):
    regex = r'(|/.*?)'
    weight = 200


app.url_map.converters['wildcard'] = WildcardConverter


@app.route("/api/create/<int:id>", methods=["GET"])
def create(id):
    config = get_auth(id)
    return jsonify({"token": create_jwt({"test": "none"}
                                        , config['authentication_secretkey']
                                        , config['authentication_algorithm'])})


@app.route("/super<wildcard:path>", methods=["GET", "PUT", "POST", "DELETE"])
def all_api(path):
    data = check_uri(path)
    if request.method != data["api_method"]:
        return jsonify({"msg": "invalid"}), 404

    # 判断接口是否开启
    if data["api_on"] == 0:
        return jsonify({"msg": "The interface has been disabled"}), 405

    if data["api_is_use_auth"] == 1:
        token = request.headers.get("Authorization")
        auth_config = get_auth(data['api_auth_id'])
        parse_jwt(token, auth_config["authentication_secretkey"], auth_config['authentication_algorithm'])

    # Decode and parse the base64 encoded query parameters
    try:
        query = eval(base64.b64decode(data["api_query"]).decode("UTF-8"))
    except Exception as e:
        return jsonify({"msg": f"query decoding error {e}"}), 400

    conn, cur = connect_api_db(data)

    # Get query parameters
    p = request.args
    params = {}
    for q in query:
        value = p.get(q)
        if value is None:
            return jsonify({"msg": "missing parameter"}), 400
        params[q] = value

    # Get JSON body parameters
    try:
        body = request.get_json() or {}
    except Exception as e:
        body = {}

    var = {}

    if data["api_is_use_script"] == 1:
        try:
            code = base64.b64decode(data["api_script"]).decode("UTF-8")
            exec(eval(code), {"params": params, "body": body, "var": var})
        except Exception as e:
            return jsonify({"msg": f"script error {e}"}), 400

    try:
        sql_template = Template(data["api_sql"])
        sql = sql_template.render(params=params, body=body, var=var)
        # print(sql)
    except Exception as e:
        return jsonify({"msg": f"sql template error {e}"}), 400

    try:
        cur.execute(sql)
        conn.commit()
        res = cur.fetchall()
        res = res if res else []
    except Exception as e:
        return jsonify({"msg": f"exec sql error {e}"}), 400

    var["data"] = res

    if data["api_is_use_post_script"] == 1:
        try:
            post_code = base64.b64decode(data["api_post_script"]).decode("UTF-8")
            exec(eval(post_code), {"params": params, "body": body, "var": var})
        except Exception as e:
            return jsonify({"msg": f"post script error {e}"}), 400

    return jsonify(var["data"])
