from flask import Flask, redirect, url_for, request, render_template, jsonify
from worker import celery
import celery.states as states
import os
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/loan", methods=["POST"])
def loan():
    result = request.form.to_dict()
    result['amount'] = float(result['amount'])
    result['income'] = float(result['income'])
    result['terms'] = int(result['terms'])

    print(result)

    task = celery.send_task('tasks.loan', args=[result], kwargs={})
    response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
    return response


@app.route("/loan/<string:task_id>")
def check_task(task_id: str) -> str:
    res = celery.AsyncResult(task_id)

    result = {
        'id': task_id,
        'status': None,
        'result': None,
        'refused_policy': None,
        'amount': None,
        'terms': None
    }

    if res.state == states.PENDING:
        pending_result = fill_result(result, {'status': 'processing'})

        return jsonify(pending_result)
    else:
        final_result = fill_result(result, res.result)

        return jsonify(final_result)


def fill_result(result, fields):

    for field in fields.keys():
        result[field] = fields[field]

    return result



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
