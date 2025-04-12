def allow_anonymous(view_func):
    view_func.allow_anonymous = True
    return view_func