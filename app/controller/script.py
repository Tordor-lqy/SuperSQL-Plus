from app.controller import *

api_script_schema = ApiScriptSchema()


@app.route('/api/script', methods=['POST'])
def create_script():
    data = request.json
    new_script = api_script_schema.load(data)
    db.session.add(new_script)
    db.session.commit()
    return api_script_schema.dump(new_script), 201


@app.route('/api/script/<int:id>', methods=['GET'])
def get_script(id):
    script = ApiScript.query.get_or_404(id)
    return api_script_schema.dump(script)


@app.route('/api/script/<int:id>', methods=['PUT'])
def update_script(id):
    script = ApiScript.query.get_or_404(id)
    data = request.json
    script = api_script_schema.load(data, instance=script, partial=True)
    db.session.commit()
    return api_script_schema.dump(script)


@app.route('/api/script/<int:id>', methods=['DELETE'])
def delete_script(id):
    script = ApiScript.query.get_or_404(id)
    db.session.delete(script)
    db.session.commit()
    return '', 204
