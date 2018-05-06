"""empty message

Revision ID: a11d0f25b6c3
Revises: 
Create Date: 2018-05-05 19:25:51.939456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a11d0f25b6c3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('billing_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('patient',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('first_name', sa.String(length=60), nullable=True),
    sa.Column('last_name', sa.String(length=60), nullable=True),
    sa.Column('national_id', sa.String(length=60), nullable=True),
    sa.Column('mobile_number', sa.String(length=10), nullable=True),
    sa.Column('address', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_patient_address'), 'patient', ['address'], unique=False)
    op.create_index(op.f('ix_patient_first_name'), 'patient', ['first_name'], unique=False)
    op.create_index(op.f('ix_patient_last_name'), 'patient', ['last_name'], unique=False)
    op.create_index(op.f('ix_patient_mobile_number'), 'patient', ['mobile_number'], unique=True)
    op.create_index(op.f('ix_patient_national_id'), 'patient', ['national_id'], unique=True)
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('medical_condition',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bp', sa.Integer(), nullable=True),
    sa.Column('temperature', sa.Float(), nullable=True),
    sa.Column('special_conditions', sa.String(length=100), nullable=True),
    sa.Column('patient_id', sa.BigInteger(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('billing_item_name', sa.String(length=60), nullable=True),
    sa.Column('patient_id', sa.BigInteger(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['billing_item_name'], ['billing_item.name'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('prescription',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('patient_id', sa.BigInteger(), nullable=True),
    sa.Column('doctor', sa.String(length=60), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('username', sa.String(length=60), nullable=True),
    sa.Column('first_name', sa.String(length=60), nullable=True),
    sa.Column('last_name', sa.String(length=60), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_first_name'), 'user', ['first_name'], unique=False)
    op.create_index(op.f('ix_user_last_name'), 'user', ['last_name'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('prescription_item',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('frequency', sa.Integer(), nullable=True),
    sa.Column('instruction', sa.String(length=60), nullable=True),
    sa.Column('prescription_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['prescription_id'], ['prescription.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_prescription_item_duration'), 'prescription_item', ['duration'], unique=False)
    op.create_index(op.f('ix_prescription_item_frequency'), 'prescription_item', ['frequency'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_prescription_item_frequency'), table_name='prescription_item')
    op.drop_index(op.f('ix_prescription_item_duration'), table_name='prescription_item')
    op.drop_table('prescription_item')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_last_name'), table_name='user')
    op.drop_index(op.f('ix_user_first_name'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('prescription')
    op.drop_table('payment')
    op.drop_table('medical_condition')
    op.drop_table('role')
    op.drop_index(op.f('ix_patient_national_id'), table_name='patient')
    op.drop_index(op.f('ix_patient_mobile_number'), table_name='patient')
    op.drop_index(op.f('ix_patient_last_name'), table_name='patient')
    op.drop_index(op.f('ix_patient_first_name'), table_name='patient')
    op.drop_index(op.f('ix_patient_address'), table_name='patient')
    op.drop_table('patient')
    op.drop_table('billing_item')
    # ### end Alembic commands ###
