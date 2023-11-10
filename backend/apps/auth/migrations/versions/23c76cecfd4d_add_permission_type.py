"""add_permission_type

Revision ID: 23c76cecfd4d
Revises: 71f7df0414f9
Create Date: 2023-07-21 10:40:00.171767

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "23c76cecfd4d"
down_revision = "71f7df0414f9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "permissions", sa.Column("type", sa.String(length=255), nullable=False)
    )
    op.drop_constraint(
        "unique_together_role_id_user_id", "users_permissions", type_="unique"
    )
    op.create_unique_constraint(
        "unique_together_permission_id_user_id",
        "users_permissions",
        ["permission_id", "user_id"],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "unique_together_permission_id_user_id", "users_permissions", type_="unique"
    )
    op.create_unique_constraint(
        "unique_together_role_id_user_id",
        "users_permissions",
        ["permission_id", "user_id"],
    )
    op.drop_column("permissions", "type")
    # ### end Alembic commands ###