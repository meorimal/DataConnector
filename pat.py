from datetime import date, datetime, timedelta
from requests import post, get
from requests.structures import CaseInsensitiveDict

import pandas as pd
import websocket
import json
import math

class Access:
    def __init__(self, email, pwd):
        token = Token(email, pwd)
        self.daily = Daily(token)
        self.score = Score(token)
        self.universe = Universe(token)
        self.factor = Factor(token)
        #self.column = Column(token)
        self.market = Market(token)

class Net:
    # URL = 'https://lefuture.kr/home/api'
    URL = 'http://localhost:8080/home/api' #개발용

    # WS_URL = 'wss://lefuture.kr/home/api/socket'
    WS_URL = 'ws://localhost:8080/home/api/socket'  # 개발용

    FOLDER = '/pat'

    def path(self, nation):
        return self.URL + self.FOLDER + '/' + nation

    def success(self, response) -> bool:
        rst = self.response(response)
        try:
            return False if rst is None else rst['success']
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

    def post_by_slicing(self, df: pd.DataFrame, path, headers, size):
        length = len(df)
        for i in range(math.ceil(length / size)):
            start = i * size
            end = min(start + size, length)
            data = df.iloc[start:end].values.tolist()
            if not self.success(post(path, headers=headers, json={'list': data})):
                return False

        return True

    def connect(self, path, headers):
        # websocket.enableTrace(True)
        return websocket.create_connection(self.WS_URL + self.FOLDER + path, header=dict(headers))

class Nation:
    KR = 'KR'
    US = 'US'

class Daily(Net):
    ADD = '/daily/adds'
    REMOVE = '/daily/removes'
    REMOVE_DT = '/daily/removes/date'
    CLEAR = '/daily/clear'
    SEARCH = '/daily/search'

    class Type:
        BUY = 'BUY'
        SELL = 'SELL'
        HOLD = 'HOLD'
        END = 'END'

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

    def adds(self, data, tp=Type.BUY, nation=Nation.KR):
        return self.success(post(self.path(nation) + self.ADD + '/' + tp, headers=self.token.headers_by_json, json={'list': data}))

    def adds_by_slicing(self, df, tp=Type.BUY, nation=Nation.KR, size=1000):
        return self.post_by_slicing(
            df.astype({'date': str}),
            self.path(nation) + self.ADD + '/' + tp,
            headers=self.token.headers_by_json,
            size=size
        )

    def removes(self, ids, nation=Nation.KR):
        return self.success(post(self.path(nation) + self.REMOVE, headers=self.token.headers_by_json, json={'list': ids}))

    def removes_by_date(self, start=date.today(), end=date.today(), tp=Type.BUY, nation=Nation.KR):
        return self.success(post(
            self.path(nation) + self.REMOVE_DT + '/' + tp,
            headers=self.token.headers,
            params={'start': start, 'end': end}
        ))

    def clear(self, tp=Type.BUY, nation=Nation.KR):
        return self.success(post(self.path(nation) + self.CLEAR + '/' + tp, headers=self.token.headers))

    def search(
            self,
            start=date.today(),
            end=date.today(),
            text='',
            page=0,
            size=10,
            sort=Sort.EN_DT,
            desc=True,
            tp=Type.BUY,
            nation=Nation.KR
    ):

        return self.response(post(self.path(nation) + self.SEARCH + '/' + tp, headers=self.token.headers, params={
            'start': start,
            'end': end,
            'text': text,
            'page': page,
            'size': size,
            'sort': sort,
            'desc': desc
        }))

class Score(Net):
    ADD = '/score/adds'
    REMOVE = '/score/removes'
    REMOVE_DT = '/score/removes/date'
    SEARCH = '/score/search'

    class Sort:
        TK = 'ticker'
        NM = 'name'
        DT = 'date'
        PRC = 'close'
        SCR = 'score'
        RV = 'revision'
        CR = 'creation'

    def __init__(self, token):
        self.token: Token = token

    def adds(self, data, nation=Nation.KR):
        return self.success(post(self.path(nation) + self.ADD, headers=self.token.headers_by_json, json={'list': data}))

    def adds_by_slicing(self, df, nation=Nation.KR, size=1000):
        return self.post_by_slicing(
            df.astype({'date': str}),
            self.path(nation) + self.ADD,
            headers=self.token.headers_by_json,
            size=size
        )

    def removes(self, ids, nation=Nation.KR):
        return self.success(post(self.path(nation) + self.REMOVE, headers=self.token.headers_by_json, json={'list': ids}))

    def removes_by_date(self, start=date.today(), end=date.today(), nation=Nation.KR):
        return self.success(post(
            self.path(nation) + self.REMOVE_DT,
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
            desc=True,
            nation=Nation.KR
    ):

        return self.response(post(self.path(nation) + self.SEARCH, headers=self.token.headers, params={
            'start': start,
            'end': end,
            'text': text,
            'page': page,
            'size': size,
            'sort': sort,
            'desc': desc
        }))

class Universe(Net):
    ADD = '/score/universe/adds'
    KOR = '/score/universe/edit/name/kor'
    REMOVE = '/score/universe/removes'
    CLEAR = '/score/universe/clear'
    SEARCH = '/score/universe/search'

    class Sort:
        TK = 'ticker'
        NM = 'name'
        RV = 'revision'
        CR = 'creation'

    def __init__(self, token, nation=Nation.KR):
        self.token: Token = token

    def adds(self, data, nation=Nation.KR):
        return self.success(post(self.path(nation) + self.ADD, headers=self.token.headers_by_json, json={'list': data}))

    def adds_by_slicing(self, df, nation=Nation.KR, size=1000):
        return self.post_by_slicing(
            df,
            self.path(nation) + self.ADD,
            headers=self.token.headers_by_json,
            size=size
        )

    def kor(self, data, nation=Nation.KR):
        return self.success(post(self.path(nation) + self.KOR, headers=self.token.headers_by_json, json={'list': data}))

    def kor_by_slicing(self, df, nation=Nation.KR, size=1000):
        return self.post_by_slicing(
            df,
            self.path(nation) + self.KOR,
            headers=self.token.headers_by_json,
            size=size
        )

    def removes(self, ids, nation=Nation.KR):
        return self.success(post(self.path(nation) + self.REMOVE, headers=self.token.headers, params={'ids': ids}))

    def clear(self, nation=Nation.KR):
        return self.success(post(self.path(nation) + self.CLEAR, headers=self.token.headers))

    def search(self, exchange=None, sector=None, text='', page=0, size=10, sort=Sort.TK, desc=False, nation=Nation.KR):
        return self.response(post(self.path(nation) + self.SEARCH, headers=self.token.headers, params={
            'exchange': exchange,
            'sector': sector,
            'text': text,
            'page': page,
            'size': size,
            'sort': sort,
            'desc': desc
        }))

class Factor(Net):
    ADD = '/factor/adds'
    REMOVE_DT = '/factor/removes/date'
    SEARCH = '/factor/search'

    class Sort:
        DT = 'date'
        MM = 'mmt'
        SM = 'smb'
        BE = 'beta'
        VO = 'vol'

    def __init__(self, token):
        self.token: Token = token

    def adds(self, data, nation=Nation.KR):
        return self.success(post(self.path(nation) + self.ADD, headers=self.token.headers_by_json, json={'list': data}))

    def adds_by_slicing(self, df, nation=Nation.KR, size=1000):
        return self.post_by_slicing(
            df.astype({'date': str}),
            self.path(nation) + self.ADD,
            headers=self.token.headers_by_json,
            size=size
        )

    def removes_by_date(self, start=date.today(), end=date.today(), nation=Nation.KR):
        return self.success(post(
            self.path(nation) + self.REMOVE_DT,
            headers=self.token.headers,
            params={'start': start, 'end': end}
        ))

    def search(self, start=None, end=None, days=None,
               text='', page=0, size=10, sort=Sort.DT, desc=False, nation=Nation.KR):
        return self.response(post(self.path(nation) + self.SEARCH, headers=self.token.headers, params={
            'start': start,
            'end': end,
            'days': days,
            'text': text,
            'page': page,
            'size': size,
            'sort': sort,
            'desc': desc
        }))

# class Column(Net):
#     ADD = '/pat/column/add'
#     REMOVE = '/pat/column/removes'
#
#     class Sort:
#         DT = 'date'
#         TI = 'title'
#         SE = 'section'
#
#     def __init__(self, token):
#         self.token: Token = token
#
#     def add(self, title, msg, dt, link=None, section=None, op=None):
#         return self.response(post(self.URL + self.ADD, headers=self.token.headers, params={
#             'title': title,
#             'msg': msg,
#             'link': link,
#             'section': section,
#             'open': op,
#             'date': dt
#         }))
#
#     def removes(self, ids):
#         return self.success(post(self.URL + self.REMOVE, headers=self.token.headers, params={'ids': ids}))

class Market(Net):
    def __init__(self, token):
        self.token: Token = token
        self.ws = None

    def send_from_df(self, df, nation=Nation.KR):
        return self.send(df.values.tolist(), nation)

    def send(self, data, nation=Nation.KR):
        if self.ws is None:
            self.ws = self.connect('/market', self.token.headers)
            self.ws.send(json.dumps({'auth': self.token.get_access, 'type': 'market_in'}))

        return self.ws.send(json.dumps({'list': data, 'nation': nation}))

    def close(self):
        self.ws.close()
        self.ws = None

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