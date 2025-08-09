"""add default parcel types

Revision ID: 05db6980d7a0
Revises: b7d301d3b5c5
Create Date: 2025-07-28 12:56:17.450628

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "05db6980d7a0"
down_revision: Union[str, Sequence[str], None] = "b7d301d3b5c5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(
        sa.table(
            "parcel_types",
            sa.column("id", sa.Integer),
            sa.column("name", sa.String),
        ),
        [
            {"name": "Одежда"},
            {"name": "Электроника"},
            {"name": "Разное"},
        ],
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM parcel_types WHERE name IN ('Одежда', 'Электроника', 'Разное')"
    )
