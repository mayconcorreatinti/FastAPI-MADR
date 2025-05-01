from sqlalchemy.orm import Mapped, mapped_column, registry
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
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

    id: Mapped[int] = mapped_column(init=False,primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    books: Mapped[list['Books']] = relationship(
        init=False, back_populates='novelist', cascade='all, delete-orphan'
    )


@table_registry.mapped_as_dataclass
class Books:
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True,init=False)
    year: Mapped[int]
    title: Mapped[str] = mapped_column(unique=True)
    novelist_id: Mapped[int] = mapped_column(ForeignKey('novelists.id'))
    novelist: Mapped[Novelist] = relationship(
        init=False, back_populates='books'
    )

