import urllib.request
import json

from flask import Blueprint, Flask, jsonify, render_template, request, session
from flask_babel import gettext as _

from utils.services import get_countries, get_new_cases, get_top, mort_rate, get_total, get_country
from settings import LANGUAGES
from main import babel


covid = Blueprint('covid', __name__, template_folder='templates')


@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'en')
    #return request.accept_languages.best_match(LANGUAGES.keys())
    #return 'sr'


@covid.route('/')
@covid.route('/api/', endpoint='api')
@covid.route('/api/latest/', endpoint='latest')
def home():
    # user_ip = request.environ['REMOTE_ADDR']
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    with urllib.request.urlopen(
            'https://freegeoip.app/json/' + user_ip) as response:
        country_data = json.loads(response.read().decode('utf8'))

    if request.endpoint == 'covid.home':
        total = get_total()
        country = get_country(country_data['country_name'])
        top_confirmed = get_top()
        top_deaths = get_top('Deaths')
        top_recovered = get_top('Recovered')
        new_confirmed = get_new_cases()
        new_deaths = get_new_cases('Deaths')
        new_recovered = get_new_cases('Recovered')
        countries = get_countries()
        return render_template('home.html',
            total=total,
            country=country,
            countries=countries,
            top_confirmed=top_confirmed,
            top_deaths=top_deaths,
            top_recovered=top_recovered,
            new_confirmed=new_confirmed,
            new_deaths=new_deaths,
            new_recovered=new_recovered,
            mort_rate=mort_rate())
    else:
        if request.endpoint == 'covid.api':
            if request.args.get('date'):
                date = request.args.get('date')
                countries = get_countries(date=date)
            elif request.args.get('name'):
                name = request.args.get('name')
                date = request.args.get('cdate', None)
                countries = get_country(name=name, date=date)
            else:
                countries = get_countries('all')
        elif request.endpoint == 'covid.latest':
            countries = get_countries('latest')
        return jsonify(countries)


@covid.route('/api/top/')
def top():
    if request.args.get('case'):
        case = request.args.get('case').title()
    else:
        case = 'Confirmed'
    if request.args.get('num'):
        num = int(request.args.get('num'))
    else:
        num = 10
    top_countries = get_top(case, num)
    return jsonify(top_countries)

@covid.route('/api/new/')
def new():
    if request.args.get('case'):
        case = request.args.get('case').title()
        print(case)
        new_cases = get_new_cases(case)
    else:
        new_cases = get_new_cases()
    return jsonify(new_cases)


@covid.route('/about')
def about():
    return _('About')
