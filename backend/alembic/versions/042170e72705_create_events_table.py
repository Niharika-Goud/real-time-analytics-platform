from alembic import op
import sqlalchemy as sa


revision = '042170e72705'
down_revision = 'cbe59e6b6b49'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'events',

        sa.Column(
            'id',
            sa.Integer(),
            primary_key=True
        ),

        sa.Column(
            'event_type',
            sa.String(length=100),
            nullable=False
        ),

        sa.Column(
            'user_email',
            sa.String(length=255),
            nullable=False
        ),

        sa.Column(
            'event_metadata',
            sa.JSON(),
            nullable=False
        ),

        sa.Column(
            'created_at',
            sa.DateTime(),
            nullable=True
        )
    )


def downgrade():

    op.drop_table('events')