# -*- coding: utf-8 -*-


@auth.requires_login()
def index():
    return dict()

@auth.requires_signature()
def load_budget_categories():
    rows = db(db.category.user_id == auth.user_id).select().as_list()
    print rows
    # categories = {}
    # for r in rows:
    #     categories[r.name] = r.budget
    return response.json(dict(categories=rows))


@auth.requires_login()
def this_week():
    return dict()

@auth.requires_login()
def summary():
    return dict()

@auth.requires_login()
@auth.requires_signature()
def save_income():
    db.monthly_income.update_or_insert(db.monthly_income.user_id==auth.user_id,
        user_id=auth.user_id, amount=request.vars.income)
    return "ok"

@auth.requires_login()
@auth.requires_signature()
def save_budget():
    db.category.update_or_insert(
        (db.category.user_id==auth.user_id)&(db.category.name==request.vars.name),
        user_id=auth.user_id, name=request.vars.name, budget=request.vars.amount)
    return "ok"



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


