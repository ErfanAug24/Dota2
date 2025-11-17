from sqlalchemy.orm import Session
from functools import wraps


def check_class_arguments(func):
    @wraps(func)
    def wrapper(cls, *args, **kwargs):
        valid_columns = valid_columns = set(cls.__mapper__.c.keys()) | set(
            cls.__mapper__.relationships.keys()
        )

        invalid_columns = {"id"}
        for key in kwargs:
            if key not in valid_columns or key in invalid_columns:
                raise AttributeError(f"{cls.__name__} has no column '{key}'")
        return func(cls, *args, **kwargs)

    return wrapper


class ModelMixin:
    _db: Session = None

    @classmethod
    def set_session(cls, db_session: Session):
        cls._db = db_session

    @classmethod
    @check_class_arguments
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        cls._db.add(instance)
        instance.save()
        instance.refresh()
        return instance

    @classmethod
    def get(cls, id: int):
        return cls._db.get(cls, id)

    @classmethod
    def get_all(cls):
        instances = cls._db.query(cls).all()
        return instances

    @classmethod
    @check_class_arguments
    def filter_by(cls, **kwargs):
        return cls._db.query(cls).filter_by(**kwargs)

    @classmethod
    @check_class_arguments
    def update(cls, **kwargs):
        instance = cls.get(kwargs["id"])
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        instance.refresh()
        return instance

    @check_class_arguments
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()
        self.refresh()
        return self

    def remove(self):
        self.__class__._db.delete(self)
        self.save()
        return True

    @classmethod
    def remove_by_id(cls, id: int):
        obj = cls.get(id)
        if obj is None:
            return False
        return obj.remove()

    def save(self):
        self.__class__._db.commit()

    def refresh(self):
        self.__class__._db.refresh(self)
