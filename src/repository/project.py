from flask import current_app
from src.adapters.project import Project

class UserRepository:
    def __init__(self) -> None:
        self.session = current_app.db.session
    
    def create(self, data):
        user = Project(**data)        
        # import ipdb;ipdb.set_trace()
        self.session.add(user)
        import ipdb;ipdb.set_trace()
        self.session.flush()
        self.session.commit()
        return user
        
    def get_paginated(self, page = 1, per_page = 10):

        per_page = min(25, per_page)
        
        users_paginated = Project.query.order_by(Project.id.desc()).paginate(page=page, per_page=per_page, error_out=False)

        return {
        'page': page,
        'perPage': per_page,
        'hasNext': users_paginated.has_next,
        'hasPrev': users_paginated.has_prev,
        'pageList': [user_page if user_page else '...' for user_page in users_paginated.iter_pages()],
        'count': users_paginated.total,
        'items': users_paginated.items 
    }
    
    def remove_by_id(self, id_:int) -> bool:
        # import ipdb; ipdb.set_trace()
        resp=Project.query.filter(Project.id.is_(id_)).delete()
        self.session.commit()
        # import ipdb; ipdb.set_trace()