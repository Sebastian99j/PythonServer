import sqlalchemy
metadata = sqlalchemy.MetaData()


class Schemas():
    userTable = sqlalchemy.Table(
        "users",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("email", sqlalchemy.String),
        sqlalchemy.Column("password", sqlalchemy.String)
    )

    dziennik_zdarzen = sqlalchemy.Table(
        "dziennik_zdarzen",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("userid", sqlalchemy.Integer),
        sqlalchemy.Column("datatime", sqlalchemy.String),
        sqlalchemy.Column("incident", sqlalchemy.String),
        sqlalchemy.Column("loss", sqlalchemy.String)
    )

    warunki_biezace = sqlalchemy.Table(
        "warunki_biezace",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("userid", sqlalchemy.Integer),
        sqlalchemy.Column("plant", sqlalchemy.String),
        sqlalchemy.Column("term", sqlalchemy.String),
     sqlalchemy.Column("condition", sqlalchemy.String)
    )

    zabiegi_agrotechniczne = sqlalchemy.Table(
        "zabiegi_agrotechniczne",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("userid", sqlalchemy.Integer),
        sqlalchemy.Column("date", sqlalchemy.String),
        sqlalchemy.Column("action", sqlalchemy.String),
        sqlalchemy.Column("data1", sqlalchemy.String),
        sqlalchemy.Column("data2", sqlalchemy.String)
    )