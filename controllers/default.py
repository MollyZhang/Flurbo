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
    db.spending_history.id.readable = db.spending_history.id.writable = False
    db.spending_history.user_id.readable = db.spending_history.writable = False
    # db.spending_history.user_id.writable = False

    # q1 = (db.spending_history.category == db.category.id)
    q2 = (db.spending_history.user_id == auth.user_id)
    grid = SQLFORM.grid(q2,create=False,deletable=False,editable=True,details=False,paginate=20)
    return dict(grid=grid)

@auth.requires_login()
def edit_budget():
    return dict()

@auth.requires_login()
def summary():
    # save budget history and spending history to txt file to be read later
    budgets = db(db.budget.user_id==auth.user_id).select()
    budget_history_file_name = save_budget_history_to_file(budgets, auth.user_id)
    spendings = db(db.spending_history.user_id==auth.user_id).select()
    spending_history_file_name = save_spending_history_to_file(spendings, auth.user_id)
    return dict(budget_history_file_name=budget_history_file_name)

def save_spending_history_to_file(spendings, user_id):
    pass




def save_budget_history_to_file(budgets, user_id):
    path="/Users/Molly/Desktop/CMPS183/web2py/web2py/applications/flurbo/static/data/"
    file_name = str(user_id) + "_budget_history_updated_" + str(datetime.datetime.now().date()) + ".txt"
    budget_dict = {}
    for budget in budgets:
        if budget.start_date not in budget_dict.keys():
            budget_dict[budget.start_date] = {budget.name:budget.amount}
        else:
            budget_dict[budget.start_date][budget.name] = budget.amount
    f = open(path+file_name, "w")
    first_line = "date"
    budget_names = get_all_budget_names(budgets)
    for budget_name in budget_names:
        first_line = first_line + "," + budget_name
    f.write(first_line + "\n")
    for date in sorted(budget_dict.keys()):
        correct_date_format = datetime.datetime.strptime(date, "%Y%m%d").strftime("%Y-%m-%d")
        new_line = correct_date_format
        for budget_name in budget_names:
            new_line = new_line + "," + str(budget_dict[date][budget_name])
        f.write(new_line + "\n")
    return file_name

def get_all_budget_names(budgets):
    names = []
    for budget in budgets:
        if budget.name not in names:
            names.append(budget.name)
    return sorted(names)



#############################################################################
######### This part loads data for the views#################################
#############################################################################

@auth.requires_login()
@auth.requires_signature()
def load_budget_data():
    now = datetime.datetime.now()
    this_month = now.strftime('%Y%m')
    this_Monday = (now - datetime.timedelta(days=now.weekday())).strftime('%Y%m%d')

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


@auth.requires_login()
@auth.requires_signature()
def load_week_data():
    now = datetime.datetime.now()
    this_Monday = (now - datetime.timedelta(days=now.weekday())).strftime('%Y%m%d')

    q1 = (db.budget.user_id==auth.user_id)
    q2 = (db.budget.start_date==this_Monday)
    preset_budget = db(q1 & q2).select().as_list()
    current_budget_category = get_current_budget_categories(preset_budget)


    spendings = db(db.spending_history.user_id==auth.user_id).select().as_list()
    this_week_spent = get_spent(spendings, current_budget_category)[1]
    previous_week_spent = get_spent(spendings, current_budget_category)[0]
    previous_budget_sum = get_previous_budget_sum(current_budget_category)
    current_available_budget = get_current_available_budget(preset_budget, previous_week_spent, previous_budget_sum)

    return response.json(dict(preset_budget=preset_budget,
                              this_week_spent=this_week_spent,
                              current_available_budget=current_available_budget))

def get_current_available_budget(preset_budget, previous_spent, previous_budget):
    current_available = {}
    for budget in preset_budget:
        name = budget['name']
        current_available[name] = previous_budget[name] - previous_spent[name] + budget['amount']
    return current_available

def get_current_budget_categories(budgets):
    categories = []
    for budget in budgets:
        categories.append(budget['name'])
    return categories

def get_previous_budget_sum(categories):
    """only return the past budget sum based on the given budget categories"""
    now = datetime.datetime.now()
    this_Monday = datetime.datetime.strptime(
        (now - datetime.timedelta(days=now.weekday())).strftime('%Y%m%d'), "%Y%m%d")
    budget_sum = {}
    for category in categories:
        budget_sum[category] = 0
    budgets = db(db.budget.user_id==auth.user_id).select()
    for budget in budgets:
        if datetime.datetime.strptime(budget.start_date, "%Y%m%d") >= this_Monday:
            pass
        else:
            if budget.name in categories:
                budget_sum[budget.name] += budget.amount
    return budget_sum

def get_spent(spendings, categories):
    """only return the current and past spendings based on the given budget categories """
    now = datetime.datetime.now()
    this_monday_mid_night = (now - datetime.timedelta(days=now.weekday())).replace(hour=0,minute=0,second=1)
    # initialize these two dictionary values to 0
    this_week_spent = {}
    previous_week_spent = {}
    for category in categories:
        this_week_spent[category] = 0
        previous_week_spent[category] = 0
    for spending in spendings:
        if spending['time_stamp'] < this_monday_mid_night:
            if spending['budget_category'] in categories:
                previous_week_spent[spending['budget_category']] += spending['amount']
        else:
            if spending['budget_category'] in categories:
                this_week_spent[spending['budget_category']] += spending['amount']
    return [previous_week_spent, this_week_spent]


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
    this_Monday = (now - datetime.timedelta(days=now.weekday())).strftime('%Y%m%d')
    income = int(request.vars.income)
    db.monthly_income.insert(user_id=user_id, amount=income,start_month=this_month)
    budgets = json.loads(request.vars.budgets)
    for budget in budgets:
        db.budget.insert(user_id=user_id, name=budget['name'],
                         amount=int(budget['amount']), start_date=this_Monday)
    fixed_spendings = json.loads(request.vars.fixed_spendings)
    for spending in fixed_spendings:
        db.fixed_spending.insert(user_id=user_id, name=spending['name'],
                                 amount=int(spending['amount']), start_month=this_month)
    return "ok"


@auth.requires_login()
@auth.requires_signature()
def save_edit():
    """update data for next week/month to database by deleting old ones and inserting new ones"""
    now = datetime.datetime.now()
    this_Monday = now - datetime.timedelta(days=now.weekday())
    next_Monday = (this_Monday + datetime.timedelta(days=7)).strftime("%Y%m%d")
    next_month = get_next_month(now)

    income_query1 = (db.monthly_income.user_id == auth.user_id)
    income_query2 = (db.monthly_income.start_month == next_month)
    budget_query1 = (db.budget.user_id ==auth.user_id)
    budget_query2 = (db.budget.start_date == next_Monday)
    fixed_query1 = (db.fixed_spending.user_id ==auth.user_id)
    fixed_query2 = (db.fixed_spending.start_month == next_month)
    db(income_query1 & income_query2).delete()
    db(budget_query1 & budget_query2).delete()
    db(fixed_query1 & fixed_query2).delete()

    income = int(request.vars.future_income)
    db.monthly_income.insert(user_id=auth.user_id, amount=income,start_month=next_month)
    budgets = json.loads(request.vars.future_budgets)
    for budget in budgets:
        db.budget.insert(user_id=auth.user_id, name=budget['name'],
                         amount=int(budget['amount']), start_date=next_Monday)
    fixed_spendings = json.loads(request.vars.future_fixed_spendings)
    for spending in fixed_spendings:
        db.fixed_spending.insert(user_id=auth.user_id, name=spending['name'],
                                 amount=int(spending['amount']), start_month=next_month)
    return "ok"


@auth.requires_login()
@auth.requires_signature()
def save_spending_history():
    db.spending_history.insert(user_id=auth.user_id,
                               budget_category=request.vars.budget_category,
                               amount=int(request.vars.amount),time_stamp=datetime.datetime.now())
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


