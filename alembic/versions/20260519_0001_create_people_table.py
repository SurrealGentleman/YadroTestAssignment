"""create people table

Revision ID: 20260519_0001
Revises:
Create Date: 2026-05-19
"""

from alembic import op
import sqlalchemy as sa

revision = "20260519_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "people",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("gender", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("address", sa.Text(), nullable=False),
        sa.Column("raw_data", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_people_id"), "people", ["id"], unique=False)
    op.create_index(op.f("ix_people_gender"), "people", ["gender"], unique=False)
    op.create_index(op.f("ix_people_first_name"), "people", ["first_name"], unique=False)
    op.create_index(op.f("ix_people_last_name"), "people", ["last_name"], unique=False)
    op.create_index(op.f("ix_people_email"), "people", ["email"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_people_email"), table_name="people")
    op.drop_index(op.f("ix_people_last_name"), table_name="people")
    op.drop_index(op.f("ix_people_first_name"), table_name="people")
    op.drop_index(op.f("ix_people_gender"), table_name="people")
    op.drop_index(op.f("ix_people_id"), table_name="people")
    op.drop_table("people")
