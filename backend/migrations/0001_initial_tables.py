"""initial_tables

Revision ID: 0001
Revises: 
Create Date: 2023-09-18 13:49:21.412422

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.schema import Sequence, CreateSequence

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(CreateSequence(Sequence('transaction_id_seq')))
    op.create_table('drivers',
                    sa.Column('email', sa.String(length=48), nullable=False),
                    sa.Column('first_name', sa.String(length=24), nullable=False),
                    sa.Column('last_name', sa.String(length=24), nullable=False),
                    sa.Column('address', sa.String(length=48), nullable=False),
                    sa.Column('billing_requisites', sa.JSON(), nullable=True),
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('is_active', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    op.create_index(op.f('ix_drivers_id'), 'drivers', ['id'], unique=True)
    op.create_table('transactions',
                    sa.Column('driver', sa.String(), nullable=False),
                    sa.Column('meter_start', sa.Integer(), nullable=False),
                    sa.Column('meter_stop', sa.Integer(), nullable=True),
                    sa.Column('charge_point', sa.String(), nullable=False),
                    sa.Column('transaction_id', sa.Integer(), server_default=sa.text("nextval('transaction_id_seq')"),
                              nullable=True),
                    sa.Column('status',
                              sa.Enum('in_progress', 'pending', 'completed', 'faulted', name='transactionstatus'),
                              nullable=True),
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('is_active', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_transactions_id'), 'transactions', ['id'], unique=True)
    op.create_table('charge_points',
                    sa.Column('description', sa.String(length=124), nullable=True),
                    sa.Column('status', sa.Enum('available', 'preparing', 'charging', 'suspended_evse', 'suspended_ev',
                                                'finishing', 'reserved', 'unavailable', 'faulted',
                                                name='chargepointstatus'), nullable=True),
                    sa.Column('manufacturer', sa.String(), nullable=False),
                    sa.Column('serial_number', sa.String(), nullable=False),
                    sa.Column('location', sa.String(), nullable=True),
                    sa.Column('model', sa.String(), nullable=False),
                    sa.Column('connectors', sa.ARRAY(sa.JSON()), nullable=True),
                    sa.Column('driver_id', sa.String(), nullable=True),
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('is_active', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['driver_id'], ['drivers.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('serial_number')
                    )
    op.create_index(op.f('ix_charge_points_id'), 'charge_points', ['id'], unique=True)
    op.create_index(op.f('ix_charge_points_status'), 'charge_points', ['status'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_charge_points_status'), table_name='charge_points')
    op.drop_index(op.f('ix_charge_points_id'), table_name='charge_points')
    op.drop_table('charge_points')
    op.drop_index(op.f('ix_transactions_id'), table_name='transactions')
    op.drop_table('transactions')
    op.drop_index(op.f('ix_drivers_id'), table_name='drivers')
    op.drop_table('drivers')
    # ### end Alembic commands ###
