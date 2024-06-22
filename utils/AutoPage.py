from utils.Result import *


def auto_page(p, s, query, schemas):
    if p < 1 or s < 1:
        return error(msg="Parameters must be greater than 0"), 400
    total_count = query.count()
    configs = query.offset((p - 1) * s).limit(s).all()
    result = {
        "total": total_count,
        "records": schemas.dump(configs)
    }
    return result
