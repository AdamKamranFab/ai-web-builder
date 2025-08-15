import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    __bind_key__ = "ai_web_builder"

    created_at = sa.Column(sa.types.TIMESTAMP(), server_default=sa.func.now())
    updated_at = sa.Column(
        sa.types.TIMESTAMP(), server_default=sa.func.now(), onupdate=sa.func.current_timestamp()
    )


class AuditTrailModel(BaseModel):
    __abstract__ = True

    created_by = sa.Column(sa.String(), nullable=True)
    updated_by = sa.Column(sa.String(), nullable=True)


class SoftDeleteModel(AuditTrailModel):
    __abstract__ = True

    deleted_at = sa.Column(sa.types.TIMESTAMP(), nullable=True)
    deleted_by = sa.Column(sa.String(), nullable=True)
    is_deleted = sa.Column(sa.Boolean(), nullable=False, server_default="0")


class Model(BaseModel):
    __abstract__ = True

    is_active = sa.Column(sa.Boolean(), nullable=False, server_default="1")
    is_deleted = sa.Column(sa.Boolean(), nullable=False, server_default="0")


class Users(BaseModel):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer(), nullable=False, autoincrement=True, primary_key=True)
    email = sa.Column(sa.String(), nullable=False)
    password = sa.Column(sa.String(), nullable=False)
    first_name = sa.Column(sa.String(), nullable=False)
    last_name = sa.Column(sa.String(), nullable=True)
    bio = sa.Column(sa.String(), nullable=True)
    expertise = sa.Column(sa.String(), nullable=True)
    stack = sa.Column(sa.String(), nullable=True)
    image_url = sa.Column(sa.String(), nullable=True)
    experience = sa.Column(sa.String(), nullable=True)


class UserKeys(BaseModel):
    __tablename__ = 'user_keys'

    id = sa.Column(sa.Integer(), nullable=False, autoincrement=True, primary_key=True)
    user_id = sa.Column(sa.Integer(), sa.ForeignKey('users.id'), nullable=False)
    otp = sa.Column(sa.String(), nullable=False)


class Project(BaseModel):
    __tablename__ = 'projects'

    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True, nullable=False)
    name = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.String(), nullable=False)
    deadline = sa.Column(sa.String(), nullable=False)
    status = sa.Column(sa.String(), nullable=False)
    media_img_url = sa.Column(sa.String(), nullable=False)
    requested_by = sa.Column(sa.String(), nullable=True)


class Payments(BaseModel):
    __tablename__ = 'payments'

    id = sa.Column(sa.Integer(), autoincrement=True, primary_key=True, nullable=False)
    project_id = sa.Column(sa.Integer(), sa.ForeignKey('projects.id'), nullable=False)
    name = sa.Column(sa.String(), nullable=False)
    payment_date = sa.Column(sa.DateTime(), nullable=False)
    payment_status = sa.Column(sa.String(), nullable=False)
    project_status = sa.Column(sa.String(), nullable=False)


class ClientReviews(BaseModel):
    __tablename__ = 'client_feedback'

    id = sa.Column(sa.Integer(), autoincrement=True, nullable=False, primary_key=True)
    client_name = sa.Column(sa.String(), nullable=False)
    project_name = sa.Column(sa.String(), nullable=False)
    feedback_summary = sa.Column(sa.String(), nullable=False)
    date_submission = sa.Column(sa.DateTime(), nullable=False)


class ServicePlans(BaseModel):
    __tablename__ = 'service_plans'

    id = sa.Column(sa.Integer(), autoincrement=True, nullable=False, primary_key=True)
    plan_name = sa.Column(sa.String(), nullable=False)
    price = sa.Column(sa.Integer(), nullable=False)
    delivery_time = sa.Column(sa.String(), nullable=False)
    revisions = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.String(), nullable=False)
    features = sa.Column(sa.String(), nullable=False)


class Developers(BaseModel):
    __tablename__ = 'developers'

    id = sa.Column(sa.Integer(), autoincrement=True, nullable=False, primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    tech_stack = sa.Column(sa.String(), nullable=False)
    github_status = sa.Column(sa.String(), nullable=False)
    joined_on = sa.Column(sa.DateTime(), nullable=False)
    active_projects = sa.Column(sa.Integer(), nullable=False)


class Subscriptions(BaseModel):
    __tablename__ = 'subscriptions'

    id = sa.Column(sa.Integer(), autoincrement=True, nullable=False, primary_key=True)
    user_id = sa.Column(sa.Integer(), sa.ForeignKey('users.id'), nullable=False)
    user_name = sa.Column(sa.String(), nullable=False)
    plan_name = sa.Column(sa.String(), nullable=False)
    start_date = sa.Column(sa.DateTime(), nullable=False)
    expiry_date = sa.Column(sa.DateTime(), nullable=False)
    amount = sa.Column(sa.Integer(), nullable=False)
    status = sa.Column(sa.String(), nullable=False)


class Roles(BaseModel):
    __tablename__ = 'roles'

    id = sa.Column(sa.Integer(), autoincrement=True, nullable=False, primary_key=True)
    name = sa.Column(sa.String(), nullable=False)


class Groups(BaseModel):
    __tablename__ = 'groups'

    id = sa.Column(sa.Integer(), autoincrement=True, nullable=False, primary_key=True)
    name = sa.Column(sa.String(), nullable=False)


class Permissions(BaseModel):
    __tablename__ = 'permissions'

    id = sa.Column(sa.Integer(), autoincrement=True, nullable=False, primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    type = sa.Column(sa.String(), nullable=False)


class UserRoles(BaseModel):
    __tablename__ = 'user_roles'

    id = sa.Column(sa.Integer(), autoincrement=True, nullable=False, primary_key=True)
    user_id = sa.Column(sa.Integer(), sa.ForeignKey('users.id'), nullable=False)
    role_id = sa.Column(sa.Integer(), sa.ForeignKey('roles.id'), nullable=False)


class RoleGroups(BaseModel):
    __tablename__ = 'role_groups'

    id = sa.Column(sa.Integer(), autoincrement=True, nullable=False, primary_key=True)
    group_id = sa.Column(sa.Integer(), sa.ForeignKey('users.id'), nullable=False)
    role_id = sa.Column(sa.Integer(), sa.ForeignKey('roles.id'), nullable=False)


class GroupPermissions(BaseModel):
    __tablename__ = 'group_permissions'

    id = sa.Column(sa.Integer(), autoincrement=True, nullable=False, primary_key=True)
    group_id = sa.Column(sa.Integer(), sa.ForeignKey('users.id'), nullable=False)
    permission_id = sa.Column(sa.Integer(), sa.ForeignKey('roles.id'), nullable=False)
