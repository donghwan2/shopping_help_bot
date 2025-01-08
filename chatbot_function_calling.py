import streamlit as st

from dotenv import load_dotenv                 # api key 파일(.env) 관리
load_dotenv()

from openai import OpenAI
client = OpenAI()

import json
import requests

from inference_by_Func_call_tone import tools, get_product, get_order, get_shipping, system_msg_1

st.title("나만의 쇼핑 헬퍼")

# session_state에 시스템 메시지를 입력
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_msg_1}
    ]

# session_state 메시지 전체 출력(시스템 메시지는 제외)
for message in st.session_state.messages:
    if message['role'] == 'system':
        continue
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

# 사용자 입력창
prompt = st.chat_input("무엇이든 물어보세요!")

# 사용자 입력이 들어오면 화면에 표시하고, session_state에 저장함
if prompt:
    with st.chat_message("user"):     # 사용자 아이콘
       st.markdown(prompt)
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    
# session_state에 대해 챗봇이 gpt로 답변
with st.chat_message("assistant"):    # 챗봇 아이콘
    response = client. chat.completions.create(
        model="gpt-4o-mini",
        messages = st.session_state.messages,
        temperature=0,
        tools=tools
    )

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
                messages = st.session_state.messages[:-1] + [  # 기존 session_state + 
                    {"role": "user", "content": prompt}        # Function calling 기반 프롬프트
                ],
                temperature=0
                )
        # print(response_answer.choices[0].message.content)  # 상품번호가 1234567890인 상품은 '아이폰 16 Pro'이며, 현재 상태는 'NORMAL'입니다.

        answer = response_answer.choices[0].message.content
    else:
        answer = response.choices[0].message.content
    st.markdown(answer)

# 챗봇 답변을 session_state에 저장
st.session_state.messages.append(
    {"role": "assistant", "content": answer}
)

# 디버깅용 코드
for message in st.session_state.messages:
    print(message)
print()

