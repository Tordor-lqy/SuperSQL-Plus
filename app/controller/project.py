from app.controller import *

api_project_schema = ApiProjectSchema()
api_project_schemas = ApiProjectSchema(many=True)


@app.route('/api/project', methods=['POST'])
def create_project():
    data = request.json
    new_project = ApiProject(
        project_name=data['project_name'],
        project_identifier=data['project_identifier']
    )
    db.session.add(new_project)
    db.session.commit()
    return success(data=api_project_schema.dump(new_project)), 201


@app.route("/api/project", methods=['PUT'])
def update_project():
    data = request.json
    project = ApiProject.query.filter_by(project_id=data['project_id']).first()
    project.project_name = data['project_name']
    project.project_identifier = data['project_identifier']
    # 更新
    db.session.add(project)
    db.session.commit()
    return success(data=api_project_schema.dump(project)), 201


@app.route('/api/project/page', methods=['GET'])
def get_projects_page():
    args = request.args
    try:
        p = int(args.get('p', 1))
        s = int(args.get('s', 10))
    except ValueError:
        return error(msg="Invalid parameters"), 400

    result = auto_page(p, s, ApiProject.query, api_project_schemas)
    return success(data=result), 200


@app.route('/api/project/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = ApiProject.query.get_or_404(project_id)
    return success(data=api_project_schema.dump(project)), 201
