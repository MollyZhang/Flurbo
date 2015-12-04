db.define_table('category',
                Field('user_id', db.auth_user, default=auth.user_id),
                Field('name'),
                Field('budget'),
                )

db.define_table('budget_history',
                Field('user_id', db.auth_user, default=auth.user_id),
                Field('category', db.category),
                Field('start_time'),
                Field('end_time'),
                Field('budget'),
                )

db.define_table('spending_history',
                Field('user_id', db.auth_user, default=auth.user_id),
                Field('category', db.category),
                Field('amount'),
                Field('transaction_date'),
                Field('note')
                )

db.define_table('monthly_income',
                Field('user_id', db.auth_user, default=auth.user_id),
                Field('amount'),
                )

# fixed spending per month
db.define_table('fixed_spending',
                Field('user_id', db.auth_user, default=auth.user_id),
                Field('name'),
                Field('amount'),
                )

###### delete all records to db
# db(db.fixed_budget.id > 0).delete()
# db(db.changing_budget.id > 0).delete()
#
#
# ######## add one or more records to db as example
# db.fixed_budget.update_or_insert(user_id = auth.user_id)
# db.changing_budget.update_or_insert(user_id = auth.user_id)

