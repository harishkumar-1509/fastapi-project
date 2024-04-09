"""create secondary phone number column for the user

Revision ID: 93213721e790
Revises: 
Create Date: 2024-04-09 18:20:02.656263

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '93213721e790'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('secondary_phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    pass
