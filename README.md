# apps/
폴더 안에 `.streamlit/secrets.toml` 생성 후 OPENAI_API_KEY = "~~~" 작성

# 가상환경
`conda create -n devship-demo python=3.11`
`conda activate devship-demo`
`pip install -r requirements.txt`
`cd apps`
`streamlit run demo.py`


# TODO
- [] : langchain 들어내고 pystardog이랑 직접 연결 후 LLM Agent 직접 만들기
  - 프롬프트도 langchain 소스 참고해서 만들어 붙이기
  - 쿼리를 stardog db에 할 수 있게 
  - SparkQL 쿼리 생성 후 직접 stardog db에 쿼리하기!
