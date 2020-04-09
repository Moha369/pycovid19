import time
import requests
from pycovid19.exceptions import *

base_url = 'https://thevirustracker.com/free-api'

class Statistics:
    def __init__(self, base = base_url):
        self.base = base

    def api_request(self, method, kwargs : dict, path = None):
        if path:
            absolute_path = self.base + path
        else:
            absolute_path = self.base
        if method.lower() == 'get':
            r = requests.get(absolute_path, params = kwargs)
            return r
        else:
            r = requests.post(absolute_path, data = kwargs)
            return r
    @property
    def total_cases(self):
        r = self.api_request('get', kwargs = {'global' : 'stats'})
        cases = r.json()['results'][0]['total_cases']
        return int(cases)

    @property
    def cases_today(self):
        r = self.api_request('get', kwargs = {'global' : 'stats'})
        cases = r.json()['results'][0]['total_new_cases_today']
        return int(cases)

    @property
    def total_recoveries(self):
        r = self.api_request('get', kwargs = {'global' : 'stats'})
        recoveries = r.json()['results'][0]['total_recovered']
        return int(recoveries)

    @property
    def total_active(self):
        r = self.api_request('get', kwargs = {'global' : 'stats'})
        cases = r.json()['results'][0]['total_active_cases']
        return int(cases)

    @property
    def total_serious(self):
        r = self.api_request('get', kwargs = {'global' : 'stats'})
        cases = r.json()['results'][0]['total_serious_cases']
        return int(cases)

    @property
    def total_affected_countries(self):
        r = self.api_request('get', kwargs = {'global' : 'stats'})
        countries = r.json()['results'][0]['total_affected_countries']
        return int(countries)

    @property
    def total_deaths(self):
        r = self.api_request('get', kwargs = {'global' : 'stats'})
        deaths = r.json()['results'][0]['total_deaths']
        return int(deaths)

    @property
    def deaths_today(self):
        r = self.api_request('get', kwargs = {'global' : 'stats'})
        deaths = r.json()['results'][0]['total_new_deaths_today']
        return int(deaths)

    @property
    def countries_info(self):
        r = self.api_request('get', kwargs = {'countryTotals' : 'ALL'})
        res = r.json()
        _all = res['countryitems'][0]
        countries = []
        for i in range(1, 400):
            try:
                country_name = _all[str(i)]['title']
                country_code = _all[str(i)]['code']
                country_dict = {'name': country_name, 'code': country_code}
                countries.append(country_dict)
            except KeyError:
                break
        return countries

    def by_country(self, country_code):
        countries = self.countries_info
        for country in countries:
            if country['code'] == country_code.upper():
                found = True
            else:
                continue
        if not found:
            raise CountryNotValidError('Country code not valid, please refer to `countries_info` method to check the list of countries.')
        r = self.api_request('get', kwargs = {'countryTotal' : country_code.upper()})
        data = r.json()['countrydata'][0]

        info = dict(total_cases = data['total_cases'],
        recovered = data['total_recovered'],
        total_deaths = data['total_deaths'],
        new_cases = data['total_new_cases_today'],
        new_deaths = data['total_new_deaths_today'],
        total_active_cases = data['total_active_cases'],
        total_serious = data['total_serious_cases'],
        global_rank = data['total_danger_rank'])

        return info
cls = Statistics()
print(cls.by_country('SA')['total_cases'])
