from dotenv import load_dotenv                 # api key 파일(.env) 관리
load_dotenv()

from openai import OpenAI
client = OpenAI()

import json
import requests

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_product",
            "description": "Get the product by product_no",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_no": {"type": "number","description": "상품번호"}
            },
            "additionalProperties": False,
            "required": ["product_no"]
        },
        "strict": True
        }
    },
    {
        "type": "function",
        "function": {
        "name": "get_shipping",
        "description": "Get the shipping info by order_no, order_seq",
        "parameters": {
            "type": "object",
            "properties": {
                "order_no": {"type": "number","description": "주문번호"},
                "order_seq": {"type": "number","description": "주문순번"}
            },
            "additionalProperties": False,
            "required": ["order_no","order_seq"]
        },
        "strict": True
        }
    },
    {
        "type": "function",
        "function": {
        "name": "get_order",
        "description": "Get the order by order_no",
        "parameters": {
            "type": "object",
            "properties": {
                "order_no": {"type": "number","description": "주문번호"}
            },
            "additionalProperties": False,
            "required": ["order_no"]
        },
        "strict": True
        }
    }
]

# temperature=1,
# max_tokens=2048,
# top_p=1,
# frequency_penalty=0,
# presence_penalty=0

# FastAPI에 HTTP 통신(여기서는 GET) 하는 함수들
def get_product(product_no):
    return requests.get(f"http://127.0.0.1:8000/products/{product_no}").json()

def get_order(order_no):
    return requests.get(f"http://127.0.0.1:8000/order/{order_no}").json()

def get_shipping(order_no, order_seq):
    return requests.get(f"http://127.0.0.1:8000/shipping/{order_no}/{order_seq}").json()

system_msg_1 = """아래 말투 예시를 참고해서 채팅하세요.
이모지를 많이 사용하세요.

example1: 안녕하세요 !! 😊
example2: 궁금한 게 있다면 무엇이든 물어보세요 😀
example3: 주문이 미뤄지고 있어요 ㅠㅜㅠㅜ 😭
example4: 오늘 제일 핫한 이 상품을 확인해보세요~ 🍎🍎
example5: 잠시만 기다려주세요 !! 🙏
example6: 이 상품은 어떤가요 ?? 🍗
example7: 헐 ... 확인해볼게요 !! 😮
example8: 무슨 일 있나요 ?? 😨
example9: 저는 온라인 쇼핑을 즐겨해요 ~~ 👗
examp le10: 좋아하시는 음식 있나요 ?? 🥪"""

# 사용자 채팅이 입력되면 상품 관련 query 파라미터를 추출해서 리턴하는 함수
def inference_tone(message):    # message = "상품번호가 1234567890인 상품 찾아줘"
    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": system_msg_1},
            {"role": "user", "content": message}
        ],
        temperature=0,
        tools = tools
    )

    # 챗gpt 1차 답변
    print("########## 1차 답변 response.choices[0]: ", response.choices[0])  
    # Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, refusal=None, role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_WWQqXgHb4q87M4b7uYJAceGo', function=Function(arguments='{"product_no":123}', name='get_product'), type='function')]))
    
    # Function calling 관련 질문과 일반적 질문을 분기처리
    if response.choices[0].finish_reason == 'tool_calls':
        tool_name = response.choices[0].message.tool_calls[0].function.name
        tool_arguments = response.choices[0].message.tool_calls[0].function.arguments
        tool_arguments = json.loads(tool_arguments)
        # print(tool_name, "\n", tool_arguments)   # get_product  {"product_no":1234567890}

        # 어떤 tool 함수를 썼느냐에 따라 API에 요청하는 엔드포인트가 달라진다.
        if tool_name == "get_product":
            result = get_product(tool_arguments["product_no"])
        elif tool_name == "get_order":
            result = get_order(tool_arguments["order_no"])
        elif tool_name == "get_shipping":
            result = get_shipping(
                order_no = tool_arguments["order_no"],
                order_seq = tool_arguments["order_seq"]
            )
        # print(result)  # {'productNo': 1234567890, 'productName': '아이폰 16 Pro', 'productStatus': 'NORMAL'}

        # Function calling 답변 결과를 활용해서 프롬프트 작성 
        prompt = f"""context: {result}
        Q: {message}                  
        A: 
        """      # message : "상품번호가 1234567890인 상품 찾아줘"
    
        # 위에서 만들어낸 프롬프트로 다시 챗gpt에게 질문
        response_answer = client.chat.completions.create(
                model="gpt-4o-mini", 
                messages=[
                    {"role": "system", "content": system_msg_1},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
                )
        # print(response_answer.choices[0].message.content)  # 상품번호가 1234567890인 상품은 '아이폰 16 Pro'이며, 현재 상태는 'NORMAL'입니다.
        return response_answer.choices[0].message.content
    else:
        # 기본적인 챗gpt 답변
        return response.choices[0].message.content


if __name__ == "__main__":                                        # Function calling 함수들
    print(inference_tone("상품번호가 1234567890인 상품 찾아줘"))    # get_product()
    print("-------------------------------------")
    print(inference_tone("""다음 주문을 찾아주세요. 주문번호: 2024010101"""))   # get_order()
    print("-------------------------------------")
    print(inference_tone("배송조회를 하고 싶어. 주문번호는 2024010101이고 주문순번이 0이야."))   # get_shipping()
    print("-------------------------------------")
    print(inference_tone("딥러닝이 뭐야?"))                       # gpt

