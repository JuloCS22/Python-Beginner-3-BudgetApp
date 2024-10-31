from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

incomes = {
    'Salary' : 1500,
    'Rental' : 300
}

expenses = {
    'Rent' : 800,
    'Groceries' : 300,
    'Internet' : 50,
    'Phone' : 30
}


@app.route('/', methods=['GET', 'POST'])
def hello_world():  # put application's code here

    new_income_label = request.form.get('label_income')
    new_income_amount = request.form.get('add_income')
    new_expense_label = request.form.get('label_expense')
    new_expense_amount = request.form.get('add_expense')

    if new_income_label and new_income_amount:
        incomes.update({str(new_income_label): int(new_income_amount)})

    if new_expense_label and new_expense_amount:
        expenses.update({str(new_expense_label): int(new_expense_amount)})

    total_incomes = sum(incomes.values())
    total_expenses = sum(expenses.values())
    money_left = total_incomes - total_expenses

    labels = list(expenses.keys())
    values = list(expenses.values())

    fig, ax = plt.subplots(figsize=(6, 4), subplot_kw=dict(aspect='equal'))
    plt.tight_layout()
    def func(pct, allvals):
        absolute = int(np.round(pct/100.*np.sum(allvals)))
        return f"{pct:.2f}%"

    wedges, texts, autotexts = ax.pie(values, labels=labels, autopct=lambda pct: func(pct, values),
                                      textprops=dict(color='w'))

    ax.legend(wedges, labels,
              title = "Expenses",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")

    ax.set_title("Expenses : Pie Chart")

    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight', pad_inches=0)
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template(
        'home.html',
        incomes=incomes,
        expenses=expenses,
        total_expenses=total_expenses,
        total_incomes=total_incomes,
        money_left=money_left,
        plot_url=plot_url
    )


if __name__ == '__main__':
    app.run()
