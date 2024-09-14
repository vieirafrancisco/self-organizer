from flask import Blueprint

main = Blueprint('main', __name__)


@main.route('/')
def init():
    return 'Olá mundo'
