from app.controller import *

api_log_schema = ApiLogSchema()


@app.route('/api/log', methods=['POST'])
def create_log():
    data = request.json
    new_log = api_log_schema.load(data)
    db.session.add(new_log)
    db.session.commit()
    return api_log_schema.dump(new_log), 201


@app.route('/api/log/<int:id>', methods=['GET'])
def get_log(id):
    log = ApiLog.query.get_or_404(id)
    return api_log_schema.dump(log)


@app.route('/api/log/<int:id>', methods=['PUT'])
def update_log(id):
    log = ApiLog.query.get_or_404(id)
    data = request.json
    log = api_log_schema.load(data, instance=log, partial=True)
    db.session.commit()
    return api_log_schema.dump(log)


@app.route('/api/log/<int:id>', methods=['DELETE'])
def delete_log(id):
    log = ApiLog.query.get_or_404(id)
    db.session.delete(log)
    db.session.commit()
    return '', 204
