#
### 테이블명: card 설명:카드정보 
|컬럼|설명|
|-|-|
PK|card_id|카드ID|
|card_name|카드명|
|is_trans_payable|	교통 기능(여부)|
|is_cash_card|	현금카드기능(여부)|
|linked_bank_code|	결제은행(코드)|
|account_num|	결제계좌번호|
|card_brand|	카드브랜드(코드)|
|annual_fee|	상품 연회비|
|issue_date|	발급일자

### 테이블: customer 설명: 고객

|-|-|
|PK|customer_id|고객ID|
|name|이름|
|age|나이
|sex|성별
|annual_salary|연급여수준

### 테이블: issued_card 설명: 발급카드
|컬럼|설명|
|-|-|
PK|card_no|카드번호|
FK|card_id|카드명|
|valid_data|유효일자|
|is_annual_fee|연회비납부여부
|is_valid|유효여부

### 테이블: customeer_own_card 설명: 고객 보유 카드

|-|-|
FK|customer_id|고객ID|
PK|card_no|카드번호|
|own_date|보유일자|

### 테이블명: point 설명: 포인트 
|컬럼|설명|
|-|-|
FK|customer_id|고객ID|
|point_cnt|포인트수|
|point_list|포인트목록|
|point_name|포인트명|
|remain_point_amt|잔여포인트|
|expiring_point_amt|M+2월 소멸예정 포인트|

### 테이블명: bill 설명: 청구 기본정보 
|컬럼|설명|
|-|-|
PK|bill_id|청구ID|
FK|customer_id|고객ID|
FK|card_no|카드번호|
|bill_cnt|청구목록수|
|bill_list|청구목록|
|seqno|결제순번|
|charge_amt|월별 청구금액|
|charge_day|결제일|
|charge_month|청구년월|
|paid_out_date|결제년월일|

### 테이블명: bill_add 설명: 청구추가정보 
|컬럼|설명|
|-|-|
FK|bill_id|청구ID|
PK|bill_add_id|청구추가ID|
|bill_detail_cnt|청구상세목록수|
|bill_detail_list|청구상세목록|
|card_id|카드 식별자|
|paid_dtime|사용일시 또는 사용일자|
|trans_no|거래번호|
|paid_amt|이용금액|
|currency_code|통화코드(이용금액)|
|merchant_name|가맹점명|
|merchant_regno|가맹점 사업자등록번호|
|credit_fee_amt|신용판매 수수료|
|total_install_cnt|전체 할부회차|
|cur_install_cnt|현재 할부회차|
|balance_amt|할부 결제 후 잔액|
|prod_type|상품구분 (코드)|

### 테이블명: payment 설명: 결제정보 
|컬럼|설명|
|-|-|
PK|payment_id:결제ID|
FK|bill_id|청구ID|
|is_revolving|리볼빙 (여부)|
|pay_cnt|결제기본정보목록수|
|pay_list|결제기본정보목록|
|seqno|결제순번|
|pay_due_date|결제예정일|
|pay_amt|결제예정금액|
|lump_sum_amt|일시불|
|monthly_amt|할부|
|loan_short_amt|단기대출(현금서비스)|
|revolving_amt|리볼빙|
|loan_long_amt|장기대출(카드론,신용대출)|
|etc_amt|연회비 및 기타|

### 테이블명: domestic_approve 설명: 국내승인내역 
|컬럼|설명|
|-|-|
FK|customer_id|고객ID|
FK|card_no|카드번호|
|approved_cnt|국내승인목록수|
|approved_list|국내승인목록|
PK|approved_num|승인번호|
|approved_dtime|승인일시|
|status|결제상태 (코드)|
|pay_type|사용구분(신용/체크) (코드)|
|trans_dtime|정정 또는 승인취소 일시|
|merchant_name|가맹점명|
|merchant_regno|가맹점 사업자등록번호|
|approved_amt|이용금액|
|modified_amt|정정후 금액|
|total_install_cnt|전체 할부회차|

### 테이블명: oversea-approve 설명: 해외승인내역 
|컬럼|설명|
|-|-|
FK|customer_id|고객ID|
FK|card_no|카드번호|
|approved_cnt|해외승인목록수|
|approved_list|해외승인목록|
PK|approved_num|승인번호|
|approved_dtime|승인일시|
|status|결제상태 (코드)|
|pay_type|사용구분 (신용/체크) (코드)|
|trans_dtime|정정 또는 승인취소 일시|
|merchant_name|가맹점명|
|approved_amt|이용금액|
|modified_amt|정정후 금액|
|country_code|결제(승인) 국가코드|
|currency_code|결제(승인) 시 통화코드|
|krw_amt|원화|
