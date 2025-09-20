from datetime import date, datetime, timedelta
from requests import post
from requests.structures import CaseInsensitiveDict

class Access:
    def __init__(self, email, pwd):
        token = Token(email, pwd)
        self.signal = Signal(token)
        self.ticker = Ticker(token)

class Net:
    # URL = 'https://lefuture.kr/futurebot/api'
    URL = 'http://localhost:8080/api' #개발용

    def success(self, response) -> bool:
        json = self.response(response)
        try:
            return False if json is None else json['success']
        except KeyError:
            return False

    @classmethod
    def response(cls, response):
        if response.status_code == 200:
            json = response.json()
            if len(json['msg']) > 0:
                print('pat data response message:', json['msg'])

            if json['result'] > 0:
                return json['data']

        return None

class Signal(Net):
    ADD = '/pat/data/adds'
    REMOVE = '/pat/data/removes'
    REMOVE_DT = '/pat/data/removes/date'
    SEARCH = '/pat/search'
    SAMPLE = '/pat/sample'

    class Sort:
        PM = 'perma'
        TK = 'ticker'
        NM = 'name'
        EN_DT = 'date'
        EN_PRC = 'enterPrice'
        EN_TRD = 'enterTradeVal'
        EX_DT = 'exitDate'
        EX_PRC = 'exitPrice'
        EX_TRD = 'exitTradeVal'
        RP = 'returnPer'
        RV = 'revision'
        CR = 'creation'

    def __init__(self, token):
        self.token: Token = token

    def adds(self, data):
        return self.success(post(self.URL + self.ADD, headers=self.token.headers_by_json, json={'list': data}))

    def removes(self, ids):
        return self.success(post(self.URL + self.REMOVE, headers=self.token.headers, params={'ids': ids}))

    def removes_by_date(self, start=date.today(), end=date.today()):
        return self.success(post(
            self.URL + self.REMOVE_DT,
            headers=self.token.headers,
            params={'start': start, 'end': end}
        ))

    def search(
            self,
            start=date.today(),
            end=date.today(),
            text='',
            page=0,
            size=10,
            sort=Sort.EN_DT,
            desc=True
    ):
        return self.response(post(self.URL + self.SEARCH, headers=self.token.headers, params={
            'start': start,
            'end': end,
            'text': text,
            'page': page,
            'size': size,
            'sort': sort,
            'desc': desc
        }))

    def sample(self):
        return self.response(post(self.URL + self.SAMPLE, headers=self.token.headers))

class Ticker(Net):
    ADD = '/pat/data/ticker/adds'
    REMOVE = '/pat/data/ticker/removes'
    CLEAR = '/pat/data/ticker/clear'
    SEARCH = '/pat/ticker/search'

    class Sort:
        PM = 'perma'
        TK = 'ticker'
        NM = 'name'
        RV = 'revision'
        CR = 'creation'

    def __init__(self, token):
        self.token: Token = token

    def adds(self, data):
        return self.success(post(self.URL + self.ADD, headers=self.token.headers_by_json, json={'list': data}))

    def removes(self, ids):
        return self.success(post(self.URL + self.REMOVE, headers=self.token.headers, params={'ids': ids}))

    def clear(self):
        return self.success(post(self.URL + self.CLEAR, headers=self.token.headers))

    def search(self, text='', page=0, size=10, sort=Sort.TK, desc=False):
        return self.response(post(self.URL + self.SEARCH, headers=self.token.headers, params={
            'text': text,
            'page': page,
            'size': size,
            'sort': sort,
            'desc': desc
        }))

class Token(Net):
    TEMP = '/user/remember/set'
    ACCESS = '/user/access'
    REISSUE = '/user/reissue'

    def __init__(self, email, pwd, on_update=None):
        self.email = email
        self.pwd = pwd
        self.access = None
        self.refresh = None
        self.on_update = on_update

    @property
    def headers(self):
        return self.header_dict('application/x-www-form-urlencoded')

    @property
    def headers_by_json(self):
        return self.header_dict('application/json')

    def header_dict(self, ct):
        headers = CaseInsensitiveDict()
        headers['Content-Type'] = ct
        headers["authorization"] = self.get_access
        return headers

    @property
    def get_access(self):
        if self.is_expires(self.access):
            if self.is_expires(self.refresh):
                self.update_by_issue()
            else:
                self.update_by_reissue()

        return self.get(self.access)

    @classmethod
    def is_expires(cls, data):
        return data is None or data['expires'] - timedelta(minutes=5) < datetime.now()

    @classmethod
    def get(cls, data):
        return '' if data is None else data['type'] + ' ' + data['token']

    @property
    def temp(self):
        return self.response(post(self.URL + self.TEMP))

    @property
    def issue(self):
        data = self.temp
        if data is None:
            return None

        headers = CaseInsensitiveDict()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers["authorization"] = data['grantType'] + ' ' + data['accessToken']

        return self.response(post(
            self.URL + self.ACCESS,
            headers=headers,
            params={'email': self.email, 'pwd': self.pwd}
        ))

    @property
    def reissue(self):
        headers = CaseInsensitiveDict()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers["authorization"] = self.get(self.refresh)

        return self.response(post(self.URL + self.REISSUE, headers=headers))

    def update_by_issue(self):
        data = self.issue
        if data is not None:
            self.set_access(data)
            self.set_refresh(data)

            if self.on_update is not None:
                self.on_update(self.access, self.refresh)

    def update_by_reissue(self):
        data = self.reissue
        if data is not None:
            self.set_access(data)

            if self.on_update is not None:
                self.on_update(self.access, self.refresh)

    def set_access(self, data):
        #print('set_access', data)
        self.access = {
            'token': data['accessToken'],
            'type': data['grantType'],
            'expires': (datetime.now() + timedelta(milliseconds=3600000))
        }

    def set_refresh(self, data):
        self.refresh = {
            'token': data['refreshToken'],
            'type': data['grantType'],
            'expires': (datetime.now() + timedelta(milliseconds=86400000))
        }