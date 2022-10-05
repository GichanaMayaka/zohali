"""create maintenance table

Revision ID: 47a88d65f603
Revises: 
Create Date: 2022-10-01 22:54:30.548773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47a88d65f603'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("maintenance_schedule",
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("region", sa.String(), nullable=True),
                    sa.Column("area", sa.String(), nullable=True),
                    sa.Column("places", sa.String(), nullable=True),
                    sa.Column("time", sa.String(), nullable=True),
                    sa.Column("date", sa.TIMESTAMP(
                        timezone=True), nullable=True),
                    sa.Column("county", sa.String(), nullable=True),
                    sa.Column("start_time", sa.String(), nullable=True),
                    sa.Column("end_time", sa.String(), nullable=True),
                    sa.Column("file_path", sa.String(), nullable=True),
                    )


def downgrade() -> None:
    op.drop_table("maintenance_schedule")
