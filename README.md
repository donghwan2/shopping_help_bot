(2025.01.08 최종 수정)

# File Descriptions

- main.py

  - FastAPI app(BE Server)       -> uvicorn <파일명>:app --reload
- chatbot_function_calling.py

  - Streamlit(FE UI)                -> streamlit run <파일명.py>
- inference_by_Func_call_tone.py

  - Module : chatbot이 가져다 쓰는 도구들(function tools). main 서버에 requests 날리는 함수들.
- domain.py

  - DB. main 서버가 정보를 가져오는 곳.

# Project Structure

![project_structure](shop_helper_proj_structure.png)
