"""add m2m assiciation between roles and role_permissions table

Revision ID: 15a38b3490c6
Revises: e78f50b8f6ee
Create Date: 2024-12-11 11:25:50.152520

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "15a38b3490c6"
down_revision: Union[str, None] = "e78f50b8f6ee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "association_roles_role_permissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.UUID(), nullable=False),
        sa.Column("role_permissions_id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["role_permissions_id"],
            ["role_permissions.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "role_id",
            "role_permissions_id",
            name="idx_unique_roles_role_permissions",
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("association_roles_role_permissions")
    # ### end Alembic commands ###
