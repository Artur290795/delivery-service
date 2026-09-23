"""add initial parcel types

Revision ID: 3ddd4829c95d
Revises: f31bf444a86f
Create Date: 2026-09-21 18:09:08.880875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ddd4829c95d'
down_revision: Union[str, Sequence[str], None] = 'f31bf444a86f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    parcel_types = sa.table(
        "parcel_types",
        sa.column("name", sa.String()),
    )

    op.bulk_insert(
        parcel_types,
        [
            {"name": "clothes"},
            {"name": "electronics"},
            {"name": "other"},
        ],
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            """
            DELETE FROM parcel_types
            WHERE name IN ('clothes', 'electronics', 'other')
            """
        )
    )
