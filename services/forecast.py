def forecast_date(current_income, target_income, monthly_growth=0.05):
    months = 0
    income = current_income
    while income < target_income:
        income *= (1 + monthly_growth)
        months += 1
        if months > 600:
            break
    return months
