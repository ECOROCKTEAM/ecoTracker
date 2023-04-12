"""Database init tables v1

Revision ID: 2a600d99580c
Revises: 1bc066db6725
Create Date: 2023-04-10 01:08:23.727630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2a600d99580c"
down_revision = "1bc066db6725"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "achievement_category",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "achievement_progress_status",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "community_role",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "constraint",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("value_type", sa.Enum("STR", "INT", "BOOL", name="variable_type_enum"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "contact_type",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table("occupancy_status", sa.Column("id", sa.Integer(), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_table("occupancy_type", sa.Column("id", sa.Integer(), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_table(
        "privacy_type", sa.Column("id", sa.Integer(), autoincrement=True, nullable=False), sa.PrimaryKeyConstraint("id")
    )
    op.create_table(
        "subscription_period_unit",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "subscription_type",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("username"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "value_type",
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("name"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "achievement",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("total", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["achievement_category.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "achievement_category_translate",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("language", sa.Enum("RU", "EN", name="language_enum"), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["achievement_category.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "achievement_progress_status_translate",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("status_id", sa.Integer(), nullable=False),
        sa.Column("language", sa.Enum("RU", "EN", name="language_enum"), nullable=False),
        sa.ForeignKeyConstraint(
            ["status_id"],
            ["achievement_progress_status.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "community",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("privacy_type_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["privacy_type_id"],
            ["privacy_type.id"],
        ),
        sa.PrimaryKeyConstraint("name"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "community_role_translate",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.Column("language", sa.Enum("RU", "EN", name="language_enum"), nullable=False),
        sa.ForeignKeyConstraint(
            ["type_id"],
            ["community_role.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "contact",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["type_id"],
            ["contact_type.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "contact_type_translate",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.Column("language", sa.Enum("RU", "EN", name="language_enum"), nullable=False),
        sa.ForeignKeyConstraint(
            ["type_id"],
            ["contact_type.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "mission",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("author", sa.String(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("occupancy_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["occupancy_id"],
            ["occupancy_type.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "occupancy_status_translate",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("status_id", sa.Integer(), nullable=False),
        sa.Column("language", sa.Enum("RU", "EN", name="language_enum"), nullable=False),
        sa.ForeignKeyConstraint(
            ["status_id"],
            ["occupancy_status.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "occupancy_type_translate",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.Column("language", sa.Enum("RU", "EN", name="language_enum"), nullable=False),
        sa.ForeignKeyConstraint(
            ["type_id"],
            ["occupancy_type.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "privacy_type_translate",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.Column("language", sa.Enum("RU", "EN", name="language_enum"), nullable=False),
        sa.ForeignKeyConstraint(
            ["type_id"],
            ["privacy_type.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "subscription_period",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("unit_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["unit_id"],
            ["subscription_period_unit.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "subscription_period_unit_translate",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.Column("language", sa.Enum("RU", "EN", name="language_enum"), nullable=False),
        sa.ForeignKeyConstraint(
            ["type_id"],
            ["subscription_period_unit.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "subscription_type_constraint",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.Column("constraint_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["constraint_id"],
            ["constraint.id"],
        ),
        sa.ForeignKeyConstraint(
            ["type_id"],
            ["subscription_type.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "subscription_type_translate",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.Column("language", sa.Enum("RU", "EN", name="language_enum"), nullable=False),
        sa.ForeignKeyConstraint(
            ["type_id"],
            ["subscription_type.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "task",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("occupancy_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["occupancy_id"],
            ["occupancy_type.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_score",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("operation", sa.Enum("PLUS", "MINUS", name="score_operation_enum"), nullable=False),
        sa.Column("value", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["username"],
            ["user.username"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "achievement_progress",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("achievement_id", sa.Integer(), nullable=False),
        sa.Column("entity_name", sa.String(), nullable=False),
        sa.Column("entity_pointer", sa.String(), nullable=False),
        sa.Column("counter", sa.Integer(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("status_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["achievement_id"],
            ["achievement.id"],
        ),
        sa.ForeignKeyConstraint(
            ["status_id"],
            ["achievement_progress_status.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "achievement_translate",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("achievement_id", sa.Integer(), nullable=False),
        sa.Column("language", sa.Enum("RU", "EN", name="language_enum"), nullable=False),
        sa.ForeignKeyConstraint(
            ["achievement_id"],
            ["achievement.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "community_mission",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("meeting_date", sa.DateTime(), nullable=False),
        sa.Column("people_required", sa.Integer(), nullable=True),
        sa.Column("people_max", sa.Integer(), nullable=True),
        sa.Column("place", sa.String(), nullable=True),
        sa.Column("comment", sa.String(), nullable=True),
        sa.Column("community", sa.String(), nullable=False),
        sa.Column("mission_id", sa.Integer(), nullable=False),
        sa.Column("status_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["community"],
            ["community.name"],
        ),
        sa.ForeignKeyConstraint(
            ["mission_id"],
            ["mission.id"],
        ),
        sa.ForeignKeyConstraint(
            ["status_id"],
            ["occupancy_status.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "community_score",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("community", sa.String(), nullable=False),
        sa.Column("operation", sa.Enum("PLUS", "MINUS", name="score_operation_enum"), nullable=False),
        sa.Column("value", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["community"],
            ["community.name"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "mission_translate",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("instruction", sa.String(), nullable=False),
        sa.Column("mission_id", sa.Integer(), nullable=False),
        sa.Column("language", sa.Enum("RU", "EN", name="language_enum"), nullable=False),
        sa.ForeignKeyConstraint(
            ["mission_id"],
            ["mission.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "subscription",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.Column("period_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["period_id"],
            ["subscription_period.id"],
        ),
        sa.ForeignKeyConstraint(
            ["type_id"],
            ["subscription_type.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "subscription_period_translate",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.Column("language", sa.Enum("RU", "EN", name="language_enum"), nullable=False),
        sa.ForeignKeyConstraint(
            ["type_id"],
            ["subscription_period.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "task_translate",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("language", sa.Enum("RU", "EN", name="language_enum"), nullable=False),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["task.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_community",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("community_name", sa.String(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["community_name"],
            ["community.name"],
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["community_role.id"],
        ),
        sa.ForeignKeyConstraint(
            ["username"],
            ["user.username"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_contact",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("contact_id", sa.Integer(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["contact_id"],
            ["contact.id"],
        ),
        sa.ForeignKeyConstraint(
            ["username"],
            ["user.username"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("contact_id"),
    )
    op.create_table(
        "user_mission",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(), autoincrement=False, nullable=False),
        sa.Column("mission_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("status_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["mission_id"],
            ["mission.id"],
        ),
        sa.ForeignKeyConstraint(
            ["status_id"],
            ["occupancy_status.id"],
        ),
        sa.ForeignKeyConstraint(
            ["username"],
            ["user.username"],
        ),
        sa.PrimaryKeyConstraint("id", "username", "mission_id"),
    )
    op.create_table(
        "user_task",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("status_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["status_id"],
            ["occupancy_status.id"],
        ),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["task.id"],
        ),
        sa.ForeignKeyConstraint(
            ["username"],
            ["user.username"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "subscription_translate",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("subscription_id", sa.Integer(), nullable=False),
        sa.Column("language", sa.Enum("RU", "EN", name="language_enum"), nullable=False),
        sa.ForeignKeyConstraint(
            ["subscription_id"],
            ["subscription.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_subscription",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("subscription_id", sa.Integer(), nullable=False),
        sa.Column("cancelled", sa.Boolean(), nullable=False),
        sa.Column("until_date", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["subscription_id"],
            ["subscription.id"],
        ),
        sa.ForeignKeyConstraint(
            ["username"],
            ["user.username"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_subscription")
    op.drop_table("subscription_translate")
    op.drop_table("user_task")
    op.drop_table("user_mission")
    op.drop_table("user_contact")
    op.drop_table("user_community")
    op.drop_table("task_translate")
    op.drop_table("subscription_period_translate")
    op.drop_table("subscription")
    op.drop_table("mission_translate")
    op.drop_table("community_score")
    op.drop_table("community_mission")
    op.drop_table("achievement_translate")
    op.drop_table("achievement_progress")
    op.drop_table("user_score")
    op.drop_table("task")
    op.drop_table("subscription_type_translate")
    op.drop_table("subscription_type_constraint")
    op.drop_table("subscription_period_unit_translate")
    op.drop_table("subscription_period")
    op.drop_table("privacy_type_translate")
    op.drop_table("occupancy_type_translate")
    op.drop_table("occupancy_status_translate")
    op.drop_table("mission")
    op.drop_table("contact_type_translate")
    op.drop_table("contact")
    op.drop_table("community_role_translate")
    op.drop_table("community")
    op.drop_table("achievement_progress_status_translate")
    op.drop_table("achievement_category_translate")
    op.drop_table("achievement")
    op.drop_table("value_type")
    op.drop_table("user")
    op.drop_table("subscription_type")
    op.drop_table("subscription_period_unit")
    op.drop_table("privacy_type")
    op.drop_table("occupancy_type")
    op.drop_table("occupancy_status")
    op.drop_table("contact_type")
    op.drop_table("constraint")
    op.drop_table("community_role")
    op.drop_table("achievement_progress_status")
    op.drop_table("achievement_category")
    
    op.execute("DROP TYPE variable_type_enum;")
    op.execute("DROP TYPE language_enum;")
    op.execute("DROP TYPE score_operation_enum;")
    # ### end Alembic commands ###