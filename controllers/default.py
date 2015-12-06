import datetime


############### This part is the controller for all views #################

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
def this_week():
    return dict()

@auth.requires_login()
def edit_budget():
    return dict()

@auth.requires_login()
def summary():
    return dict()

#############################################################################

######### This part loads data for the views#################################



@auth.requires_login()
@auth.requires_signature()
def load_data():
    categories = db(db.category.user_id == auth.user_id).select().as_list()
    fixed_spendings = db(db.fixed_spending.user_id == auth.user_id).select().as_list()
    income = db(db.monthly_income.user_id == auth.user_id).select().as_list()
    spendings_by_user = db(db.spending_history.user_id == auth.user_id).select()
    spendings_by_user_this_week = get_this_week_spending(spendings_by_user, categories)
    return response.json(dict(categories=categories,
                              fixed_spendings=fixed_spendings,
                              income=income,
                              spendings=spendings_by_user_this_week))

def get_this_week_spending(spendings_by_user, budgets):
    """this week's spending history is saved as a list in the same order as categories list"""
    now = datetime.datetime.now()
    this_week_start = (now - datetime.timedelta(days=now.weekday())).replace(hour=0,minute=0,second=1)
    spendings = []
    for budget in budgets:
        amount = 0
        spendings_at_this_category = db(db.spending_history.category == budget['id']).select()
        for each in spendings_at_this_category:
            if (each.time_stamp - this_week_start).days < 7:
                amount += each.amount
        spendings.append(amount)
    return spendings


#############################################################################

######### this part handle all the savings to database ######################

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
    redirect(URL("default", "this_week"))
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
    try:
        amount = int(request.vars.amount)
        db.spending_history.insert(user_id=auth.user_id,
                                   category=request.vars.category_id,
                                   amount=amount,
                                   time_stamp=datetime.datetime.now())
        return "ok"
    except ValueError:
        return "wrong value"

##############################################################


############## this part handles all the deletions ###########
@auth.requires_signature()
def delete_budget_category():
    db(db.category.id == request.vars.category_id).delete()
    return "ok"

@auth.requires_signature()
def delete_fixed_spending():
    db(db.fixed_spending.id == request.vars.fixed_id).delete()
    return "ok"

#################################################################

############# this part comes with web2py #######################

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


