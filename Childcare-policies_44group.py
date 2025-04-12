import streamlit as st
from datetime import datetime, timedelta

# 공휴일 및 주말 제외 계산 함수
def business_days_only(start_date, days):
    count = 0
    current = start_date
    while count < days:
        current += timedelta(days=1)
        if current.weekday() < 5 and not is_holiday(current):
            count += 1
    return current

# 공휴일 목록 설정
def is_holiday(date):
    holidays = [
        datetime(2025, 1, 1).date(),
        datetime(2025, 3, 1).date(),
        datetime(2025, 5, 5).date(),
        datetime(2025, 6, 6).date(),
        datetime(2025, 8, 15).date(),
        datetime(2025, 10, 3).date(),
        datetime(2025, 12, 25).date(),
    ]
    return date in holidays

# Streamlit 앱 설정
st.set_page_config(page_title="육아제도 신청 가이드", layout="centered")

# 제안서 스타일로 커스탬했습니다
custom_style = """
<link href="https://fonts.googleapis.com/css2?family=42dot+Sans&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Do+Hyeon&family=Gasoek+One&display=swap" rel="stylesheet">

<style>
    body {
        background-color: #f9f9f9;
        font-family: '42dot Sans', sans-serif;
        color: #000000;
    }
    .main-header {
        color: #3D83EB;
        font-family: 'Do Hyeon', sans-serif;
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
    }
    .sub-header {
        color: #3D83EB;
        font-size: 24px;
        font-weight: bold;
        margin-top: 40px;
        margin-bottom: 10px;
    }
    .success-box {
        background-color: #3D83EB;
        border-left: 6px solid #3D83EB;
        padding: 10px;
        margin-top: 0px;
        font-weight: bold;
        color: #FFFFFF;
        margin-bottom: 10px;
    }
</style>
"""
st.markdown(custom_style, unsafe_allow_html=True)

# 메인 헤더
st.markdown('<div class="main-header">육아제도 신청 가이드</div>', unsafe_allow_html=True)

# 기본 정보 입력
st.markdown('<div class="sub-header">1. 기본 정보 입력</div>', unsafe_allow_html=True)
type_choice = st.radio("유형 선택", ["출산예정일", "자녀 생년월일", "임신 준비"])
input_date = st.date_input("날짜를 입력하세요")

# 제도 선택 조건 분기
if type_choice == "출산예정일":
    policy_options = ["임신기단축근로", "출산전후휴가", "배우자출산휴가"]
elif type_choice == "자녀 생년월일":
    policy_options = ["육아기단축근로", "육아휴직 (6+6제도 포함)"]
else:  # 임신 준비
    policy_options = ["난임치료휴가"]

policy_type = st.selectbox("이용할 육아제도를 선택하세요", policy_options)

# 날짜 계산 및 결과 출력
today = datetime.today().date()
result = ""
st.badge("information")

if policy_type == "출산전후휴가":
    start_date = input_date - timedelta(days=45)
    end_date = input_date + timedelta(days=45)
    result += f"✅ 출산전후휴가는 {start_date}부터 {end_date}까지 사용 가능 (공휴일 및 주말 포함)\n"
elif policy_type == "배우자출산휴가":
    end_date = business_days_only(input_date, 20)
    deadline = input_date + timedelta(days=120)
    result += f"✅ 배우자출산휴가는 {end_date}까지 사용 가능 (출산일 기준 120일 이내)\n"
elif policy_type == "육아기단축근로":
    deadline = input_date + timedelta(days=365 * 12)
    result += f"✅ 육아기단축근로 신청 가능: {deadline}까지 (자녀 만 12세 전까지)\n"
elif policy_type == "임신기단축근로":
    result += "✅ 임신기 단축 근무는 임신 초기 또는 말기에 적용됩니다.\n"
elif policy_type == "난임치료휴가":
    result += "✅ 난임치료휴가는 연간 최대 6일 사용 가능합니다.\n"

if result:
    st.markdown(f'<div class="success-box">{result}</div>', unsafe_allow_html=True)

# 급여 계산기
if policy_type in ["출산전후휴가", "배우자출산휴가"]:
    st.markdown('<div class="sub-header">2. 급여 계산기</div>', unsafe_allow_html=True)
    base_salary = st.number_input("통상임금 (월급)", min_value=0, step=10000)
    
    if base_salary > 0:
        if policy_type == "출산전후휴가":
            daily_pay = base_salary / 30
            total_support = daily_pay * 60
            st.info(f"예상 급여: {total_support:,.0f}원 (60일 기준)")
        elif policy_type == "배우자출산휴가":
            daily_pay = base_salary / 30
            total_support = daily_pay * 20
            st.info(f"예상 급여: {total_support:,.0f}원 (20일 기준)")

# 서류 링크 안내
st.markdown('<div class="sub-header">3. 관련 서류 안내</div>', unsafe_allow_html=True)
st.markdown("""
- [육아휴직급여 신청서 다운로드](https://www.moel.go.kr/policy/policydata/list.do)
- [육아휴직 온라인 신청 안내](https://www.ei.go.kr/)
""")