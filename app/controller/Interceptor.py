from app.controller import *
from utils import authorization


@app.before_request
def before_request():
    # 排除路径
    path = request.path
    expath = ["/super", "/api/login" , "/"]

    safe = False
    for e in expath:
        if e == path[:len(e)]:
            safe = True

    if request.method == "OPTIONS":
        safe = True
    # 处理不安全路径
    if not safe:
        token = request.headers.get('Authorization')
        status, msg = authorization.parse_jwt(token)
        if not status:
            return error(msg=msg), 401
