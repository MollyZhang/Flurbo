/**
 * Created by Molly on 12/7/15.
 */
$(function() {
    var MAIN = new Ractive({
        el: '#target',
        template: '#template',
        delimiters: ['{%', '%}'],
        tripleDelimiters: ['{%%', '%%}'],
        data: {
            adding_income: false,
            adding_budget: false,
            adding_fixed: false,
            budget_under_edit: -1,
            fixed_under_edit: -1,
            income: 0,
            categories: [],
            fixed_spendings: [],
            total: 0
        }
    });

    $.ajax("{{=URL('default', 'load_data', user_signature=True)}}",
        {
        method: 'POST',
        success: function (data) {
            if (data['income']) {
                window.location.href = "{{=URL('default','this_week')}}";
            }
            MAIN.set('categories', data['categories']);
            MAIN.set('fixed_spendings', data['fixed_spendings']);
            MAIN.set('total', calculate_total_budget());
            }
        }
  );

    function calculate_total_budget() {
        var total = 0;
        fixed = MAIN.get('fixed_spendings');
        budgets = MAIN.get('categories');
        for (i=0; i<fixed.length; ++i) {
            total += parseInt(fixed[i]['amount'])
        }
        for (i=0; i<budgets.length; ++i) {
            total += parseInt(budgets[i]['budget'])* 30 / 7
        }
        return Math.round(total);
    }

    MAIN.on('add-budget', function(){
        MAIN.set('adding_budget', true);
    });

    MAIN.on('save-budget', function(){
        var name = $('#category_name').val();
        var amount = $('#category_budget').val();
        MAIN.set('adding_budget', false);
        var new_category = {"name": name, "budget": amount};
        var updated_category = MAIN.get('categories');
        updated_category.push(new_category);
        MAIN.set('categories', updated_category);
        MAIN.set('total', calculate_total_budget());
    });

    MAIN.on("save_income", function() {
        MAIN.set("adding_income", false);
        income = MAIN.get('income');
    });
    MAIN.on("edit_income", function() {
        MAIN.set("adding_income", true);
    });

    MAIN.on('add_fixed', function(){
        MAIN.set('adding_fixed', true);
    });

    MAIN.on('save_fixed', function(){
        var name = $('#spending_name').val();
        var amount = $('#spending_amount').val();
        MAIN.set('adding_fixed', false);
        var new_spending = {"name": name, "amount": amount};
        var updated_spending = MAIN.get('fixed_spendings');
        updated_spending.push(new_spending);
        MAIN.set('fixed_spendings', updated_spending);
        MAIN.set('total', calculate_total_budget());
    });

    MAIN.on("delete_budget", function(e) {
        var index = $(e.original.target).data('index');
        categories = MAIN.get('categories');
        target_category = categories[index];
        categories.splice(index,1);
        MAIN.set('categories', categories);
        MAIN.set('total', calculate_total_budget());
    });

    MAIN.on("edit_budget", function(e) {
        var index = $(e.original.target).data('index');
        MAIN.set('budget_under_edit', index);
    });

    MAIN.on("save-budget-edit", function(e) {
        MAIN.set('budget_under_edit', -1);
        MAIN.set('total', calculate_total_budget());

    })

    MAIN.on("delete_fixed", function(e) {
        var index = $(e.original.target).data('index');
        fixed = MAIN.get('fixed_spendings');
        target_fixed = fixed[index];
        fixed.splice(index,1);
        MAIN.set('fixed_spendings', fixed);
        MAIN.set('total', calculate_total_budget());
    });

    MAIN.on("edit_fixed", function(e) {
        var index = $(e.original.target).data('index');
        MAIN.set('fixed_under_edit', index);
    });

    MAIN.on("save-fixed-edit", function(e) {
        MAIN.set('fixed_under_edit', -1);
        MAIN.set('total', calculate_total_budget());

    });

    MAIN.on('save-all', function() {
        fixed_spendings = MAIN.get('fixed_spendings');
        income = MAIN.get('income');
        categories = MAIN.get('categories');
        $.ajax("{{=URL('default', 'save_all', user_signature=True)}}",
            {
            method: 'POST',
            data: {
                fixed_spendings: JSON.stringify(fixed_spendings),
                budgets: JSON.stringify(categories),
                income: income
                }
            }
        );
        window.location.href="{{=URL('default','this_week')}}";
    });

});
