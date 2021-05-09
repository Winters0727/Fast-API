# 기본

### 설치

```bash
$pip install fastapi[all] # 애플리케이션을 운영 환경에 배포
$pip install uvicorn[standard] # 서버 역할
```



### 첫 API

**코드 작성**

```python
# main.py
from fastapi import FastAPI # FastAPI

app = FastAPI() # app 생성 (FastAPI 인스턴스 생성)

@app.get("/") # 애플리케이션 경로 설정
async def root(): # 비동기 함수
    return {"message": "Hello World"} # dict를 반환하면 JSON 형태로 보여진다.
# dict, list 외에도 단일값을 가지는 str, int 등을 반환할 수 있다.
```



**서버 실행**

```bash
$uvicorn main:app --reload
# main : main.py (파이썬 '모듈')
# app : main.py 내부의 'app = FastAPI()'로 생성된 객체
# --reload : 코드 변경 시 서버 재시작. 개발 시에만 사용
```



**문서화**

- **대화용 문서** : http://127.0.0.1:8000/docs (Swagger UI)

- **대안 API 문서** : http://127.0.0.1:8000/redoc (Open API)
