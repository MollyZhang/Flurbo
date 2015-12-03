# -*- coding: utf-8 -*-


@auth.requires_login()
def index():
    """
    start up users with initial budget catogories
    """

    ######## save current user's budget categories as a dictionaries
    budget_categories = {"fixed":{}, "changing":{}}
    fixed_budget_categories = db(db.fixed_budget.user_id == auth.user_id).select().as_list()[0]
    changing_budget_categories = db(db.changing_budget.user_id == auth.user_id).select().as_list()[0]
    keys1 = sorted(fixed_budget_categories.keys())[0:-2]
    for key in keys1:
        budget_categories["fixed"][fixed_budget_categories[key]] = 0
    keys2 = sorted(changing_budget_categories.keys())[0:-2]
    for key in keys2:
        budget_categories["changing"][changing_budget_categories[key]] = 0


    return dict(budget_categories=budget_categories)


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


