from app.controller import *


api_config_schema = ApiConfigSchema()
api_config_schemas = ApiConfigSchema(many=True)


@app.route('/api/config', methods=['POST'])
def create_config():
    data = request.json
    sess = scoped_session(sessionmaker(bind=engine))
    new_config = api_config_schema.load(data, session=sess)
    db.session.add(new_config)
    db.session.commit()
    return success(data=api_config_schema.dump(new_config)), 201


@app.route('/api/config/<int:id>', methods=['GET'])
def get_config(id):
    config = ApiConfig.query.get_or_404(id)
    return success(data=api_config_schema.dump(config)), 201


@app.route('/api/config/page', methods=['GET'])
def get_config_page():
    args = request.args
    try:
        p = int(args.get('p', 1))
        s = int(args.get('s', 10))
    except ValueError:
        return error(msg="Invalid parameters"), 400

    result = auto_page(p, s, ApiConfig.query, api_config_schemas)
    return success(data=result), 200


@app.route('/api/config/page/<int:project_id>', methods=['GET'])
def get_config_by_project_id(project_id):
    args = request.args
    try:
        p = int(args.get('p', 1))
        s = int(args.get('s', 10))
    except ValueError:
        return error(msg="Invalid parameters"), 400
    query = ApiConfig.query.filter_by(api_project_id=project_id)
    result = auto_page(p, s, query, api_config_schemas)
    return success(data=result), 200


@app.route('/api/config/<int:id>', methods=['PUT'])
def update_config(id):
    config = ApiConfig.query.get_or_404(id)
    data = request.json
    sess = scoped_session(sessionmaker(bind=engine))
    config = api_config_schema.load(data, session=sess, instance=config, partial=True)
    db.session.commit()
    return success(data=api_config_schema.dump(config)), 201


@app.route('/api/config/<int:id>', methods=['DELETE'])
def delete_config(id):
    config = ApiConfig.query.get_or_404(id)
    db.session.delete(config)
    db.session.commit()
    return success(data=config), 204
