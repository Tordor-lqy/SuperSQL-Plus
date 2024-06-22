from app.controller import *

api_db_config_schema = ApiDbConfigSchema()
api_db_config_schemas = ApiDbConfigSchema(many=True)


@app.route('/api/db_config', methods=['POST'])
def create_db_config():
    data = request.json
    sess = scoped_session(sessionmaker(bind=engine))
    new_db_config = api_db_config_schema.load(data, session=sess)
    db.session.add(new_db_config)
    db.session.commit()
    return api_db_config_schema.dump(new_db_config), 201


@app.route('/api/db_config/<int:id>', methods=['GET'])
def get_db_config(id):
    db_config = ApiDbConfig.query.get_or_404(id)
    return success(data=api_db_config_schema.dump(db_config))


@app.route('/api/db_config/page', methods=['GET'])
def get_db_page():
    args = request.args
    try:
        p = int(args.get('p', 1))
        s = int(args.get('s', 10))
    except ValueError:
        return error(msg="Invalid parameters"), 400

    result = auto_page(p, s, ApiDbConfig.query, api_db_config_schemas)
    return success(data=result), 200


@app.route('/api/db_config/list', methods=['GET'])
def get_db_config_list():
    return success(data=api_db_config_schemas.dump(ApiDbConfig.query.all()))


@app.route('/api/db_config/<int:id>', methods=['PUT'])
def update_db_config(id):
    db_config = ApiDbConfig.query.get_or_404(id)
    data = request.json
    sess = scoped_session(sessionmaker(bind=engine))
    db_config = api_db_config_schema.load(data, session=sess, instance=db_config, partial=True)
    db.session.commit()
    return api_db_config_schema.dump(db_config)


@app.route('/api/db_config/<int:id>', methods=['DELETE'])
def delete_db_config(id):
    db_config = ApiDbConfig.query.get_or_404(id)
    db.session.delete(db_config)
    db.session.commit()
    return success(data=db_config), 204
