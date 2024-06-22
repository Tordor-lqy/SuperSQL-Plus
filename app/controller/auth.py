from app.controller import *

api_authentication_schema = ApiAuthenticationSchema()
api_authentication_schemas = ApiAuthenticationSchema(many=True)


@app.route('/api/authentication/<int:id>', methods=['GET'])
def get_authentication(id):
    auth = ApiAuthentication.query.get_or_404(id)
    return api_authentication_schema.dump(auth)


@app.route('/api/authentication', methods=['POST'])
def create_authentication():
    data = request.json
    sess = scoped_session(sessionmaker(bind=engine))
    new_auth = api_authentication_schema.load(data, session=sess)
    db.session.add(new_auth)
    db.session.commit()
    return api_authentication_schema.dump(new_auth), 201


# Update (U)
@app.route('/api/authentication/<int:id>', methods=['PUT'])
def update_authentication(id):
    auth = ApiAuthentication.query.get_or_404(id)
    data = request.json
    sess = scoped_session(sessionmaker(bind=engine))
    auth = api_authentication_schema.load(data, session=sess, instance=auth, partial=True)
    db.session.commit()
    return api_authentication_schema.dump(auth)


@app.route('/api/authentication/page', methods=['GET'])
def get_authentication_page():
    args = request.args
    try:
        p = int(args.get('p', 1))
        s = int(args.get('s', 10))
    except ValueError:
        return error(msg="Invalid parameters"), 400
    query = ApiAuthentication.query
    result = auto_page(p, s, query, api_authentication_schemas)
    return success(data=result), 200


@app.route("/api/authentication/list", methods=['GET'])
def get_authentication_list():
    return success(data=api_authentication_schemas.dump(ApiAuthentication.query.all())), 200


# Delete (D)
@app.route('/api/authentication/<int:id>', methods=['DELETE'])
def delete_authentication(id):
    auth = ApiAuthentication.query.get_or_404(id)
    db.session.delete(auth)
    db.session.commit()
    return success(data=auth), 204
