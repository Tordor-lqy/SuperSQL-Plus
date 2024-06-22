from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app import db


class ApiAuthentication(db.Model):
    __tablename__ = 'api_authentication'
    authentication_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='Primary Key')
    authentication_secretkey = db.Column(db.String(3000), nullable=False, comment='鉴权秘钥')
    authentication_algorithm = db.Column(db.String(200), nullable=False, comment='鉴权算法')
    authentication_name = db.Column(db.String(255), default='安全组', comment='鉴权组名称')


class ApiConfig(db.Model):
    __tablename__ = 'api_config'
    api_config_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='Primary Key')
    api_uri = db.Column(db.String(255), nullable=False)
    api_method = db.Column(db.String(30), nullable=False)
    api_db_id = db.Column(db.Integer, nullable=False)
    api_sql = db.Column(db.String(9000), nullable=False)
    api_query = db.Column(db.String(5000), default='W10=', comment='查询参数')
    api_is_use_body = db.Column(db.Integer, nullable=False, default=0, comment='是否使用body/json参数')
    api_script = db.Column(db.Text)
    api_is_use_script = db.Column(db.Integer, nullable=False, default=0, comment='是否启用前置脚本')
    api_on = db.Column(db.Integer, nullable=False, default=1, comment='是否开启')
    api_post_script = db.Column(db.Text, comment='后置脚本')
    api_is_use_post_script = db.Column(db.Integer, nullable=False, default=0, comment='是否开启后置脚本')
    api_is_use_auth = db.Column(db.Integer, nullable=False, default=0, comment='是否使用鉴权')
    api_auth_id = db.Column(db.Integer, comment='鉴权组ID')
    api_project_id = db.Column(db.Integer, nullable=False)
    api_name = db.Column(db.String(255), nullable=False)


class ApiDbConfig(db.Model):
    __tablename__ = 'api_db_config'
    db_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='Primary Key')
    db_type = db.Column(db.String(50), nullable=False)
    db_name = db.Column(db.String(255), nullable=False)
    db_password = db.Column(db.String(500), nullable=False)
    db_host = db.Column(db.String(500), nullable=False)
    db_port = db.Column(db.Integer, nullable=False)
    db_user = db.Column(db.String(255), nullable=False)


class ApiLog(db.Model):
    __tablename__ = 'api_log'
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='Primary Key')
    log_api_uri = db.Column(db.String(1000), nullable=False, comment='API URI')
    log_request_ip = db.Column(db.String(1000), nullable=False, comment='Request IP')
    log_create_time = db.Column(db.DateTime, comment='Create Time')


class ApiScript(db.Model):
    __tablename__ = 'api_script'
    script_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='Primary Key')
    script_name = db.Column(db.String(255), nullable=False, comment='Script Name')
    script_content = db.Column(db.Text, nullable=False, comment='Script Content')
    script_number_of_run = db.Column(db.Integer, nullable=False, comment='Number of Run')


class ApiProject(db.Model):
    __tablename__ = 'api_project'
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(255), nullable=False, comment='Project')
    project_identifier = db.Column(db.String, nullable=False, comment='identifier')


class ApiAdmin(db.Model):
    __tablename__ = 'api_admin'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_name = db.Column(db.String(255), nullable=False)
    admin_password = db.Column(db.String(255), nullable=False)


# Marshmallow Schemas
class ApiAuthenticationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ApiAuthentication
        load_instance = True


class ApiConfigSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ApiConfig
        load_instance = True


class ApiDbConfigSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ApiDbConfig
        load_instance = True


class ApiLogSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ApiLog
        load_instance = True


class ApiScriptSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ApiScript
        load_instance = True


class ApiProjectSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ApiProject
        load_instance = True


class ApiAdminSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ApiAdmin
        load_instance = True
