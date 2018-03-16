"""empty message

Revision ID: e004bc53d32c
Revises: 
Create Date: 2018-03-15 18:56:52.295793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e004bc53d32c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auth_permissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tag')
    )
    op.create_table('metas',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('descricao', sa.VARCHAR(length=80), nullable=True),
    sa.Column('tipo', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pessoas',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nome', sa.VARCHAR(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('revoked_token',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('jti', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usuario', sa.String(length=15), nullable=True),
    sa.Column('senha', sa.String(length=64), nullable=True),
    sa.Column('pessoa_id', sa.Integer(), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['pessoa_id'], ['pessoas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('auth_usuarios_permissions',
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('auth_tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['auth_tag_id'], ['auth_permissions.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('usuario_id', 'auth_tag_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('auth_usuarios_permissions')
    op.drop_table('usuarios')
    op.drop_table('revoked_token')
    op.drop_table('pessoas')
    op.drop_table('metas')
    op.drop_table('auth_permissions')
    # ### end Alembic commands ###
