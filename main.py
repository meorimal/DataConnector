#모듈
import pat

VERSION = "0.0.1"

# 가입한 이메일(ID) / 비밀번호 입력
# 관리자 권한 필요 (검색은 사용자 권한)
pta = pat.Access('test@test.com', '00000')

# 예제
def prompt(name):
    match name:
        case 'e':
            return False

        case 'pat a':
            pat_add()
        case 'pat r':
            pat_remove()
        case 'pat rd':
            pat_remove_by_date()
        case 'pat s':
            pat_search()
        case 'pat sp':
            pat_sample()

        case 'pat tk a':
            pat_ticker_add()
        case 'pat tk r':
            pat_ticker_remove()
        case 'pat tk c':
            pat_ticker_clear()
        case 'pat tk s':
            pat_ticker_search()

    return True

# 산호 추가
def pat_add():
    # [[permaticker, ticker, entry_date, entry_price, entry_tradeval, exit_date, exit_price, exit_tradeval, return]]
    # ticker는 필수값 아님(빈값 '' 으로 대체 가능)
    rst = pta.signal.adds([
        ['124263', 'IRTC', '8/1/25', '164.97', '310803480', '8/12/25', '162.35', '73382200', '-1.59%'],
        ['198871', 'TILE', '8/1/25', '24.61', '29261290', '8/12/25', '26.07', '10558350', '5.93%'],
        ['124668', 'FLGT', '8/5/25', '20.78', '21361840', '8/14/25', '21.74', '4239300', '4.62%']
    ])
    # 결과값 bool
    print(rst)

# 신호 삭제
def pat_remove():
    # [entry_date@permaticker]
    # 날짜(Y-m-d)와 종목번호를 '@'구분자로 결합후 리스트로 전달
    rst = pta.signal.removes(['2025-08-01@124263','2025-08-01@198871','2025-08-05@124668'])
    # 결과값 bool
    print(rst)

# 날짜기준 신호 삭제
def pat_remove_by_date():
    # 매입일(entry_date, Y-m-d) 기준 날짜 범뮈
    rst = pta.signal.removes_by_date('2025-08-01', '2025-08-05')
    # 결과값 bool
    print(rst)

# 신호 검색
def pat_search():
    # 파라미터 start=매입일(entry_date, Y-m-d, 시작일), end=매입일(entry_date, Y-m-d, 마지막일),
    # text=검색어, page=페이지번호, size=페이지당출력갯수, sort=정렬기준, desc=역순여부
    # 정렬기준(sort) PM=permaticker, TK=ticker, NM=이름, EN_DT=매입일, EN_PRC=매입가격, EN_TRD=매입거래액,
    # EX_DT=처분일, EX_PRC=처분가격, EX_TRD=처분거래액, RP=수익률, RV=변경시간, CR=생성시간
    rst = pta.signal.search('2025-08-01', '2025-08-31', 'IR', page=0, size=10, sort=pat.Signal.Sort.EN_DT, desc=True)
    # 결과값 json (API 문서 참고)
    print(rst)

# 체험용 신호 보기
def pat_sample():
    rst = pta.signal.sample()
    # 결과값 json (API 문서 참고)
    print(rst)

# 종목정보 추가
def pat_ticker_add():
    # [[permaticker, ticker, name]]
    rst = pta.ticker.adds([
        ['114929', 'ASL', 'ASHANTI GOLDFIELDS CO LTD'],
        ['115164', 'BROA', 'BROKAT TECHNOLOGIES AKTIENGESELLSCHAFT'],
        ['103863', 'DANOY', 'GROUPE DANONE']
    ])
    # 결과값 bool
    print(rst)

# 종목정보 삭제
def pat_ticker_remove():
    # [permaticker]
    rst = pta.ticker.removes(['114929','115164','103863'])
    # 결과값 bool
    print(rst)

# 종목정보 전체삭제
def pat_ticker_clear():
    rst = pta.ticker.clear()
    # 결과값 bool
    print(rst)

# 종목정보 검색
def pat_ticker_search():
    # 파라미터 text=검색어, page=페이지번호, size=페이지당출력갯수, sort=정렬기준, desc=역순여부
    # 정렬기준(sort) PM=permaticker, TK=ticker, NM=이름, RV=변경시간, CR=생성시간
    rst = pta.ticker.search('ASHANTI', page=0, size=10, sort=pat.Ticker.Sort.TK, desc=False)
    # 결과값 json (API 문서 참고)
    print(rst)

if __name__ == '__main__':
    print('Welcome! Data Connector! v' + VERSION)
    print('[e] 종료')
    print('[pat a] 산호 추가, [pat r] 산호 삭제, [pat rd] 날짜기준 신호 삭제, '
          '[pat s] 신호 검색, [pat sp] 체험용 신호 보기')
    print('[pat tk a] 종목정보 추가, [pat tk r] 종목정보 삭제, [pat tk c] 종목정보 전체삭제, '
          '[pat tk s] 종목정보 검색')

    while True:
        if not prompt(input('dc : ')):
            break

    print('Goodbye')

