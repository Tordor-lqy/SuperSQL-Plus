import time


def log(msg):
    print(f"[{time.asctime(time.localtime())}]:{msg}")


def success(code=1, data=None, msg="成功"):
    return {
        "code": code,
        "msg": msg,
        "data": data
    }


def error(code=-1, data=None, msg="错误"):
    return {
        "code": code,
        "msg": msg,
        "data": data
    }
