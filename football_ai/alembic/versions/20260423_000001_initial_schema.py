"""initial schema

Revision ID: 20260423_000001
Revises:
Create Date: 2026-04-23 00:00:01.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "20260423_000001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "leagues",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_index(op.f("ix_leagues_code"), "leagues", ["code"], unique=False)

    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("league_id", sa.Integer(), nullable=False),
        sa.Column("espn_team_id", sa.String(length=32), nullable=True),
        sa.Column("display_name", sa.String(length=128), nullable=False),
        sa.Column("short_name", sa.String(length=64), nullable=True),
        sa.Column("abbreviation", sa.String(length=16), nullable=True),
        sa.Column("location", sa.String(length=64), nullable=True),
        sa.Column("nickname", sa.String(length=64), nullable=True),
        sa.Column("color", sa.String(length=16), nullable=True),
        sa.Column("alternate_color", sa.String(length=16), nullable=True),
        sa.Column("logo_url", sa.String(length=512), nullable=True),
        sa.ForeignKeyConstraint(["league_id"], ["leagues.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("espn_team_id"),
    )
    op.create_index(op.f("ix_teams_abbreviation"), "teams", ["abbreviation"], unique=False)
    op.create_index(op.f("ix_teams_display_name"), "teams", ["display_name"], unique=False)
    op.create_index(op.f("ix_teams_league_id"), "teams", ["league_id"], unique=False)

    op.create_table(
        "players",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=True),
        sa.Column("espn_athlete_id", sa.String(length=32), nullable=True),
        sa.Column("full_name", sa.String(length=128), nullable=False),
        sa.Column("short_name", sa.String(length=64), nullable=True),
        sa.Column("position", sa.String(length=16), nullable=True),
        sa.Column("jersey", sa.String(length=8), nullable=True),
        sa.Column("headshot_url", sa.String(length=512), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.ForeignKeyConstraint(["team_id"], ["teams.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("espn_athlete_id"),
    )
    op.create_index(op.f("ix_players_full_name"), "players", ["full_name"], unique=False)
    op.create_index(op.f("ix_players_position"), "players", ["position"], unique=False)
    op.create_index(op.f("ix_players_team_id"), "players", ["team_id"], unique=False)

    op.create_table(
        "games",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("league_id", sa.Integer(), nullable=False),
        sa.Column("espn_event_id", sa.String(length=32), nullable=False),
        sa.Column("season", sa.Integer(), nullable=False),
        sa.Column("week", sa.Integer(), nullable=True),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("venue_name", sa.String(length=128), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=True),
        sa.Column("home_team_id", sa.Integer(), nullable=False),
        sa.Column("away_team_id", sa.Integer(), nullable=False),
        sa.Column("home_score", sa.Integer(), nullable=True),
        sa.Column("away_score", sa.Integer(), nullable=True),
        sa.Column("neutral_site", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.ForeignKeyConstraint(["away_team_id"], ["teams.id"]),
        sa.ForeignKeyConstraint(["home_team_id"], ["teams.id"]),
        sa.ForeignKeyConstraint(["league_id"], ["leagues.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("espn_event_id"),
    )
    op.create_index(op.f("ix_games_espn_event_id"), "games", ["espn_event_id"], unique=False)
    op.create_index(op.f("ix_games_home_team_id"), "games", ["home_team_id"], unique=False)
    op.create_index(op.f("ix_games_away_team_id"), "games", ["away_team_id"], unique=False)
    op.create_index(op.f("ix_games_league_id"), "games", ["league_id"], unique=False)
    op.create_index(op.f("ix_games_season"), "games", ["season"], unique=False)
    op.create_index(op.f("ix_games_start_time"), "games", ["start_time"], unique=False)
    op.create_index(op.f("ix_games_status"), "games", ["status"], unique=False)
    op.create_index(op.f("ix_games_week"), "games", ["week"], unique=False)

    op.create_table(
        "roster_snapshots",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("player_id", sa.Integer(), nullable=False),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("raw_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("depth_position", sa.String(length=16), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=True),
        sa.ForeignKeyConstraint(["player_id"], ["players.id"]),
        sa.ForeignKeyConstraint(["team_id"], ["teams.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_roster_snapshots_captured_at"), "roster_snapshots", ["captured_at"], unique=False)
    op.create_index(op.f("ix_roster_snapshots_player_id"), "roster_snapshots", ["player_id"], unique=False)
    op.create_index(op.f("ix_roster_snapshots_team_id"), "roster_snapshots", ["team_id"], unique=False)

    op.create_table(
        "injury_reports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("player_id", sa.Integer(), nullable=True),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=True),
        sa.Column("detail", sa.String(length=256), nullable=True),
        sa.Column("raw_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(["player_id"], ["players.id"]),
        sa.ForeignKeyConstraint(["team_id"], ["teams.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_injury_reports_captured_at"), "injury_reports", ["captured_at"], unique=False)
    op.create_index(op.f("ix_injury_reports_player_id"), "injury_reports", ["player_id"], unique=False)
    op.create_index(op.f("ix_injury_reports_status"), "injury_reports", ["status"], unique=False)
    op.create_index(op.f("ix_injury_reports_team_id"), "injury_reports", ["team_id"], unique=False)

    op.create_table(
        "news_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("league_id", sa.Integer(), nullable=True),
        sa.Column("team_id", sa.Integer(), nullable=True),
        sa.Column("player_id", sa.Integer(), nullable=True),
        sa.Column("external_id", sa.String(length=64), nullable=True),
        sa.Column("source_name", sa.String(length=64), nullable=True),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("url", sa.String(length=1024), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("raw_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(["league_id"], ["leagues.id"]),
        sa.ForeignKeyConstraint(["player_id"], ["players.id"]),
        sa.ForeignKeyConstraint(["team_id"], ["teams.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("external_id"),
    )
    op.create_index(op.f("ix_news_items_league_id"), "news_items", ["league_id"], unique=False)
    op.create_index(op.f("ix_news_items_player_id"), "news_items", ["player_id"], unique=False)
    op.create_index(op.f("ix_news_items_published_at"), "news_items", ["published_at"], unique=False)
    op.create_index(op.f("ix_news_items_source_name"), "news_items", ["source_name"], unique=False)
    op.create_index(op.f("ix_news_items_team_id"), "news_items", ["team_id"], unique=False)

    op.create_table(
        "game_drives",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.Column("drive_index", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=True),
        sa.Column("raw_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(["game_id"], ["games.id"]),
        sa.ForeignKeyConstraint(["team_id"], ["teams.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_game_drives_drive_index"), "game_drives", ["drive_index"], unique=False)
    op.create_index(op.f("ix_game_drives_game_id"), "game_drives", ["game_id"], unique=False)
    op.create_index(op.f("ix_game_drives_team_id"), "game_drives", ["team_id"], unique=False)

    op.create_table(
        "game_plays",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.Column("drive_id", sa.Integer(), nullable=True),
        sa.Column("play_index", sa.Integer(), nullable=False),
        sa.Column("raw_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(["drive_id"], ["game_drives.id"]),
        sa.ForeignKeyConstraint(["game_id"], ["games.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_game_plays_drive_id"), "game_plays", ["drive_id"], unique=False)
    op.create_index(op.f("ix_game_plays_game_id"), "game_plays", ["game_id"], unique=False)
    op.create_index(op.f("ix_game_plays_play_index"), "game_plays", ["play_index"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_game_plays_play_index"), table_name="game_plays")
    op.drop_index(op.f("ix_game_plays_game_id"), table_name="game_plays")
    op.drop_index(op.f("ix_game_plays_drive_id"), table_name="game_plays")
    op.drop_table("game_plays")

    op.drop_index(op.f("ix_game_drives_team_id"), table_name="game_drives")
    op.drop_index(op.f("ix_game_drives_game_id"), table_name="game_drives")
    op.drop_index(op.f("ix_game_drives_drive_index"), table_name="game_drives")
    op.drop_table("game_drives")

    op.drop_index(op.f("ix_news_items_team_id"), table_name="news_items")
    op.drop_index(op.f("ix_news_items_source_name"), table_name="news_items")
    op.drop_index(op.f("ix_news_items_published_at"), table_name="news_items")
    op.drop_index(op.f("ix_news_items_player_id"), table_name="news_items")
    op.drop_index(op.f("ix_news_items_league_id"), table_name="news_items")
    op.drop_table("news_items")

    op.drop_index(op.f("ix_injury_reports_team_id"), table_name="injury_reports")
    op.drop_index(op.f("ix_injury_reports_status"), table_name="injury_reports")
    op.drop_index(op.f("ix_injury_reports_player_id"), table_name="injury_reports")
    op.drop_index(op.f("ix_injury_reports_captured_at"), table_name="injury_reports")
    op.drop_table("injury_reports")

    op.drop_index(op.f("ix_roster_snapshots_team_id"), table_name="roster_snapshots")
    op.drop_index(op.f("ix_roster_snapshots_player_id"), table_name="roster_snapshots")
    op.drop_index(op.f("ix_roster_snapshots_captured_at"), table_name="roster_snapshots")
    op.drop_table("roster_snapshots")

    op.drop_index(op.f("ix_games_week"), table_name="games")
    op.drop_index(op.f("ix_games_status"), table_name="games")
    op.drop_index(op.f("ix_games_start_time"), table_name="games")
    op.drop_index(op.f("ix_games_season"), table_name="games")
    op.drop_index(op.f("ix_games_league_id"), table_name="games")
    op.drop_index(op.f("ix_games_away_team_id"), table_name="games")
    op.drop_index(op.f("ix_games_home_team_id"), table_name="games")
    op.drop_index(op.f("ix_games_espn_event_id"), table_name="games")
    op.drop_table("games")

    op.drop_index(op.f("ix_players_team_id"), table_name="players")
    op.drop_index(op.f("ix_players_position"), table_name="players")
    op.drop_index(op.f("ix_players_full_name"), table_name="players")
    op.drop_table("players")

    op.drop_index(op.f("ix_teams_league_id"), table_name="teams")
    op.drop_index(op.f("ix_teams_display_name"), table_name="teams")
    op.drop_index(op.f("ix_teams_abbreviation"), table_name="teams")
    op.drop_table("teams")

    op.drop_index(op.f("ix_leagues_code"), table_name="leagues")
    op.drop_table("leagues")
