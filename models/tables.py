db.define_table('changing_budget',
                Field('user_id', db.auth_user),
                Field('c1', default='food_and_drink'),
                Field('c2', default='medical_health_related'),
                Field('c3', default='transportation'),
                Field('c4', default='education'),
                Field('c5', default='entertainment'),
                Field('c6', default="new category1"),
                Field('c7', default="new category2"),
                Field('c8', default="new category3"),
                Field('c9', default="new category4"),
                )

db.define_table('fixed_budget',
                Field('user_id', db.auth_user),
                Field('c1', default='rent'),
                Field('c2', default='car_insurance_registration'),
                Field('c3', default='sportify_subscription'),
                )

db.define_table('monthly_income',
                Field('user_id', db.auth_user),
                Field('source1'),
                Field('source2'),
                Field('source3'),
                )


# how do one link the day spending in each categories with the budget-category table
db.define_table('day_spending',
                Field('user_id', db.auth_user),
                Field('food_and_drink'),
                Field('medical_health_related'),
                Field('transportation'),
                Field('education'),
                Field('entertainment'),
                )


db.define_table('week_history',
                Field('user_id', db.auth_user),
                Field('Monday', db.day_spending),
                Field('Tuesday', db.day_spending),
                Field('Wednesday', db.day_spending),
                Field('Thursday', db.day_spending),
                Field('Friday', db.day_spending),
                Field('Saturday', db.day_spending),
                Field('Sunday', db.day_spending),
                )

db.define_table('month_history',
                Field('user_id', db.auth_user),
                Field('week1', db.week_history),
                Field('week2', db.week_history),
                Field('week3', db.week_history),
                Field('week4', db.week_history),
                Field('week5', db.week_history),
                )

db.define_table('year_history',
                Field('user_id', db.auth_user),
                Field('year_number'),
                Field('January', db.month_history),
                Field('February', db.month_history),
                Field('March', db.month_history),
                Field('April', db.month_history),
                Field('May', db.month_history),
                Field('June', db.month_history),
                Field('July', db.month_history),
                Field('August', db.month_history),
                Field('September', db.month_history),
                Field('October', db.month_history),
                Field('November', db.month_history),
                Field('December', db.month_history),
                )

# ###### delete all records to db
# db(db.fixed_budget.id > 0).delete()
# db(db.changing_budget.id > 0).delete()
#
#
# ######## add one or more records to db as example
# db.fixed_budget.update_or_insert(user_id = auth.user_id)
# db.changing_budget.update_or_insert(user_id = auth.user_id)

