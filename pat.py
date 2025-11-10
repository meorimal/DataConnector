from datetime import date, datetime, timedelta

from requests import post, get
from requests.structures import CaseInsensitiveDict

class Access:
    def __init__(self, email, pwd):
        token = Token(email, pwd)
        self.daily = Daily(token)
        self.score = Score(token)
        self.universe = Universe(token)
        self.factor = Factor(token)
        self.column = Column(token)

class Net:
    # URL = 'https://lefuture.kr/home/api'
    URL = 'http://localhost:8080/home/api' #개발용

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

class Daily(Net):
    ADD = '/pat/daily/adds'
    REMOVE = '/pat/daily/removes'
    REMOVE_DT = '/pat/daily/removes/date'
    CLEAR = '/pat/daily/clear'
    SEARCH = '/pat/daily/search'
    SAMPLE = '/pat/daily/sample'

    class Type:
        BUY = 'BUY'
        SELL = 'SELL'
        HOLD = 'HOLD'

    class Sort:
        PM = 'perma'
        TK = 'ticker'
        NM = 'name'
        DT = 'date'
        PRC = 'price'
        EN_DT = 'enterDate'
        EN_PRC = 'enterPrice'
        SCR = 'score'
        RT = 'returns'
        RV = 'revision'
        CR = 'creation'

    def __init__(self, token):
        self.token: Token = token

    def adds(self, data, tp=Type.BUY):
        return self.success(post(self.URL + self.ADD + '/' + tp, headers=self.token.headers_by_json, json={'list': data}))

    def removes(self, ids):
        return self.success(post(self.URL + self.REMOVE, headers=self.token.headers_by_json, json={'list': ids}))

    def removes_by_date(self, start=date.today(), end=date.today(), tp=Type.BUY):
        return self.success(post(
            self.URL + self.REMOVE_DT + '/' + tp,
            headers=self.token.headers,
            params={'start': start, 'end': end}
        ))

    def clear(self, tp=Type.BUY):
        return self.success(post(self.URL + self.CLEAR + '/' + tp, headers=self.token.headers))

    def search(
            self,
            start=date.today(),
            end=date.today(),
            text='',
            page=0,
            size=10,
            sort=Sort.EN_DT,
            desc=True,
            tp=Type.BUY
    ):

        return self.response(post(self.URL + self.SEARCH + '/' + tp, headers=self.token.headers, params={
            'start': start,
            'end': end,
            'text': text,
            'page': page,
            'size': size,
            'sort': sort,
            'desc': desc
        }))

    def sample(self, tp=Type.BUY):
        return self.response(post(self.URL + self.SAMPLE + '/' + tp, headers=self.token.headers))

class Score(Net):
    ADD = '/pat/score/adds'
    REMOVE = '/pat/score/removes'
    REMOVE_DT = '/pat/score/removes/date'
    SEARCH = '/pat/score/search'

    class Sort:
        PM = 'perma'
        TK = 'ticker'
        NM = 'name'
        DT = 'date'
        PRC = 'close'
        SCR = 'score'
        RV = 'revision'
        CR = 'creation'

    def __init__(self, token):
        self.token: Token = token

    def adds(self, data):
        return self.success(post(self.URL + self.ADD, headers=self.token.headers_by_json, json={'list': data}))

    def removes(self, ids):
        return self.success(post(self.URL + self.REMOVE, headers=self.token.headers_by_json, json={'list': ids}))

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
            sort=Sort.DT,
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

class Universe(Net):
    ADD = '/pat/score/universe/adds'
    KOR = '/pat/score/universe/edit/name/kor'
    REMOVE = '/pat/score/universe/removes'
    CLEAR = '/pat/score/universe/clear'
    SEARCH = '/pat/score/universe/search'

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

    def kor(self, data):
        return self.success(post(self.URL + self.KOR, headers=self.token.headers_by_json, json={'list': data}))

    def removes(self, ids):
        return self.success(post(self.URL + self.REMOVE, headers=self.token.headers, params={'ids': ids}))

    def clear(self):
        return self.success(post(self.URL + self.CLEAR, headers=self.token.headers))

    def search(self, exchange=None, category=None, sector=None, industry=None, location=None,
               text='', page=0, size=10, sort=Sort.TK, desc=False):
        return self.response(post(self.URL + self.SEARCH, headers=self.token.headers, params={
            'exchange': exchange,
            'category': category,
            'sector': sector,
            'industry': industry,
            'location': location,
            'text': text,
            'page': page,
            'size': size,
            'sort': sort,
            'desc': desc
        }))

class Factor(Net):
    ADD = '/pat/factor/adds'
    REMOVE_DT = '/pat/factor/removes/date'
    SEARCH = '/pat/factor/search'

    class Sort:
        DT = 'date'
        MM = 'mmt'
        SM = 'smb'
        BE = 'beta'
        VO = 'vol'

    def __init__(self, token):
        self.token: Token = token

    def adds(self, data):
        return self.success(post(self.URL + self.ADD, headers=self.token.headers_by_json, json={'list': data}))

    def removes_by_date(self, start=date.today(), end=date.today()):
        return self.success(post(
            self.URL + self.REMOVE_DT,
            headers=self.token.headers,
            params={'start': start, 'end': end}
        ))

    def search(self, start=None, end=None, days=None,
               text='', page=0, size=10, sort=Sort.DT, desc=False):
        return self.response(post(self.URL + self.SEARCH, headers=self.token.headers, params={
            'start': start,
            'end': end,
            'days': days,
            'text': text,
            'page': page,
            'size': size,
            'sort': sort,
            'desc': desc
        }))

class Column(Net):
    ADD = '/pat/column/add'
    REMOVE = '/pat/column/removes'

    class Sort:
        DT = 'date'
        TI = 'title'
        SE = 'section'

    def __init__(self, token):
        self.token: Token = token

    def add(self, title, msg, dt, link=None, section=None, op=None):
        return self.response(post(self.URL + self.ADD, headers=self.token.headers, params={
            'title': title,
            'msg': msg,
            'link': link,
            'section': section,
            'open': op,
            'date': dt
        }))

    def removes(self, ids):
        return self.success(post(self.URL + self.REMOVE, headers=self.token.headers, params={'ids': ids}))

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

        return self.response(get(self.URL + self.REISSUE, headers=headers))

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
        print('set_access', data)
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