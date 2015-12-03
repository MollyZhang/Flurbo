db.define_table('fixed_budget',
                Field('user_id', db.auth_user),
                Field('food_and_drink'),
                Field('medical_health_related'),
                Field('transportation'),
                Field('education'),
                Field('entertainment')
                )

db.define_table('changing_budget_category',
                Field('user_id', db.auth_user),
                Field('rent'),
                Field('car_insurance_registration'),
                Field('sportify_subscription'),
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
