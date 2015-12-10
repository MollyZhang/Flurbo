from datetime import datetime

db.define_table('budget',
                Field('user_id', db.auth_user, default=auth.user_id),
                Field('name', 'string'),
                Field('amount', 'integer'),
                Field('start_date', 'string') # in the format of YYYYMMDD
                )

db.define_table('monthly_income',
                Field('user_id', db.auth_user, default=auth.user_id),
                Field('amount', 'integer'),
                Field('start_month', 'string') ## in the format of YYYYMM
                )

db.define_table('fixed_spending',
                Field('user_id', db.auth_user, default=auth.user_id),
                Field('name', 'string'),
                Field('amount', 'integer'),
                Field('start_month','string') ## in the format of YYYYMM
                )

db.define_table('spending_history',
                Field('user_id', db.auth_user, default=auth.user_id),
                Field('budget_category', 'string'),
                Field('amount', 'integer'),
                Field('time_stamp','datetime')
                )

# on foreign key constraint error, drop the table and add it again would solve the problem
# db.spending_history.drop()