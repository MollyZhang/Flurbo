from datetime import datetime

db.define_table('budget',
                Field('user_id', db.auth_user, default=auth.user_id),
                Field('name', 'string'),
                Field('amount', 'integer'),
                Field('start_date', 'string') # in the format of YYYYMMDD
                )

db.define_table('spending_history',
                Field('user_id', db.auth_user, default=auth.user_id),
                Field('budget_category', db.budget),
                Field('amount', 'integer'),
                Field('time_stamp','datetime')
                )

# db.spending_history.user_id.writable = db.spending_history.user_id.readable = False
# db.spending_history.id.writable = db.spending_history.id.readable = False


db.define_table('monthly_income',
                Field('user_id', db.auth_user, default=auth.user_id),
                Field('amount', 'integer'),
                Field('start_month', 'string') ## in the format of YYYYMM
                )

# fixed spending per month
db.define_table('fixed_spending',
                Field('user_id', db.auth_user, default=auth.user_id),
                Field('name', 'string'),
                Field('amount', 'integer'),
                Field('start_month','string') ## in the format of YYYYMM
                )



###### delete all records to db
# db(db.fixed_budget.id > 0).delete()
# db(db.changing_budget.id > 0).delete()
#
#
# ######## add one or more records to db as example
# db.fixed_budget.update_or_insert(user_id = auth.user_id)
# db.changing_budget.update_or_insert(user_id = auth.user_id)
