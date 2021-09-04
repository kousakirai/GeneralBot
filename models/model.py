from sqlalchemy import MetaData, Table, Column, BigInteger, String,Integer, Boolean


meta = MetaData()

guild = Table(
    "guild",
    meta,
    Column("id", BigInteger(), nullable=False, primary_key=True),
    Column("prefix", String(8), server_default="g!", nullable=False),
    Column("auth_ch", BigInteger(), nullable=True),
    Column("auth_role", BigInteger(), nullable=True),
    Column("level", Boolean(), default=False)
)

level = Table(
    "level",
    meta,
    Column("id", BigInteger(), nullable=False,
    primary_key=True),
    Column("exp", Integer(), nullable=True),
    Column("level", Integer(), nullable=True)
)

auth = Table(
    "auth",
    meta,
    Column("id", BigInteger(), nullable=False, primary_key=True),
    Column("code", Integer(), nullable=False),
)