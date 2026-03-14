from typing import Optional

from flask import Flask, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectMultipleField
from flask_admin.theme import Bootstrap4Theme
from sqlalchemy import ForeignKey, Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

MODE = "lite"

if MODE == "lite":
    from flask_sqlalchemy_lite import SQLAlchemy
else:
    from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
if MODE == "lite":
    app.config["SQLALCHEMY_ENGINES"] = {"default": "sqlite://"}
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"

app.config["SECRET_KEY"] = "super sectet"
db = SQLAlchemy(app)


@app.route("/")
def index():
    return redirect(url_for("arts.index_view"))


if MODE == "lite":

    class Base(DeclarativeBase):
        """Base model of sqlalchemy."""
else:

    class Base(db.Model):
        """Base model of sqlalchemy."""

        __abstract__ = True


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    art_id: Mapped[int] = mapped_column(
        ForeignKey("arts.id", ondelete="SET NULL"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(255))

    art: Mapped["Art"] = relationship(back_populates="teams")

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"

    def __repr__(self) -> str:
        return f"Team({self.name!r}:{self.description!r})"


class Art(Base):
    __tablename__ = "arts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(255))

    teams: Mapped[list["Team"]] = relationship(back_populates="art")

    def __str__(self) -> str:
        return f"ART-{self.id} {self.name}"

    def __repr__(self) -> str:
        return f"Art({self.name!r}:{self.description!r})"


class TeamsView(ModelView):
    # list view
    column_list = ["name", "description"]
    column_editable_list = ["name", "description"]

    # edit forms
    form_columns = ["name", "description"]


class ArtsView(ModelView):
    # List columns
    column_list = ["name", "description", "teams"]
    column_editable_list = ["name", "description"]
    column_searchable_list = ["name", "description"]
    column_formatters = {
        "teams": lambda v, c, m, n: str([f"{t.name}" for t in m.teams]),
    }
    column_auto_select_related = True

    # edit forms
    form_columns = ["name", "description", "teams"]

    # form_extra_fields = {
    #     "teams": QuerySelectMultipleField(
    #         "teams",
    #         query_factory=lambda: db.session.scalars(select(Team)),
    #         allow_blank=True,
    #     )
    # }

    # form_args = {
    #     "teams": {
    #         "query_factory": lambda: db.session.scalars(select(Team)),
    #         "get_label": "name"
    #     }
    # }


if __name__ == "__main__":
    admin = Admin(
        app=app,
        name="test",
        theme=Bootstrap4Theme(swatch="cerulean", fluid=True),
    )

    with app.app_context():
        if MODE == "lite":
            engine = db.engines["default"]
            Base.metadata.create_all(bind=engine)
        else:
            db.create_all()
        teams = [Team(name = f"team_{i}") for i in range(1, 6)]
        db.session.add_all(teams)
        db.session.commit()

        admin.add_view(TeamsView(Team, db, name="Teams", endpoint="teams"))
        admin.add_view(ArtsView(Art, db, name="Arts", endpoint="arts"))

    app.run(debug=True)
