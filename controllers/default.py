# -*- coding: utf-8 -*-

from datetime import datetime

@auth.requires_login()
def index():
    # find out if it's a new uninitialized user
    user_status = db(db.initialization.user_id == auth.user_id).select().first()
    if user_status is None:
        db.initialization.insert(user_id=auth.user_id, initialized=False)
        init = False
    else:
        init = user_status.initialized
    return dict(init=init)

@auth.requires_login()
@auth.requires_signature()
def load_data():
    budgets = db(db.category.user_id == auth.user_id).select().as_list()
    fixed_spendings = db(db.fixed_spending.user_id == auth.user_id).select().as_list()
    income = db(db.monthly_income.user_id == auth.user_id).select().as_list()
    return response.json(dict(categories=budgets,
                              fixed_spendings=fixed_spendings,
                              income=income))

@auth.requires_login()
def this_week():
    return dict()

@auth.requires_login()
def summary():
    return dict()



######### this part handle all the savings to database
@auth.requires_login()
@auth.requires_signature()
def save_income():
    db.monthly_income.update_or_insert(db.monthly_income.user_id==auth.user_id,
        user_id=auth.user_id, amount=request.vars.income)
    return "ok"

@auth.requires_login()
@auth.requires_signature()
def save_fixed_spending():
    db.fixed_spending.update_or_insert(
        (db.fixed_spending.user_id==auth.user_id)&(db.fixed_spending.name==request.vars.name),
        user_id=auth.user_id, name=request.vars.name, amount=request.vars.amount)
    return "ok"

@auth.requires_signature()
@auth.requires_login()
def save_init():
    db(db.initialization.user_id==auth.user_id).update(initialized=True)
    return "ok"


@auth.requires_login()
@auth.requires_signature()
def save_budget():
    db.category.update_or_insert(
        (db.category.user_id==auth.user_id)&(db.category.name==request.vars.name),
        user_id=auth.user_id, name=request.vars.name, budget=request.vars.amount)
    return "ok"


@auth.requires_login()
@auth.requires_signature()
def save_spending_history():
    db.spending_history.insert(user_id=auth.user_id,
                               category=request.vars.category_id,
                               amount=request.vars.amount,
                               time_stamp=datetime.now()
                               )
    return "ok"

############## this part handles all the deletions ###########
@auth.requires_signature()
def delete_budget_category():
    db(db.category.id == request.vars.category_id).delete()
    return "ok"

@auth.requires_signature()
def delete_fixed_spending():
    db(db.fixed_spending.id == request.vars.fixed_id).delete()
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


