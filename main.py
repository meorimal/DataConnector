#모듈
import pat

VERSION = "0.0.7"

# 가입한 이메일(ID) / 비밀번호 입력
# 유료이용자/관리자 권한 필요 (검색은 사용자 권한)
pta = pat.Access('test@test.com', '00000')

# 모든 함수에는 nation 파라미터가 있습니다. 국내주식은 KR, 미국주식은 US 를 입력합니다

# 예제
def prompt(name):
    match name:
        case 'e':
            return False

        case 'pat a b':
            pat_add_buy()
        case 'pat a s':
            pat_add_sell()
        case 'pat a h':
            pat_add_hold()

        case 'pat r b':
            pat_remove(pat.Daily.Type.BUY)
        case 'pat r s':
            pat_remove(pat.Daily.Type.SELL)
        case 'pat r h':
            pat_remove(pat.Daily.Type.HOLD)

        case 'pat rd b':
            pat_remove_by_date(pat.Daily.Type.BUY)
        case 'pat rd s':
            pat_remove_by_date(pat.Daily.Type.SELL)
        case 'pat rd h':
            pat_remove_by_date(pat.Daily.Type.HOLD)

        case 'pat c b':
            pat_clear(pat.Daily.Type.BUY)
        case 'pat c s':
            pat_clear(pat.Daily.Type.SELL)
        case 'pat c h':
            pat_clear(pat.Daily.Type.HOLD)

        case 'pat s b':
            pat_search(pat.Daily.Type.BUY)
        case 'pat s s':
            pat_search(pat.Daily.Type.SELL)
        case 'pat s h':
            pat_search(pat.Daily.Type.HOLD)

        case 'pat scr a':
            pat_score_add()
        case 'pat scr r':
            pat_score_remove()
        case 'pat scr rd':
            pat_score_remove_by_date()
        case 'pat scr s':
            pat_score_search()

        case 'pat uni a':
            pat_universe_add()
        case 'pat uni k':
            pat_universe_kor()
        case 'pat uni r':
            pat_universe_remove()
        case 'pat uni c':
            pat_universe_clear()
        case 'pat uni s':
            pat_universe_search()

        case 'pat fac a':
            pat_factor_add()
        case 'pat fac rd':
            pat_factor_remove_by_date()
        case 'pat fac s':
            pat_factor_search()

        # case 'pat col a':
        #     pat_column_add()
        # case 'pat col r':
        #     pat_column_remove()

    return True

# 매입 신호 추가
def pat_add_buy():
    # [[date, ticker, price, score]]
    rst = pta.daily.adds([
        ["2025-09-18", "ABAT", "2.9563", "1.0"],
        ["2025-09-18", "QSI", "1.525", "1.0"],
        ["2025-09-22", "MTSR", "53.75", "1.0"]
    ], nation=pat.Nation.KR)    # 국내: KR, 미국: US
    # 결과값 bool
    print(rst)

# 처분 신호 추가
def pat_add_sell():
    # [[date, ticker, price, return]]
    rst = pta.daily.adds([
        ["2025-09-19", "ABAT", "3.3", "0.116260190102493"],
        ["2025-09-22", "QSI", "1.7", "0.114754098360656"],
        ["2025-09-23", "MTSR", "53.0", "-0.013953488372093"]
    ], tp=pat.Daily.Type.SELL)
    # 결과값 bool
    print(rst)

# 보유 신호 추가
def pat_add_hold():
    # [[date, ticker, price, entry_date, entry_price, score, return]]
    rst = pta.daily.adds([
        ["2025-09-19", "ATYR", "0.9921", "2025-09-12", " 6.435", " 1.0", "-0.845827505827506"],
        ["2025-09-19", "QSI", "1.5", "2025-09-18", "1.525", "1.0", "-0.0163934426229507"],
        ["2025-09-22", "MTSR", "53.58", "2025-09-22", "53.75", "1.0", "-0.00316279069767444"]
    ], tp=pat.Daily.Type.HOLD)
    # 결과값 bool
    print(rst)

# 신호 삭제
def pat_remove(tp):
    # [[date, type, ticker]]
    rst = pta.daily.removes([
        ["2025-09-19", tp, "ATYR"],
        ["2025-09-19", tp, "QSI"],
        ["2025-09-22", tp, "MTSR"]
    ])
    # 결과값 bool
    print(rst)

# 날짜기준 신호 삭제
def pat_remove_by_date(tp):
    # 파라미터 start=시작일, end=마지막일, tp=(BUY: 매입, SELL: 처분, HOLD: 보유)
    rst = pta.daily.removes_by_date('2025-08-01', '2025-08-05', tp)
    # 결과값 bool
    print(rst)

# 신호 전체삭제
def pat_clear(tp):
    rst = pta.daily.clear(tp)
    # 결과값 bool
    print(rst)

# 신호 검색
def pat_search(tp):
    # 파라미터 start=시작일, end=마지막일,
    # text=검색어, page=페이지번호, size=페이지당출력갯수, sort=정렬기준, desc=역순여부
    # tp=(BUY: 매입, SELL: 처분, HOLD: 보유)
    # 정렬기준(sort) PM=permaticker, TK=ticker, NM=이름, DT=날짜, PRC=가격,
    # EN_DT=매입일, EN_PRC=매입가격, SCR=점수, RT=수익률, RV=변경시간, CR=생성시간
    rst = pta.daily.search(
        start='2025-10-01',
        end='2025-10-30',
        page=0,
        size=10,
        sort=pat.Daily.Sort.DT,
        desc=True,
        tp=tp
    )
    # 결과값 json (API 문서 참고)
    print(rst)

# 종목 점수 추가
def pat_score_add():
    # [[[date, ticker, score, mmt, smb, beta, vol, group, close, lower, upper]]]
    rst = pta.score.adds([
        ["2025-08-28", "110688", "1.0", "1.0", "1.0", "1.0", "1.0", "top", "1.72", "100", "200"],
        ["2025-08-28", "121744", "1.0", "1.0", "1.0", "1.0", "1.0", "top", "5.56", "100", "200"],
        ["2025-08-28", "124440", "1.0", "1.0", "1.0", "1.0", "1.0", "top", "01.22", "100", "200"]
    ])
    # 결과값 bool
    print(rst)

# 종목 점수 삭제
def pat_score_remove():
    # [[date, ticker]]
    rst = pta.score.removes([
        ["2025-08-28", "110688"],
        ["2025-08-28", "121744"],
        ["2025-08-28", "124440"]
    ])
    # 결과값 bool
    print(rst)

# 날짜기준 종목 점수 삭제
def pat_score_remove_by_date():
    # 파라미터 start=시작일, end=마지막일
    rst = pta.score.removes_by_date('2025-08-01', '2025-08-05')
    # 결과값 bool
    print(rst)

# 종목 점수 검색
def pat_score_search():
    # 파라미터 start=시작일, end=마지막일,
    # text=검색어, page=페이지번호, size=페이지당출력갯수, sort=정렬기준, desc=역순여부
    # 정렬기준(sort) PM=permaticker, TK=ticker, NM=이름, DT=날짜, PRC=가격,
    # SCR=점수, RV=변경시간, CR=생성시간
    rst = pta.score.search(
        start='2025-08-01',
        end='2025-08-31',
        text='IR',
        page=0,
        size=10,
        sort=pat.Score.Sort.DT,
        desc=True
    )
    # 결과값 json (API 문서 참고)
    print(rst)

# 종목정보 추가
def pat_universe_add():
    # [ticker, name, exchange, sector, nameKor]
    rst = pta.universe.adds([
        ["ASL", "ASHANTI GOLDFIELDS CO LTD", "NYSE", "Basic Materials", ""],
        ["BROA", "BROKAT TECHNOLOGIES AKTIENGESELLSCHAFT", "NASDAQ", "Technology", ""],
        ["DANOY", "GROUPE DANONE", "NYSE", "Consumer Defensive", ""]
    ])
    # 결과값 bool
    print(rst)

# 종목정보 한글명추가
def pat_universe_kor():
    # [ticker, name]
    rst = pta.universe.adds([
        ["AACB", "아티어스II애퀴지션"],
        ["TNDM", "탠덤다이어비츠케어"],
        ["EVR", "에버코어"]
    ])
    # 결과값 bool
    print(rst)

# 종목정보 삭제
def pat_universe_remove():
    # [ticker]
    rst = pta.universe.removes(['ASL','BROA','DANOY'])
    # 결과값 bool
    print(rst)

# 종목정보 전체삭제
def pat_universe_clear():
    rst = pta.universe.clear()
    # 결과값 bool
    print(rst)

# 종목정보 검색
def pat_universe_search():
    # 파라미터 text=검색어, page=페이지번호, size=페이지당출력갯수, sort=정렬기준, desc=역순여부
    # 정렬기준(sort) PM=permaticker, TK=ticker, NM=이름, RV=변경시간, CR=생성시간
    rst = pta.universe.search(text='ASHANTI', page=0, size=10, sort=pat.Universe.Sort.TK, desc=False)
    # 결과값 json (API 문서 참고)
    print(rst)

# 팩터 추가
def pat_factor_add():
    # [date, mmt, smb, beta, vol]
    rst = pta.factor.adds([
        ["2025-09-25", "0.34", "-0.39", "-0.31", "0.58"],
        ["2025-09-26", "-0.20", "0.13", "0.26", "-0.28"],
        ["2025-09-29", "-0.06", "-0.22", "0.24", "-0.56"]
    ])
    # 결과값 bool
    print(rst)

# 팩터 삭제
def pat_factor_remove_by_date():
    # 파라미터 start=시작일, end=마지막일
    rst = pta.factor.removes_by_date('2025-08-01', '2025-08-05')
    # 결과값 bool
    print(rst)

# 팩터 검색
def pat_factor_search():
    # 파라미터 start=시작일, end=마지막일,
    # text=검색어, page=페이지번호, size=페이지당출력갯수, sort=정렬기준, desc=역순여부
    # 정렬기준(sort) DT=날짜, MM=모멘텀, SM=SMB, BE=베타, VO=Low Volatility,
    # SCR=점수, RV=변경시간, CR=생성시간
    rst = pta.factor.search(
        start='2025-08-01',
        end='2025-08-31',
        page=0,
        size=10,
        sort=pat.Factor.Sort.DT,
        desc=True
    )
    # 결과값 json (API 문서 참고)
    print(rst)

# # 칼럼 추가
# def pat_column_add():
#     # title=제목, msg=내용, link=외부링크, section=주제구분, open=게시여부, date=날짜
#     rst = pta.column.add(
#         title="test title",
#         msg="text msg",
#         dt="2025-11-01"
#     )
#     # 결과값 json (API 문서 참고)
#     print(rst)
#
# # 칼럼 삭제
# def pat_column_remove():
#     # [id]
#     rst = pta.column.removes(['id1','id2','id3'])
#     # 결과값 bool
#     print(rst)

if __name__ == '__main__':
    print('Welcome! Data Connector! v' + VERSION)
    print('[e] 종료')

    print('[pat a b] 매입 신호 추가, [pat a s] 처분 신호 추가, [pat a h] 보유 신호 추가')
    print('[pat r b] 매입 신호 삭제, [pat r s] 처분 신호 삭제, [pat r h] 보유 신호 삭제, ')
    print('[pat rd b] 매입 신호 날짜기준 삭제, [pat rd s] 처분 신호 날짜기준 삭제, [pat rd h] 보유 신호 날짜기준 삭제')
    print('[pat c b] 매입 신호 전체삭제, [pat c s] 처분 신호 전체삭제, [pat c h] 보유 신호 전체삭제')
    print('[pat s b] 매입 신호 검색, [pat s s] 처분 신호 검색, [pat s h] 보유 신호 검색')
    print('[pat scr a] 종목점수 추가, [pat scr r] 종목점수 삭제, [pat scr rd] 종목점수 날짜기준 삭제, [pat scr s] 종목점수 검색')
    print('[pat uni a] 종목정보 추가, [pat uni k] 종목정보 한글명추가, [pat uni r] 종목정보 삭제, [pat uni c] 종목정보 전체삭제, [pat uni s] 종목정보 검색')
    print('[pat fac a] 팩터 추가, [pat fac rd] 팩터 날짜기준 삭제, [pat fac s] 팩터 검색')
    print('[pat col a] 칼럼 추가, [pat col r] 칼럼 삭제')

    while True:
        if not prompt(input('dc : ')):
            break

    print('Goodbye')

