#калькулятор рассчета ежемесячного взноса по кредиту
from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, ValidationError, NumberRange
from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NKJNIsns64da'

class MortgageCalculatorForm(FlaskForm):#класс формы для калькулятора ипотеки
    loan_amount = IntegerField( validators=[DataRequired(), NumberRange(min=1)], render_kw={"placeholder": "Сумма кредита"})#сумма
    interest_rate = IntegerField(validators=[DataRequired(), NumberRange(min=1)], render_kw={"placeholder": "Процентная ставка"})#проценты
    loan_term = IntegerField( validators=[DataRequired(), NumberRange(min=1)], render_kw={"placeholder": "Срок кредита"})#срок

    submit = SubmitField('Рассчитать')

@app.route('/', methods=['GET', 'POST'])
def mortgage_calculator():
    form = MortgageCalculatorForm()# создаем форму
    if form.validate_on_submit():#в случае если форма нормальная
        loan_amount = form.loan_amount.data
        interest_rate = form.interest_rate.data / 100 / 12 # Преобразуем в месячную ставку
        loan_term_months = form.loan_term.data * 12 # Преобразуем в месяцы

        monthly_payment = (# аннуитентная
            loan_amount * interest_rate / (1 - (1 + interest_rate) ** -loan_term_months)
        )

        return render_template('mortage_result.html', monthly_payment=monthly_payment)

    return render_template('mortage_calculator.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)