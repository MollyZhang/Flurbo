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

@auth.requires_login()
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
#############################################################################

@auth.requires_login()
@auth.requires_signature()
def load_data():
    now = datetime.datetime.now()
    this_month = now.strftime('%Y%m')
    this_Monday = now.strftime('%Y%m%d')
    next_month = get_next_month(now)
    next_Monday = (now + datetime.timedelta(days=7)).strftime('%Y%m%d')

    income_query1 = (db.monthly_income.user_id == auth.user_id)
    income_query2 = (db.monthly_income.start_month == this_month)
    income_query3 = (db.monthly_income.start_month == next_month)
    current_income = db(income_query1&income_query2).select().as_list()
    future_income = db(income_query1&income_query3).select().as_list()
    if len(future_income) == 0:
        future_income = current_income

    budget_query1 = (db.budget.user_id ==auth.user_id)
    budget_query2 = (db.budget.start_date == this_Monday)
    budget_query3 = (db.budget.start_date == next_Monday)
    current_budgets = db(budget_query1&budget_query2).select().as_list()
    future_budgets = db(budget_query1&budget_query3).select().as_list()
    if len(future_budgets) == 0:
        future_budgets = current_budgets

    fixed_query1 = (db.fixed_spending.user_id ==auth.user_id)
    fixed_query2 = (db.fixed_spending.start_month == this_month)
    fixed_query3 = (db.fixed_spending.start_month == next_month)
    current_fixed_spendings = db(fixed_query1 & fixed_query2).select().as_list()
    future_fixed_spendings = db(fixed_query1 & fixed_query3).select().as_list()
    if len(future_fixed_spendings) == 0:
        future_fixed_spendings = current_fixed_spendings

    return response.json(dict(current_income=current_income, future_income=future_income,
                              current_budgets=current_budgets, future_budgets=future_budgets,
                              current_fixed_spendings=current_fixed_spendings,
                              future_fixed_spendings=future_fixed_spendings))


def get_next_month(now):
    beginning_of_this_month = now.replace(day=1, hour=0, minute=0, second=1)
    days_in_this_month = calendar.monthrange(now.year, now.month)[1]
    next_month = beginning_of_this_month + datetime.timedelta(days=days_in_this_month)
    return next_month.strftime('%Y%m')


def get_this_week_budget(budgets):
    this_week = []
    now = datetime.datetime.now()
    for budget in budgets:
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
#############################################################################


@auth.requires_login()
@auth.requires_signature()
def save_initial():
    """save the initial income, budget and fixed_spending to database """
    user_id = auth.user_id
    now = datetime.datetime.now()
    this_month = now.strftime('%Y%m')
    this_Monday = now.strftime('%Y%m%d')
    # save initial income to db
    income = int(request.vars.income)
    db.monthly_income.insert(user_id=user_id, amount=income,start_month=this_month)
    # save initial budgets to db
    budgets = json.loads(request.vars.budgets)
    for budget in budgets:
        db.budget.insert(user_id=user_id, name=budget['name'],
                         amount=int(budget['amount']), start_date=this_Monday)
    # save initial fixed spending to db
    fixed_spendings = json.loads(request.vars.fixed_spendings)
    for spending in fixed_spendings:
        db.fixed_spending.insert(user_id=user_id, name=spending['name'],
                                 amount=int(spending['amount']), start_month=this_month)

    return "ok"


@auth.requires_login()
@auth.requires_signature()
def save_edit():
    """save the income (for the next month), budget (for the next week) and
    fixed_spending (for the next month) to database"""
    print request.vars


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
# @auth.requires_signature()
# def delete_budget_category():
#     db(db.category.id == request.vars.category_id).delete()
#     return "ok"
#
# @auth.requires_signature()
# def delete_fixed_spending():
#     db(db.fixed_spending.id == request.vars.fixed_id).delete()
#     return "ok"

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


