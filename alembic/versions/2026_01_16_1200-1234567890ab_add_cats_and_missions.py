"""Add cats and missions tables

Revision ID: 1234567890ab
Revises: e16b33721b64
Create Date: 2026-01-16 12:00:00.000000+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1234567890ab"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # spy_cat table
    op.create_table(
        "spy_cat",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("years_of_experience", sa.Integer(), nullable=False),
        sa.Column("breed", sa.String(), nullable=False),
        sa.Column("salary", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # mission table
    op.create_table(
        "mission",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cat_id", sa.Integer(), nullable=True),
        sa.Column("is_complete", sa.Boolean(), nullable=False, default=False),
        sa.ForeignKeyConstraint(["cat_id"], ["spy_cat.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # target table
    op.create_table(
        "target",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("mission_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("country", sa.String(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("is_complete", sa.Boolean(), nullable=False, default=False),
        sa.ForeignKeyConstraint(["mission_id"], ["mission.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("target")
    op.drop_table("mission")
    op.drop_table("spy_cat")
