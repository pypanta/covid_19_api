from collections import defaultdict
from datetime import datetime
from urllib.error import URLError
from urllib.request import Request, urlopen
import csv
import functools
import getopt
import io
import json
import os
import re
import sys


covid_data_file = 'covid19_data.json'

def get_covid_data():
    """
    Download COVID-19 reports
    """
    req = Request('https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports')
    try:
        with urlopen(req) as response:
            html = response.read().decode('utf-8')
    except URLError as e:
        print(e.reason)
        raise

    links = re.findall(
        'CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_daily_reports.*\.csv(?=\")',
        html)

    if os.path.isfile(covid_data_file):
        with open(covid_data_file) as fh:
            old_data = json.load(fh)
    else:
        old_data = {}

    new_data = {}

    for link in links:
        link = f"https://raw.githubusercontent.com/{link.replace('/blob','')}"
        key = link.replace('.csv','').rpartition('/')[-1]

        if key not in old_data:
            print(f'Downloading covid-19 reports: {key}')
            req = Request(link)
            try:
                with urlopen(req) as response:
                    resp = response.read().decode('utf-8-sig')
            except URLError as e:
                print(e.reason)
                raise
            csv_reader = csv.DictReader(io.StringIO(resp), delimiter=',')

            passed = []
            for row in csv_reader:
                province = row.get('Province/State') or row.get('Province_State')
                country = row.get('Country/Region') or row.get('Country_Region')
                confirmed = int(row.get('Confirmed') or 0)
                deaths = int(row.get('Deaths') or 0)
                recovered = int(row.get('Recovered') or 0)
                active = int(row.get('Active', 0))
                last_update = row.get('Last Update') or row.get('Last_Update')
                latitude = row.get('Latitude') or row.get('Lat')
                longitude = row.get('Longitude') or row.get('Long_')
                combined_key = row.get('Combined_Key')
                if not new_data.get(key):
                    new_data[key]=[]
                if country not in passed:
                    if province:
                        new_data[key].append({
                            'Country_Region': country,
                            'Confirmed': confirmed,
                            'Deaths': deaths,
                            'Recovered': recovered,
                            'Active': active,
                            'Last_Update': last_update,
                            'Latitude': latitude,
                            'Longitude': longitude,
                            'Province_State': {province: {
                                             'Country_Region': country,
                                             'Confirmed': confirmed,
                                             'Deaths': deaths,
                                             'Recovered': recovered,
                                             'Active': active,
                                             'Last_Update': last_update,
                                             'Latitude': latitude,
                                             'Longitude': longitude,
                                             'Combined_Key': combined_key}}
                            })
                    else:
                        new_data[key].append({
                            'Country_Region': country,
                            'Confirmed': confirmed,
                            'Deaths': deaths,
                            'Recovered': recovered,
                            'Active': active,
                            'Last_Update': last_update,
                            'Latitude': latitude,
                            'Longitude': longitude,
                            })
                    passed.append(country)
                else:
                    for d in new_data[key]:
                        if country == d['Country_Region']:
                            d['Confirmed']+=confirmed
                            d['Deaths']+=deaths
                            d['Recovered']+=recovered
                            d['Active']+=active
                            if d.get('Province_State'):
                                d['Province_State'].update({province: {
                                                'Country_Region': country,
                                                'Confirmed': confirmed,
                                                'Deaths': deaths,
                                                'Recovered': recovered,
                                                'Active': active,
                                                'Last_Update': last_update,
                                                'Latitude': latitude,
                                                'Longitude': longitude,
                                                'Combined_Key': combined_key}})

    if new_data:
        old_data.update(new_data)
        with open(covid_data_file, "w", encoding='utf-8') as write_file:
            json.dump(old_data, write_file, indent=4)


@functools.lru_cache(maxsize=32)
def load_data():
    """
    Load COVID-19 data
    """
    if os.path.isfile(covid_data_file):
        mtime = os.path.getmtime(covid_data_file)
        when = datetime.fromtimestamp(mtime)
        now = datetime.now()
        td = now - when
        if td.seconds > 3600:
            print('Checking for updates... Please wait ☻\n')
            get_covid_data()
            os.utime(covid_data_file)
    else:
        get_covid_data()
    with open(covid_data_file) as fh:
        json_data = json.load(fh)
    return json_data


def get_countries(route=None, date=None):
    """
    All countries sorted by case name
    """
    all_data = load_data()
    if date:
        try:
            data = all_data[date]
        except KeyError:
            raise KeyError('There is no data for a given date.')
    else:
        data = all_data[list(all_data)[-1]]
    countries = {}
    for country in data:
        countries.update({country['Country_Region']: {
                                'Confirmed': country['Confirmed'],
                                'Deaths': country['Deaths'],
                                'Recovered': country['Recovered'],
                                'Active': country['Active'],
                                'Last_Update': country['Last_Update'],
                                'Latitude': country['Latitude'],
                                'Longitude': country['Longitude'],
                                'Province_State': country.get('Province_State')
                         }})
    if route == 'all':
        return all_data
    elif route == 'latest':
        return countries
    return {k:v for k, v in
            sorted(countries.items(), key=lambda i: i[1]['Confirmed'], reverse=True)}


def get_country(name, date=None):
    """
    One specific country by name
    """
    data = load_data()
    if date:
        try:
            countries = data[date]
        except KeyError:
            raise KeyError('There is no data for a given date.')
    else:
        countries = data[list(data)[-1]]

    country_data = {}
    for country in countries:
        if country['Country_Region'] == name:
            if country['Country_Region'] not in country_data.values():
                country_data['Country']=country['Country_Region']
                country_data['Confirmed']=country['Confirmed']
                country_data['Deaths']=country['Deaths']
                country_data['Recovered']=country['Recovered']
                country_data['Active']=country['Active']
                country_data['Last_Update']=country['Last_Update']
            else:
                country_data['Confirmed']+=country['Confirmed']
                country_data['Deaths']+=country['Deaths']
                country_data['Recovered']+=country['Recovered']
                country_data['Active']+=country['Active']
    return country_data


def get_top(case='Confirmed', num=10):
    """
    Top N countries by cases
    """
    case = case.title()
    data = load_data()
    top = {}
    for country in data[list(data)[-1]]:
        top[country['Country_Region']]=country[case]
    return {k:v for k, v in
            sorted(top.items(), key=lambda x: x[1], reverse=True)[:num]}


@functools.lru_cache(maxsize=32)
def get_new_cases(case='Confirmed'):
    """
    New cases by country
    """
    case = case.title()
    data = load_data()
    new = {}
    for country1 in data[list(data)[-1]]:
        for country2 in data[list(data)[-2]]:
            if country1['Country_Region'] == country2['Country_Region']:
                if country1[case] > country2[case]:
                    new[country1['Country_Region']]=(country1[case] - country2[case])
    return {k:v for k, v in sorted(new.items(), key=lambda i: i[1], reverse=True)}


def get_total():
    """
    Total number of cases
    """
    data = load_data()
    total = defaultdict(lambda:0)
    for country in data[list(data)[-1]]:
        total['Confirmed']+=country['Confirmed']
        total['Deaths']+=country['Deaths']
        total['Recovered']+=country['Recovered']
        total['Active']+=country['Active']
    return total


@functools.lru_cache(maxsize=32)
def mort_rate():
    """
    Mortality rate by country
    """
    data = load_data()
    countries = {}
    for country in data[list(data)[-1]]:
        countries.update({country['Country_Region']: {
                                'Confirmed': country['Confirmed'],
                                'Deaths': country['Deaths'],
                                }})
    return {k:countries[k]['Deaths']/countries[k]['Confirmed']*100 for k in
            sorted(countries, key=lambda i: countries[i]['Deaths']/countries[i]['Confirmed'],
                reverse=True)}


def diff(date1, date2):
    """
    Differences between two dates
    """
    data = load_data()
    data1 = data[date1]
    data2 = data[date2]
    countries = {}
    cases = ['Confirmed', 'Deaths', 'Recovered', 'Active']
    ck = {k['Combined_Key'] for k in data2}
    passed = []
    for c1 in data1:
        for c2 in data2:
            if c1['Combined_Key'] == c2['Combined_Key']:
                for case in cases:
                    if c1['Country_Region'] not in countries:
                        countries.update({c1['Country_Region']: {case:[c1[case], abs(c1[case]-c2[case])]}})
                    else:
                        if not countries[c1['Country_Region']].get(case):
                            countries[c1['Country_Region']][case]=[c1[case], abs(c1[case]-c2[case])]
                        else:
                            countries[c1['Country_Region']][case][0]+=c1[case]
                            countries[c1['Country_Region']][case][1]+=abs(c1[case]-c2[case])
            elif c1['Combined_Key'] not in ck and c1['Combined_Key'] not in passed:
                passed.append(c1['Combined_Key'])
                for case in cases:
                    if c1['Country_Region'] not in countries:
                        countries.update({c1['Country_Region']: {case:[c1[case], c1[case]]}})
                    else:
                        if not countries[c1['Country_Region']].get(case):
                            countries[c1['Country_Region']][case]=[c1[case], c1[case]]
                        else:
                            countries[c1['Country_Region']][case][0]+=c1[case]
                            countries[c1['Country_Region']][case][1]-=c1[case]
    return {k:v for k,v in sorted(countries.items(), key=lambda i: i[1]['Confirmed'][0], reverse=True)}
