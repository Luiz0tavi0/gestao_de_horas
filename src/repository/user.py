from typing import Dict
import ipdb
from flask import current_app
from sqlalchemy import update, select
from sqlalchemy.orm import load_only, defer, Load, undefer

from sqlalchemy.exc import IntegrityError
from src.adapters.user import User
from src.repository.interfaces.user import IUserRepository
from pydantic import BaseModel
from redis import StrictRedis


class UserRepository(IUserRepository):

    def __init__(self) -> None:
        self.session = current_app.db.session

    def get_user_by_id(self, identity: int):

        return self.session.query(User).get(identity)

    def get_user_by_email(self, email: str):

        return self.session.query(User).options(undefer("id")).filter(User.email == email).first_or_404()

        # return self.session.query(User).filter(User.email == email).first_or_404()

    def exists_by_id(self, identity) -> bool:

        return self.session.query(self.session.query(User).filter(User.id == identity).exists()).scalar()

    def exists_by_email(self, email: str) -> bool:

        return self.session.query(self.session.query(User).filter(User.email == email).exists()).scalar()

    def create(self, data: BaseModel):
        #
        import ipdb
#
        user = User(**data.dict())
        user._gen_hash()
        try:
            self.session.add(user)

            self.session.commit()
            self.session.refresh(user)

        except IntegrityError as i_err:
            self.session.rollback()
            self.session.commit()
            raise i_err

        return user

    def update(self, identity: int, data: Dict[str, str | int]):
        user = self.get_user_by_id(identity)
#

        to_update = {}
        # checks need for update
        for key, value in data.items():
            if hasattr(User, key) and getattr(user, key) != value:
                # print(f'BD ->{getattr(user, key)} -------------- Payload -> {value}')
                to_update[key] = value

#
        if not to_update:
            return to_update
        stmt = update(User).where(User.id == identity).values(**to_update)
        try:
            self.session.execute(stmt)
            self.session.commit()
            self.session.refresh(user)
        except IntegrityError as i_err:

            self.session.rollback()
            self.session.commit()
            raise i_err
        return user

    def get_paginated(self, page=1, per_page=10):

        per_page = min(25, per_page)

        users_paginated = User.query.order_by(User.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False)

        return {
            'page': page,
            'perPage': per_page,
            'hasNext': users_paginated.has_next,
            'hasPrev': users_paginated.has_prev,
            'pageList': [user_page if user_page else '...' for user_page in users_paginated.iter_pages()],
            'count': users_paginated.total,
            'items': users_paginated.items
        }

    def remove_by_id(self, id_: int) -> bool:

        resp = User.query.filter(User.id.is_(id_)).delete()
        self.session.commit()
        return bool(resp)

    def change_password(self, identity, password: str):

        user = self.get_user_by_id(identity=identity)
        user.set_password(password)
        self.session.commit()
        self.session.refresh(user)
        return user
