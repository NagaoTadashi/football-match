"""Add new schema changes

Revision ID: 4076f5d8fb61
Revises: 0432bd9d77dc
Create Date: 2024-11-02 08:18:20.943756

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4076f5d8fb61'
down_revision: Union[str, None] = '0432bd9d77dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
