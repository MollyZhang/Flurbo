from datetime import datetime

db.define_table('category',
                Field('user_id', db.auth_user, default=auth.user_id),
                Field('name', 'string'),
                Field('budget', 'integer'),
                )

db.define_table('budget_history',
                Field('user_id', db.auth_user, default=auth.user_id),
                Field('category', db.category),
                Field('start_time', 'datetime'),
                Field('end_time', 'datetime'),
                Field('budget', 'integer'),
                )

db.define_table('spending_history',
                Field('user_id', db.auth_user, default=auth.user_id),
                Field('category', db.category),
                Field('amount', 'integer'),
                Field('time_stamp','datetime')
                )

db.spending_history.amount.requires = IS_INT_IN_RANGE(0,100000)



db.spending_history.amount.requires = IS_INT_IN_RANGE(0,100000)


db.define_table('monthly_income',
                Field('user_id', db.auth_user, default=auth.user_id),
                Field('amount', 'integer'),
                )

# fixed spending per month
db.define_table('fixed_spending',
                Field('user_id', db.auth_user, default=auth.user_id),
                Field('name', 'string'),
                Field('amount', 'integer'),
                )

# keep track of new users and old users.
db.define_table('initialization',
                Field('user_id', db.auth_user),
                Field('initialized', 'boolean', default="False")
                )



###### delete all records to db
# db(db.fixed_budget.id > 0).delete()
# db(db.changing_budget.id > 0).delete()
#
#
# ######## add one or more records to db as example
# db.fixed_budget.update_or_insert(user_id = auth.user_id)
# db.changing_budget.update_or_insert(user_id = auth.user_id)

db(db.spending_history.amount == None).delete()