from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260328_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("service_name", sa.String(length=100), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("environment", sa.String(length=32), nullable=False),
        sa.Column("response_time_ms", sa.Integer(), nullable=True),
        sa.Column("status_code", sa.Integer(), nullable=True),
        sa.Column("source", sa.String(length=64), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "ingested_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_events_created_at", "events", ["created_at"], unique=False)
    op.create_index("ix_events_environment", "events", ["environment"], unique=False)
    op.create_index(
        "ix_events_environment_created_at",
        "events",
        ["environment", "created_at"],
        unique=False,
    )
    op.create_index("ix_events_service_name", "events", ["service_name"], unique=False)
    op.create_index("ix_events_severity", "events", ["severity"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_events_severity", table_name="events")
    op.drop_index("ix_events_service_name", table_name="events")
    op.drop_index("ix_events_environment_created_at", table_name="events")
    op.drop_index("ix_events_environment", table_name="events")
    op.drop_index("ix_events_created_at", table_name="events")
    op.drop_table("events")

