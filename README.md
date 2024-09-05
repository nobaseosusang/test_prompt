# test_prompt

.env를 만들어서 api key를 입력해줘야 해요

ex) OPENAI_API_KEY="your api key"

테스트 결과 제일 적절한 프롬프트는

"""
당신은 중고 거래 사기 여부를 판단합니다. 지시사항은 다음과 같습니다

0.json 이외의 응답을 절대 하지 마십시오 

1.사용자에게 채팅 내용을 입력받으면 답변을 json의 형태로 만드십시오 형태는 다음과 같습니다 {”피싱여부” : True or False, “관련 유형"(True 일때만) : [”type1(적절히 변경)”, …]} 

2. 사기 유형 목록에 없는 유형으로는 대답하지 마십시오.

3. 사기 유형에 없는 방법이라면 사기가 의심되어도 피싱 여부는 False입니다
""""

이러면 적어도 딴짓은 안했던 것 같아요

지금 사용하는 프롬프트가 대충

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"현재 알려진 사기 유형: {fraud_types_text}. {prompt_text}"},
                {"role": "user", "content": conversation}
            ]
        )

이렇게 생겼는데 사기 타입에 맞는 대화는 어떻게 넣어줘야 할지 잘 모르겠어요

***예시 입출력***

2. Type2 제목 :외부 링크 유도 내용: http를 포함하는 인터넷 링크를 보내며 현재 메신저가 아닌 다른 곳에서 거래하도록 유도합니다. 
1. Type1 제목 : 카카오톡 유도 내용 : 카카오톡 id를 주며 친구추가 후 앱 밖에서 거래를 유도


계좌를 내놓거라
{ "피싱여부": false }

카카오톡 nobaseosusang 친추 ㄱ
{"피싱여부": True, "관련 유형": ["Type1"]}

https://unist.ac.kr 여기 안전거래 사이트니까 여기서 거래하시죠
{"피싱여부": True, "관련 유형": ["Type2"]}
