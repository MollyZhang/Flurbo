import datetime
import json
import calendar
import os


############### This part is the controller for all views #################

@auth.requires_login()
def index():
    return dict()

@auth.requires_login()
def this_week():
    return dict()

@auth.requires_signature()
def edit():
    return dict()

@auth.requires_login()
def spending_history():
    db.spending_history.category.readable = True
    db.spending_history.user_id.readable = False
    db.spending_history.user_id.writable = False

    # q1 = (db.spending_history.category == db.category.id)
    q2 = (db.spending_history.user_id == auth.user_id)
    grid = SQLFORM.grid(q2,create=False,deletable=False,editable=True,details=False,paginate=20,
                        fields=[db.spending_history.category,
                                db.spending_history.amount,
                                db.spending_history.time_stamp])
    return dict(grid=grid)

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
    budget_this_week = get_this_week_budget(categories)
    print income
    return response.json(dict(categories=budget_this_week,
                              fixed_spendings=fixed_spendings,
                              income=income,
                              spendings=spendings_by_user_this_week))

def get_this_week_budget(categories):
    this_week = []
    now = datetime.datetime.now()
    for budget in categories:
        if (now - budget['start_time']).days >= 0 and (now-budget['start_time']).days <= 7:
            this_week.append(budget)
    return this_week

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
def save_all():
    print "hey I am called"
    initial = json.loads(request.vars.initial)
    income = request.vars.income
    fixed_spendings = json.loads(request.vars.fixed_spendings)
    budgets = json.loads(request.vars.budgets)
    save_income(income, auth.user_id)
    now = datetime.datetime.now()
    this_monday = (now - datetime.timedelta(days=now.weekday())).replace(hour=0,minute=0,second=1)
    next_monday = this_monday + datetime.timedelta(days=7)
    beginning_of_this_month = now.replace(day=1, hour=0, minute=0, second=1)
    days_in_this_month = calendar.monthrange(now.year, now.month)[1]
    beginning_of_next_month = now + datetime.timedelta(days=days_in_this_month)
    if initial:
        save_initial_budget(budgets, auth.user_id, this_monday)
        save_initial_fixed_spending(fixed_spendings,auth.user_id,beginning_of_this_month)
    else:
        save_next_week_budget(budgets, auth.user_id, next_monday)
        save_next_month_fixed(fixed_spendings, auth.user_id, beginning_of_next_month)
    return "ok"

def save_income(income, user_id):
    db.monthly_income.update_or_insert(db.monthly_income.user_id==user_id,
        user_id=user_id, amount=int(income))

def save_initial_fixed_spending(fixed_spendings, user_id, time):
    for spending in fixed_spendings:
        db.fixed_spending.insert(user_id=auth.user_id,
                                 name=spending['name'],
                                 amount=int(spending['amount']),
                                 start_time=time)

def save_initial_budget(budgets, user_id, this_monday):
    for budget in budgets:
            db.category.insert(user_id=auth.user_id,
                               name=budget['name'],
                               budget=int(budget['budget']),
                               start_time=this_monday)

def save_next_week_budget(budgets, user_id, next_monday):
    for budget in budgets:
        q1 = (db.category.user_id==user_id)
        q2 = (db.category.name == budget['name'])
        q3 = (db.category.start_time == next_monday)
        db.category.update_or_insert(q1 & q2 & q3,
                                     user_id=user_id,
                                     name=budget['name'],
                                     budget=int(budget['budget']),
                                     start_time=next_monday)


def save_next_month_fixed(fixed_spendings, user_id, time):
    for spending in fixed_spendings:
        q1 = (db.fixed_spending.user_id==user_id)
        q2 = (db.fixed_spending.name == spending['name'])
        q3 = (db.fixed_spending.start_time == time)
        db.fixed_spending.update_or_insert(q1 & q2 & q3,
                                     user_id=user_id,
                                     name=spending['name'],
                                     amount=int(spending['amount']),
                                     start_time=time)

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


