"""grid_providers_table

Revision ID: 0010
Revises: 0009
Create Date: 2023-10-20 09:43:23.358144

"""
import csv
import os
from uuid import uuid4

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '0010'
down_revision = '0009'
branch_labels = None
depends_on = None

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

data = []
with open(os.path.join(BASE_DIR, "NorwayELPrices.csv")) as csv_file:
    reader = csv.reader(csv_file)
    next(reader, None)
    for row in reader:
        data.append(dict(
            id=str(uuid4()),
            postnummer=row[0],
            region=row[1],
            name=row[2],
            daily_rate=row[3],
            nightly_rate=row[4]
        ))


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    grid_providers = op.create_table('grid_providers',
                                     sa.Column('postnummer', sa.String(), nullable=False),
                                     sa.Column('region', sa.String(), nullable=False),
                                     sa.Column('name', sa.String(), nullable=False),
                                     sa.Column('daily_rate', sa.Numeric(precision=2, scale=2), nullable=True),
                                     sa.Column('nightly_rate', sa.Numeric(precision=2, scale=2), nullable=True),
                                     sa.Column('id', sa.String(), nullable=False),
                                     sa.Column('created_at', sa.DateTime(), nullable=True),
                                     sa.Column('updated_at', sa.DateTime(), nullable=True),
                                     sa.Column('is_active', sa.Boolean(), nullable=True),
                                     sa.PrimaryKeyConstraint('id'),
                                     sa.UniqueConstraint('postnummer')
                                     )
    op.create_index(op.f('ix_grid_providers_id'), 'grid_providers', ['id'], unique=True)
    op.add_column('garages', sa.Column('grid_provider_id', sa.String(), nullable=False))
    op.create_foreign_key("garages_grid_provider_id_fkey", 'garages', 'grid_providers', ['grid_provider_id'], ['id'])

    op.bulk_insert(grid_providers, data)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("garages_grid_provider_id_fkey", 'garages', type_='foreignkey')
    op.drop_column('garages', 'grid_provider_id')
    op.drop_index(op.f('ix_grid_providers_id'), table_name='grid_providers')
    op.drop_table('grid_providers')
    # ### end Alembic commands ###