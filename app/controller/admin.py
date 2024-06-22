from app.controller import *
from utils import authorization

api_admin_schema = ApiAdminSchema()
api_admin_schemas = ApiAdminSchema(many=True)


@app.route("/api/login", methods=["POST"])
def admin_login():
    body = request.get_json()
    admin = ApiAdmin.query.filter_by(admin_name=body["admin_name"]).first()
    if not admin:
        return error(msg="没有这个管理员")
    if admin.admin_password != body["admin_password"]:
        return error(msg="用户名或密码错误")
    res = api_admin_schema.dump(admin)
    res["admin_password"] = "******"
    res["token"] = authorization.create_jwt(res)
    return success(data=res)
