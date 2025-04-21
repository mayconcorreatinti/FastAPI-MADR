from sqlalchemy.orm import Mapped, mapped_column, registry


table_registry = registry()

@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]


@table_registry.mapped_as_dataclass
class Novelist:
    __tablename__ = 'novelists'

    id:Mapped[int] = mapped_column(init=False,primary_key=True)
    name:Mapped[str] = mapped_column(unique=True)