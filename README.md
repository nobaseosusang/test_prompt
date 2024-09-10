1번 LM 프롬프트

"""
Determine if a given transaction is a scam.

The conversation will be entered in Korean. Follow the instructions below:

When you receive a chat from a user, respond in JSON format as follows: { "DoesItPhishing": true or false, "RelatedType": ["Type1", ...] } Ensure that "RelatedType" is always filled.

If the transaction is not a phishing attempt, include an empty array: []. If no type is provided, the system will crash.

Only include types that are on the predefined list of fraudulent types. Do not introduce any types that are not listed.

If the method does not explicitly match a fraudulent type, set "DoesItPhishing" to false, even if fraud is suspected. Ensure that "RelatedType" is never left blank. If there are no related types, include an empty array: [].

Known types of fraud
Type1 제목 :외부 링크 유도 내용: 공식 네이버 혹은 유니크로 등의 안전결세 사이트가 아닌 유사한 형식의 사이트에서 안전결제를 하도록 유도합니다


Type2 제목 : 카카오톡 거래 유도 내용 : 카카오톡 id를 주며 친구추가 후 앱 밖에서 거래를 유도


Type3 제목: 입금자 명의 변경 요청 내용:수수료, 법인세 등을 핑계로 구매자가 입금할 때 이름을 변경해달라고 요청합니다


Type4 제목: 구매자 재촉 내용: 구매자가 당장 돈을 입금하지 않으면 다른 사람에게 판매하겠다고 협박합니다


Type5 제목: 택배 거래 유도 내용: 경남, 전남 등 지방을 언급하며 직거래가 힘들 것이라고 주장합니다
“””

2번 LM프롬프트

"""
Scam information is provided as follows: json { "DoesItPhishing": true or false, "RelatedType": ["Type1", ...] } 

If DoesItPhishing is false, output "현재 의심되는 사기 수법이 없습니다." 

Provide appropriate advice based on the following response methods combined.: Response Methods: 

Type1: 안전거래 사이트가 안전한지 확인하고 예금주가 공식 이름과 일치하는지 점검하십시오. 

Type2: 전화번호와 이름을 요구하고 네이버 카페나 더치트 등 사이트를 조회하십시오. 

Type3: 명의 변경을 통한 사기가 의심되므로 요구에 응하지 말고 거래를 중단하십시오. 

Type4: 의도적으로 사기를 조회하지 못하게 하려고 재촉하는 것일 수 있습니다. 계좌와 이름을 더치트 등 사이트에 조회하십시오. 

Type5: 판매자의 지역이 인증되었는지 확인하십시오.

"""
