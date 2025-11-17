import pytest
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.utils.model_mixin import ModelMixin
from app.models import Base


class TextModel(ModelMixin, Base):
    __tablename__ = "text_model"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    text: Mapped[str] = mapped_column(String(100), nullable=False)


def test_creation(session):
    obj = TextModel.create(text="sample text")
    assert obj.id is not None
    assert obj.text == "sample text"


def test_get_all(session):

    obj1 = TextModel.create(text="text one")
    obj2 = TextModel.create(text="text two")
    all_objs = TextModel.get_all()
    assert len(all_objs) == 2
    assert all_objs[0].text == "text one"
    assert all_objs[1].text == "text two"
    assert True


def test_get(session):
    obj = TextModel.create(text="sample text")
    fetched = TextModel.get(obj.id)
    assert fetched.id == obj.id
    assert True


def test_update(session):
    obj = TextModel.create(text="sample text")
    assert obj.text == "sample text"
    obj.update(text="sample text updated")
    assert obj.text == "sample text updated"


def test_remove(session):
    obj = TextModel.create(text="sample text")
    obj.remove()
    assert TextModel.get(obj.id) is None


def test_create_invalid_column(session):
    with pytest.raises(AttributeError):
        TextModel.create(text="valid", invalid_column="invalid")


def test_filter_by_invalid_column(session):
    with pytest.raises(AttributeError):
        TextModel.filter_by(invalid_column="value").get()


def test_update_invalid_column(session):
    obj = TextModel.create(text="sample text")
    with pytest.raises(AttributeError):
        obj.update(invalid_column="value")


def test_remove_nonexistent(session):
    result = TextModel.remove_by_id(9999)
    assert result is False


def test_session_not_set():
    class DummyModel(ModelMixin, Base):
        __tablename__ = "dummy_model"
        id: Mapped[int] = mapped_column(
            primary_key=True, autoincrement=True, init=False
        )
        text: Mapped[str]

    ModelMixin._db = None
    with pytest.raises(AttributeError):
        DummyModel.create(text="hello")


def test_create_missing_field(session):
    with pytest.raises(TypeError):
        TextModel.create()
