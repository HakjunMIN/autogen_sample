import sqlite3
from faker import Faker
import random

fake = Faker("ko_KR")

conn = sqlite3.connect('kb-creditcard.db')
cursor = conn.cursor()

create_table_statements = [
    """
    CREATE TABLE IF NOT EXISTS card (
        card_id INTEGER PRIMARY KEY AUTOINCREMENT,
        card_name TEXT,
        card_brand TEXT,
        is_trans_payable BOOLEAN,
        is_cash_card BOOLEAN,
        linked_bank_code TEXT,
        account_num TEXT,
        annual_fee REAL,
        issue_date TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS customer (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        sex TEXT,
        annual_salary REAL, 
        city TEXT,
        address TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS issued_card (
        card_no TEXT PRIMARY KEY,
        card_id INTEGER,
        valid_data TEXT,
        is_annual_fee BOOLEAN,
        is_valid BOOLEAN,
        FOREIGN KEY(card_id) REFERENCES card(card_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS customer_own_card (
        customer_own_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        card_no TEXT,
        own_date TEXT,
        FOREIGN KEY(customer_id) REFERENCES customer(customer_id),
        FOREIGN KEY(card_no) REFERENCES issued_card(card_no)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS point (
        customer_id INTEGER,
        point_id INTEGER PRIMARY KEY AUTOINCREMENT,
        point_cnt INTEGER,
        point_list TEXT,
        point_name TEXT,
        remain_point_amt REAL,
        expiring_point_amt REAL,
        FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS bill (
        bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        card_no TEXT,
        bill_cnt INTEGER,
        bill_list TEXT,
        seqno INTEGER,
        charge_amt REAL,
        charge_day INTEGER,
        charge_month INTEGER,
        paid_out_date DATETIME,
        FOREIGN KEY(customer_id) REFERENCES customer(customer_id),
        FOREIGN KEY(card_no) REFERENCES issued_card(card_no)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS bill_add (
        bill_id INTEGER,
        bill_add_id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_detail_cnt INTEGER,
        bill_detail_list TEXT,
        card_no TEXT,
        paid_dtime DATETIME,
        trans_no TEXT,
        paid_amt REAL,
        currency_code TEXT,
        merchant_name TEXT,
        merchant_regno TEXT,
        credit_fee_amt REAL,
        total_install_cnt INTEGER,
        cur_install_cnt INTEGER,
        balance_amt REAL,
        prod_type TEXT,
        FOREIGN KEY(bill_id) REFERENCES bill(bill_id),
        FOREIGN KEY(card_no) REFERENCES issued_card(card_no)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS payment (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_id INTEGER,
        is_revolving BOOLEAN,
        pay_cnt INTEGER,
        pay_list TEXT,
        seqno INTEGER,
        pay_due_date DATETIME,
        pay_amt REAL,
        lump_sum_amt REAL,
        monthly_amt REAL,
        loan_short_amt REAL,
        revolving_amt REAL,
        loan_long_amt REAL,
        etc_amt REAL,
        FOREIGN KEY(bill_id) REFERENCES bill(bill_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS domestic_approve (
        customer_id INTEGER,
        card_no TEXT,
        approved_cnt INTEGER,
        approved_list TEXT,
        approved_num INTEGER PRIMARY KEY AUTOINCREMENT,
        approved_dtime DATETIME,
        status TEXT,
        pay_type TEXT,
        trans_dtime DATETIME,
        merchant_name TEXT,
        merchant_regno TEXT,
        approved_amt REAL,
        modified_amt REAL,
        total_install_cnt INTEGER,
        FOREIGN KEY(customer_id) REFERENCES customer(customer_id),
        FOREIGN KEY(card_no) REFERENCES issued_card(card_no)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS oversea_approve (
        customer_id INTEGER,
        card_no TEXT,
        approved_cnt INTEGER,
        approved_list TEXT,
        approved_num INTEGER PRIMARY KEY AUTOINCREMENT,
        approved_dtime TEXT,
        status TEXT,
        pay_type TEXT,
        trans_dtime DATETIME,
        merchant_name TEXT,
        approved_amt REAL,
        modified_amt REAL,
        country_code TEXT,
        currency_code TEXT,
        krw_amt REAL,
        FOREIGN KEY(customer_id) REFERENCES customer(customer_id),
        FOREIGN KEY(card_no) REFERENCES issued_card(card_no)
    )
    """
]

# Execute create table statements
for statement in create_table_statements:
    cursor.execute(statement)


business_types = [
    "음식점", "카페", "슈퍼마켓", "백화점", "의류점", "전자제품점", "서점", "약국", "병원", "미용실",
    "주유소", "호텔", "여행사", "영화관", "헬스장", "편의점", "꽃집", "자동차 정비소", "가구점", "스포츠 용품점"
]

goods = [
    "사과", "바나나", "오렌지", "포도", "딸기", "수박", "참외", "배", "복숭아", "자두",
    "감", "귤", "레몬", "라임", "체리", "망고", "파인애플", "키위", "블루베리", "라즈베리",
    "양파", "마늘", "감자", "고구마", "당근", "호박", "오이", "토마토", "브로콜리", "시금치",
    "상추", "배추", "무", "파", "고추", "피망", "가지", "버섯", "옥수수", "완두콩",
    "쌀", "밀가루", "보리", "옥수수", "귀리", "퀴노아", "아마씨", "치아씨드", "호두", "아몬드",
    "땅콩", "캐슈넛", "피스타치오", "헤이즐넛", "마카다미아", "브라질넛", "잣", "해바라기씨", "호박씨", "참깨",
    "우유", "치즈", "요거트", "버터", "크림", "아이스크림", "두유", "아몬드밀크", "코코넛밀크", "연유",
    "빵", "케이크", "쿠키", "머핀", "도넛", "크루아상", "파이", "타르트", "샌드위치", "햄버거",
    "피자", "파스타", "스파게티", "라자냐", "리조또", "수프", "스튜", "카레", "볶음밥", "김밥",
    "떡볶이", "순대", "튀김", "전", "만두", "찜", "구이", "조림", "볶음", "탕",
    "국", "찌개", "전골", "샐러드", "나물", "무침", "장아찌", "젓갈", "김치", "된장",
    "고추장", "간장", "소금", "설탕", "식초", "참기름", "들기름", "올리브유", "해바라기유", "코코넛오일",
    "돼지고기", "소고기", "닭고기", "양고기", "오리고기", "칠면조", "베이컨", "햄", "소시지", "스테이크",
    "생선", "새우", "게", "오징어", "문어", "조개", "굴", "홍합", "전복", "해삼",
    "라면", "우동", "소면", "칼국수", "냉면", "쫄면", "짜장면", "짬뽕", "비빔면", "국수",
    "커피", "차", "주스", "탄산음료", "스무디", "쉐이크", "와인", "맥주", "소주", "막걸리",
    "위스키", "브랜디", "보드카", "럼", "진", "데킬라", "샴페인", "칵테일", "리큐어", "사케",
    "샴푸", "린스", "바디워시", "비누", "치약", "칫솔", "면도기", "면도크림", "로션", "크림",
    "선크림", "화장품", "향수", "헤어젤", "헤어스프레이", "데오도란트", "핸드크림", "립밤", "마스크팩", "클렌징폼",
    "세제", "섬유유연제", "표백제", "청소용품", "쓰레기봉투", "비닐봉지", "종이컵", "종이접시", "일회용젓가락", "일회용숟가락"
]


def generate_fake_card_data():
    return {
        'card_name': random.choice([
            'KB 국민카드',
            'KB 국민 비즈니스카드',
            'KB 국민 청춘대로카드',
            'KB 국민 탄탄대로카드',
            'KB 국민 굿데이카드',
            'KB 국민 이지카드',
            'KB 국민 와이즈카드',
            'KB 국민 리브메이트카드',
            'KB 국민 다담카드',
            'KB 국민 해피포인트카드'
        ]),
        'card_brand': random.choice(['VISA', 'MasterCard', 'AMEX']),
        'is_trans_payable': random.choice([True, False]),
        'is_cash_card': random.choice([True, False]),
        'linked_bank_code': fake.iban(),
        'account_num': fake.bban(),
        'annual_fee': round(random.uniform(0, 100000), 0),
        'issue_date': fake.date()
    }


for _ in range(10):
    card_data = generate_fake_card_data()
    cursor.execute("""
        INSERT INTO card (card_name, card_brand, is_trans_payable, is_cash_card, linked_bank_code, account_num, annual_fee, issue_date)
        VALUES (:card_name, :card_brand, :is_trans_payable, :is_cash_card, :linked_bank_code, :account_num, :annual_fee, :issue_date)
    """, card_data)

conn.commit()

def generate_fake_customer_data():
    return {
        'name': fake.name(),
        'age': random.randint(18, 80),
        'sex': random.choice(['M', 'F']),
        'annual_salary': round(random.uniform(2000000, 900000000), 0), 
        'city': fake.city(),
        'address': fake.address()
    }

for _ in range(100):
    customer_data = generate_fake_customer_data()
    cursor.execute("""
        INSERT INTO customer (name, age, sex, annual_salary, city, address)
        VALUES (:name, :age, :sex, :annual_salary, :city, :address)
    """, customer_data)

conn.commit()

cursor.execute("SELECT customer_id FROM customer")
customer_ids = [row[0] for row in cursor.fetchall()]

def generate_fake_issued_card_data():
    return {
        'card_no': fake.credit_card_number(card_type=None),
        'card_id': random.randint(1, 10), 
        'valid_data': fake.date_between(start_date='-1y', end_date='+5y').strftime('%Y-%m-%d'),
        'is_annual_fee': random.choices([True, False], weights=[99, 1])[0],
        'is_valid': random.choices([True, False], weights=[99, 1])[0]
    }

for _ in range(100):
    issued_card_data = generate_fake_issued_card_data()
    cursor.execute("""
        INSERT INTO issued_card (card_no, card_id, valid_data, is_annual_fee, is_valid)
        VALUES (:card_no, :card_id, :valid_data, :is_annual_fee, :is_valid)
    """, issued_card_data)

conn.commit()

cursor.execute("SELECT card_no FROM issued_card")
card_nos = [row[0] for row in cursor.fetchall()]

def generate_fake_customer_own_card_data():
    return {
        'customer_id': random.choice(customer_ids),
        'card_no': random.choice(card_nos), 
        'own_date': fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d')
    }

for _ in range(200):
    customer_own_card_data = generate_fake_customer_own_card_data()
    cursor.execute("""
        INSERT INTO customer_own_card (customer_id, card_no, own_date)
        VALUES (:customer_id, :card_no, :own_date)
    """, customer_own_card_data)

conn.commit()    

cursor.execute("SELECT customer_id FROM customer")
customer_ids = [row[0] for row in cursor.fetchall()]

def generate_fake_point_data():
    return {
        'customer_id': random.choice(customer_ids),
        'point_cnt': random.randint(1, 10),
        'point_list': random.choice(goods),
        'point_name': fake.word(),
        'remain_point_amt': round(random.uniform(0, 100000), 0),
        'expiring_point_amt': round(random.uniform(0, 1000), 0)
    }

for _ in range(100):
    point_data = generate_fake_point_data()
    cursor.execute("""
        INSERT INTO point (customer_id, point_cnt, point_list, point_name, remain_point_amt, expiring_point_amt)
        VALUES (:customer_id, :point_cnt, :point_list, :point_name, :remain_point_amt, :expiring_point_amt)
    """, point_data)

conn.commit()

cursor.execute("SELECT card_no FROM issued_card")
card_nos = [row[0] for row in cursor.fetchall()]

def generate_fake_bill_data():
    bill_cnt =  random.randint(1, 10)
    return {
        'customer_id': random.choice(customer_ids),
        'card_no': random.choice(card_nos),
        'bill_cnt': bill_cnt,
        'bill_list': f'{random.choice(goods)} 외 {bill_cnt - 1}',
        'seqno': random.randint(1, 100),
        'charge_amt': round(random.uniform(1000, 100000), 0),
        'charge_day': random.randint(1, 28),
        'charge_month': fake.month_name(),
        'paid_out_date': fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d')
    }

for _ in range(100):
    bill_data = generate_fake_bill_data()
    cursor.execute("""
        INSERT INTO bill (customer_id, card_no, bill_cnt, bill_list, seqno, charge_amt, charge_day, charge_month, paid_out_date)
        VALUES (:customer_id, :card_no, :bill_cnt, :bill_list, :seqno, :charge_amt, :charge_day, :charge_month, :paid_out_date)
    """, bill_data)

conn.commit()

cursor.execute("SELECT bill_id FROM bill")
bill_ids = [row[0] for row in cursor.fetchall()]

def generate_fake_bill_add_data():
    bill_detail_cnt = random.randint(1, 10)
    return {
        'bill_id': random.choice(bill_ids),
        'bill_detail_cnt': bill_detail_cnt,
        'bill_detail_list': f'{random.choice(goods)} 외 {bill_detail_cnt - 1}',
        'card_no': random.choice(card_nos),
        'paid_dtime': fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
        'trans_no': fake.uuid4(),
        'paid_amt': round(random.uniform(1000, 10000000), 0),
        'currency_code': fake.currency_code(),
        'merchant_name': fake.company(),
        'merchant_regno': fake.ean13(),
        'credit_fee_amt': round(random.uniform(10, 100000), 0),
        'total_install_cnt': random.randint(1, 24),
        'cur_install_cnt': random.randint(1, 24),
        'balance_amt': round(random.uniform(1000, 5000000), 0),
        'prod_type': random.choice(business_types)
    }

for _ in range(100):
    bill_add_data = generate_fake_bill_add_data()
    cursor.execute("""
        INSERT INTO bill_add (bill_id, bill_detail_cnt, bill_detail_list, card_no, paid_dtime, trans_no, paid_amt, currency_code, merchant_name, merchant_regno, credit_fee_amt, total_install_cnt, cur_install_cnt, balance_amt, prod_type)
        VALUES (:bill_id, :bill_detail_cnt, :bill_detail_list, :card_no, :paid_dtime, :trans_no, :paid_amt, :currency_code, :merchant_name, :merchant_regno, :credit_fee_amt, :total_install_cnt, :cur_install_cnt, :balance_amt, :prod_type)
    """, bill_add_data)

conn.commit()    

def generate_fake_payment_data():
    pay_cnt = random.randint(1, 10)
    return {
        'bill_id': random.choice(bill_ids),
        'is_revolving': random.choice([True, False]),
        'pay_cnt': pay_cnt,
        'pay_list': f'{random.choice(goods)} 외 {pay_cnt - 1}',
        'seqno': random.randint(1, 100),
        'pay_due_date': fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d'),
        'pay_amt': round(random.uniform(1000, 100000), 0),
        'lump_sum_amt': round(random.uniform(1000, 50000), 0),
        'monthly_amt': round(random.uniform(100, 5000), 0),
        'loan_short_amt': round(random.uniform(100, 5000), 0),
        'revolving_amt': round(random.uniform(100, 5000), 0),
        'loan_long_amt': round(random.uniform(100, 5000), 0),
        'etc_amt': round(random.uniform(10, 1000), 0)
    }

for _ in range(100):
    payment_data = generate_fake_payment_data()
    cursor.execute("""
        INSERT INTO payment (bill_id, is_revolving, pay_cnt, pay_list, seqno, pay_due_date, pay_amt, lump_sum_amt, monthly_amt, loan_short_amt, revolving_amt, loan_long_amt, etc_amt)
        VALUES (:bill_id, :is_revolving, :pay_cnt, :pay_list, :seqno, :pay_due_date, :pay_amt, :lump_sum_amt, :monthly_amt, :loan_short_amt, :revolving_amt, :loan_long_amt, :etc_amt)
    """, payment_data)

conn.commit()

def generate_fake_domestic_approve_data():
    approved_cnt = random.randint(1, 10)
    return {
        'customer_id': random.choice(customer_ids),
        'card_no': random.choice(card_nos),
        'approved_cnt': approved_cnt,
        'approved_list': f'{random.choice(goods)} 외 {approved_cnt - 1}',
        'approved_dtime': fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
        'status': random.choices(['approved', 'declined'], weights=[99, 1])[0],
        'pay_type': random.choice(['credit', 'debit']),
        'trans_dtime': fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
        'merchant_name': fake.company(),
        'merchant_regno': fake.ean13(),
        'approved_amt': round(random.uniform(1000, 10000000), 0),
        'modified_amt': round(random.uniform(1000, 10000000), 0),
        'total_install_cnt': random.randint(1, 24)
    }


for _ in range(10000):
    domestic_approve_data = generate_fake_domestic_approve_data()
    cursor.execute("""
        INSERT INTO domestic_approve (customer_id, card_no, approved_cnt, approved_list, approved_dtime, status, pay_type, trans_dtime, merchant_name, merchant_regno, approved_amt, modified_amt, total_install_cnt)
        VALUES (:customer_id, :card_no, :approved_cnt, :approved_list, :approved_dtime, :status, :pay_type, :trans_dtime, :merchant_name, :merchant_regno, :approved_amt, :modified_amt, :total_install_cnt)
    """, domestic_approve_data)

conn.commit()    

def generate_fake_oversea_approve_data():
    approved_cnt = random.randint(1, 10)
    return {
        'customer_id': random.choice(customer_ids),
        'card_no': random.choice(card_nos),
        'approved_cnt': approved_cnt,
        'approved_list': f'{random.choice(goods)} 외 {approved_cnt - 1}',
        'approved_dtime': fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
        'status': random.choice(['approved', 'declined']),
        'pay_type': random.choice(['credit', 'debit']),
        'trans_dtime': fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
        'merchant_name': fake.company(),
        'approved_amt': round(random.uniform(1000, 100000), 0),
        'modified_amt': round(random.uniform(1000, 100000), 0),
        'country_code': fake.country_code(),
        'currency_code': fake.currency_code(),
        'krw_amt': round(random.uniform(1000, 100000), 0)
    }

for _ in range(5000):
    oversea_approve_data = generate_fake_oversea_approve_data()
    cursor.execute("""
        INSERT INTO oversea_approve (customer_id, card_no, approved_cnt, approved_list, approved_dtime, status, pay_type, trans_dtime, merchant_name, approved_amt, modified_amt, country_code, currency_code, krw_amt)
        VALUES (:customer_id, :card_no, :approved_cnt, :approved_list, :approved_dtime, :status, :pay_type, :trans_dtime, :merchant_name, :approved_amt, :modified_amt, :country_code, :currency_code, :krw_amt)
    """, oversea_approve_data)

conn.commit()

conn.close





















# Commit the changes
conn.commit()






















conn.close()








# # Generate sample data for cardholders
# for _ in range(100):
#     cursor.execute("INSERT INTO cardholders (name, email, address) VALUES (?, ?, ?)", 
#                    (fake.name(), fake.email(), fake.address()))


# card_types = ['visa16', 'jcb16', 'diners', 'discover']
# for cardholder_id in range(1, 101):
#     for _ in range(random.randint(1, 3)):  # Each cardholder has 1 to 3 credit cards
#         cursor.execute("INSERT INTO credit_cards (cardholder_id, card_number, card_type, expiration_date, cvv) VALUES (?, ?, ?, ?, ?)",
#                        (cardholder_id, fake.credit_card_number(card_type=random.choice(card_types)), 
#                         random.choice(card_types), fake.date_between(start_date='-5y', end_date='+5y'), 
#                         fake.random_number(digits=3)))

# # Generate sample data for transactions
# for credit_card_id in range(1, 201):
#     for _ in range(random.randint(5, 20)):  # Each credit card has 5 to 20 transactions
#         cursor.execute("INSERT INTO transactions (credit_card_id, amount, date, merchant) VALUES (?, ?, ?, ?)",
#                        (credit_card_id, round(random.uniform(5.0, 500.0), 0), 
#                         fake.date_between(start_date='-1y', end_date='today'), fake.company()))

















# # Commit the changes
# conn.commit()

# # Sample data insertion
# sample_data_statements = [
#     "INSERT INTO card (card_id, card_name, is_trans_payable, is_cash_card, linked_bank_code, account_num, card_brand, annual_fee, issue_date) VALUES (1, 'Sample Card', 1, 0, '001', '1234567890', 'VISA', 100.0, '2023-01-01')",
#     "INSERT INTO customer (customer_id, name, age, sex, annual_salary) VALUES (1, 'John Doe', 30, 'M', 50000.0)",
#     "INSERT INTO issued_card (card_no, card_id, valid_data, is_annual_fee, is_valid) VALUES (1, 1, '2025-01-01', 1, 1)",
#     "INSERT INTO customer_own_card (customer_id, card_no, own_date) VALUES (1, 1, '2023-01-01')",
#     "INSERT INTO point (customer_id, point_cnt, point_list, point_name, remain_point_amt, expiring_point_amt) VALUES (1, 100, 'Sample List', 'Sample Point', 50.0, 10.0)",
#     "INSERT INTO bill (bill_id, customer_id, card_no, bill_cnt, bill_list, seqno, charge_amt, charge_day, charge_month, paid_out_date) VALUES (1, 1, 1, 1, 'Sample List', 1, 100.0, 15, '2023-01', '2023-01-15')",
#     "INSERT INTO bill_add (bill_id, bill_add_id, bill_detail_cnt, bill_detail_list, card_id, paid_dtime, trans_no, paid_amt, currency_code, merchant_name, merchant_regno, credit_fee_amt, total_install_cnt, cur_install_cnt, balance_amt, prod_type) VALUES (1, 1, 1, 'Sample Detail List', 1, '2023-01-01 10:00:00', '123456', 100.0, 'KRW', 'Sample Merchant', '123-45-67890', 1.0, 12, 1, 90.0, 'Sample Type')",
#     "INSERT INTO payment (payment_id, bill_id, is_revolving, pay_cnt, pay_list, seqno, pay_due_date, pay_amt, lump_sum_amt, monthly_amt, loan_short_amt, revolving_amt, loan_long_amt, etc_amt) VALUES (1, 1, 0, 1, 'Sample Pay List', 1, '2023-01-15', 100.0, 50.0, 25.0, 10.0, 5.0, 5.0, 5.0)",
#     "INSERT INTO domestic_approve (customer_id, card_no, approved_cnt, approved_list, approved_num, approved_dtime, status, pay_type, trans_dtime, merchant_name, merchant_regno, approved_amt, modified_amt, total_install_cnt) VALUES (1, 1, 1, 'Sample Approve List', 1, '2023-01-01 10:00:00', 'Approved', 'Credit', '2023-01-01 11:00:00', 'Sample Merchant', '123-45-67890', 100.0, 90.0, 12)",
#     "INSERT INTO oversea_approve (customer_id, card_no, approved_cnt, approved_list, approved_num, approved_dtime, status, pay_type, trans_dtime, merchant_name, approved_amt, modified_amt, country_code, currency_code, krw_amt) VALUES (1, 1, 1, 'Sample Oversea Approve List', 1, '2023-01-01 10:00:00', 'Approved', 'Credit', '2023-01-01 11:00:00', 'Sample Merchant', 100.0, 90.0, 'US', 'USD', 110000.0)"
# ]

# # Execute sample data insertion statements
# for statement in sample_data_statements:
#     cursor.execute(statement)

# # Commit the changes
# conn.commit()

# Close the connection
