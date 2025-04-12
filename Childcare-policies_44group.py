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
elif type_choice == "임신 준비":
    policy_options = ["난임치료휴가"]
else:
    policy_options = []

policy_type = st.selectbox("이용할 육아제도를 선택하세요", policy_options)
notify = st.checkbox("알림 기능 수신을 원하시나요?")
public_servant = st.radio("공무원이신가요?", ["아니오", "예"]) == "예"

# 날짜 계산
today = datetime.today().date()
child_birth_date = input_date
if type_choice == "출산예정일":
    child_birth_date = input_date

child_age_months = (today.year - child_birth_date.year) * 12 + (today.month - child_birth_date.month)
if today.day < child_birth_date.day:
    child_age_months -= 1

# 육아휴직 관련 추가 질문 (필요 시만 출력)
joint_leave = False
if policy_type == "육아휴직 (6+6제도 포함)" and child_age_months <= 18:
    joint_leave = st.radio("배우자도 함께 육아휴직을 사용할 예정인가요?", ["예", "아니오"]) == "예"

# 결과 출력
st.markdown('<div class="sub-header">2. 육아제도 신청 가이드</div>', unsafe_allow_html=True)

if public_servant:
    st.warning("※ 공무원은 '고용보험 적용 대상'이 아니므로 일부 육아휴직 급여 제도(6+6 포함)는 적용되지 않을 수 있습니다.")

result = ""

if policy_type == "육아휴직 (6+6제도 포함)":
    deadline = child_birth_date + timedelta(days=365 * 8)
    result += f"- 육아휴직 신청 마감일: {deadline} (자녀 만 8세 이전)\n"
    result += f"- 현재 자녀 나이: 약 {child_age_months}개월\n\n"

    if child_age_months <= 18:
        if joint_leave:
            result += ("✅ 부모 함께 사용하는 '6+6 육아휴직제도' 적용 대상입니다.\n"
                       "- 부모 각자 첫 6개월 동안 통상임금의 100% 지급 (상한액 적용)\n"
                       "- 각 월별 상한액: 1~2개월 250만, 3개월 300만, 4개월 350만, 5개월 400만, 6개월 450만 원")
        else:
            result += "- 단독 육아휴직 사용 시: 1년 (상황에 따라 최대 1년 6개월까지 가능)"
    else:
        result += "⚠ 자녀가 생후 18개월 초과로 '6+6 제도'는 적용되지 않습니다."

elif policy_type == "출산전후휴가":
    start_date = input_date - timedelta(days=45)
    end_date = input_date + timedelta(days=45)
    result += f"- 출산전후휴가는 {start_date}부터 {end_date}까지 사용 가능 (공휴일 및 주말 포함)\n- 최초 60일 유급, 이후 30일 무급\n"

elif policy_type == "배우자출산휴가":
    end_date = business_days_only(input_date, 20)
    deadline = input_date + timedelta(days=120)
    result += f"- 배우자출산휴가는 {end_date}까지 20일 유급으로 사용 가능 (출산일 기준 120일 이내 사용, 공휴일 및 주말 제외)\n- 최대 3회 분할 가능\n"

elif policy_type == "육아기단축근로":
    deadline = input_date + timedelta(days=365 * 12)
    result += f"- 육아기단축근로 신청 가능: {deadline}까지 (자녀 만 12세 전까지)\n"

elif policy_type == "임신기단축근로":
    result += ("- 임신 12주 이내 또는 32주 이후의 근로자 대상\n"
               "- 1일 2시간 단축 근무, 고위험 임신 시 전 기간 유급\n")

elif policy_type == "난임치료휴가":
    result += "- 난임치료휴가: 연 6일 (최초 2일 유급), 남녀 근로자 모두 가능\n"

if result:
    result += ("\n\n**[신청 가이드]**\n"
               "- 고용노동부 정책자료 사이트 방문 또는 고용센터 문의\n"
               "- [고용노동부 정책 안내 바로가기](https://www.moel.go.kr/policy/policydata/list.do)")

st.success(result)

# 급여 계산기 조건부 표시
if policy_type in ["출산전후휴가", "배우자출산휴가", "육아휴직 (6+6제도 포함)"]:
    st.markdown('<div class="sub-header">3. 육아휴직 급여 예상 계산기', unsafe_allow_html=True)
    base_salary = st.number_input("통상임금 (월급)", min_value=0, step=10000, format="%d")

    if base_salary > 0:
        total_support = 0
        description = ""

        months_used = st.slider("사용 개월 수 (1~12개월)", 1, 12, 6)

        if policy_type == "출산전후휴가":
            daily_pay = base_salary / 30
            support = daily_pay * 60
            total_support = support
            description += f"출산전후휴가 예상 급여: 일급 {daily_pay:,.0f}원 x 60일 = {support:,.0f}원"

        elif policy_type == "배우자출산휴가":
            daily_pay = base_salary / 30
            support = daily_pay * 20
            total_support = support
            description += f"배우자출산휴가 예상 급여: 일급 {daily_pay:,.0f}원 x 20일 = {support:,.0f}원"

        elif policy_type == "육아휴직 (6+6제도 포함)":
            support = 0
            if child_age_months <= 18 and joint_leave:
                caps = [2500000, 2500000, 3000000, 3500000, 4000000, 4500000]
                for i in range(min(months_used, 6)):
                    support += min(base_salary, caps[i]) * 2  # 부모 각각 적용
                for i in range(6, months_used):
                    support += min(base_salary, 2000000) * 2
            else:
                for i in range(months_used):
                    support += min(base_salary, 2500000 if i < 3 else 2000000)

            total_support = support
            description += f"육아휴직 예상 급여 총합: {support:,.0f}원 (사용 개월 수 기준)"

        st.info(description)

        parent_pay = 0
        if child_age_months <= 11:
            parent_pay = 1000000
        elif child_age_months <= 23:
            parent_pay = 500000

        if parent_pay:
            months = min(months_used, 12 if child_age_months <= 11 else max(0, 24 - child_age_months))
            parent_total = parent_pay * months
            st.info(f"부모급여 예상 금액: 월 {parent_pay:,.0f}원 x {months}개월 = {parent_total:,.0f}원")
            st.info(f"총 예상 지원금: 육아휴직/휴가급여 {total_support:,.0f}원 + 부모급여 {parent_total:,.0f}원 = {total_support + parent_total:,.0f}원")

# 서류 링크 안내
st.markdown('<div class="sub-header">4. 육아휴직 신청 서류 안내</div>', unsafe_allow_html=True)
st.markdown("""
- [육아휴직급여 신청서 다운로드 (고용노동부)](https://www.moel.go.kr/policy/policydata/list.do)
- [육아휴직 온라인 신청 안내](https://www.ei.go.kr/)
""")

if notify:
    st.info("추후 이메일/캘린더 알림 기능과 연동 예정입니다.")

# 요약 안내
st.markdown("""
---
### 🍼 임신과 육아를 준비하고 계신가요?
**주요 지원제도 요약:**

- **국민행복카드**: 태아 1인당 100만 원, 출산 후 2년까지 사용 가능
- **고위험 임산부 의료비**: 최대 300만 원 지원
- **청소년 산모 지원**: 120만 원 (만 19세 이하 대상)
- **엽산제/철분제**: 보건소에서 무료 제공
- **첫만남이용권**: 첫째 200만 원, 둘째 이상 300만 원 (출생 1년 내 사용)
- **신청처**: 정부24 또는 주민센터 방문
""")
