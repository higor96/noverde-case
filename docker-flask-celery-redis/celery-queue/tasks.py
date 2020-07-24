import os
import time
import requests
import json
from dateutil.relativedelta import relativedelta
from datetime import datetime
from celery import Celery


CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

api_key = 'z2qcDsl6BK8FEPynp2ND17WvcJKMQTpjT5lcyQ0d'

@celery.task(name='tasks.loan')
def loan(param):
    time.sleep(5)

    accepted_score = 600
    accepted_age = 18

    age = check_age(param['birthdate'])
    score = check_score(param['cpf'])
    commitment = check_commitment(param['cpf'])

    if age < accepted_age:
        return {'result': 'refused', 'refused_policy': 'age', 'status': 'completed'}

    if score < accepted_score:
        return {'result': 'refused', 'refused_policy': 'score', 'status': 'completed'}
    else:
        commitment_result = evaluate_commitment(score, commitment, param['terms'], param['amount'], param['income'])

        if not commitment_result['accepted']:
            return {'result': 'refused', 'refused_policy': 'commitment', 'status': 'completed'}
        else:
            return {'result': 'approved', 'terms': commitment_result['terms'], 'amount': param['amount'], 'status': 'completed'}


def check_age(birthdate):

    birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
    today = datetime.today()

    age = relativedelta(today, birthdate).years

    return age


def check_score(cpf):

    url="https://challenge.noverde.name/score"
    response = requests.post(url=url, headers={"x-api-key": api_key}, data=json.dumps({"cpf": cpf}))

    score = json.loads(response.text)['score']
    
    return score


def check_commitment(cpf):

    url="https://challenge.noverde.name/commitment"
    response = requests.post(url=url, headers={"x-api-key": api_key}, data=json.dumps({"cpf": cpf}))

    commitment = json.loads(response.text)['commitment']
    
    return commitment

def evaluate_commitment(score, commitment, terms, amount, income):

    accepted = False
    terms_range = [6, 9, 12]

    while terms in terms_range and accepted is False:

        term_value = calc_term_value(score, terms, amount)
        diff = income*(1 - commitment) - term_value

        if diff >= 0:
            accepted = True
        else:
            terms = terms + 3

    return {'accepted': accepted, 'terms': terms}



def calc_term_value(score, terms, amount):

    tax = get_tax(score, terms)

    num = ((1 + tax)**terms)*(tax)
    den = ((1 + tax)**terms)-(tax)
    term_value = amount*(num/den) 

    return term_value


def get_tax(score, terms):

    if score >= 900:
        dict_tax = {
            6: 0.039,
            9: 0.042,
            12: 0.045
        }

    if 800 <= score < 900:
        dict_tax = {
            6: 0.047,
            9: 0.050,
            12: 0.053
        }

    if 700 <= score < 800:
        dict_tax = {
            6: 0.055,
            9: 0.058,
            12: 0.061
        }

    if 600 <= score < 700:
        dict_tax = {
            6: 0.064,
            9: 0.066,
            12: 0.069
        }

    return dict_tax[terms]
    






