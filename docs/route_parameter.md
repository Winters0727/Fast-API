# 경로 매개변수

### 경로 매개변수

```python
@app.get("/items/{item_id}") # 경로 매개변수는 중괄호안에 선언한다.
async def read_item(item_id): # 경로 매개변수를 함수 인자로 받는다.
    return {"item_id": item_id}
```



**매개변수 타입선언**

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int): # item_id 매개변수의 타입을 int로 선언
    return {"item_id": item_id} # 반환 시에 데이터를 자동으로 '파싱'한다.
# 타입 선언 시에 FastAPI는 데이터 검증 과정을 거치므로 다른 타입의 데이터를 받지 못한다.
```

데이터 검증은 **Pydantic**에 의해 내부적으로 수행된다. 파이썬 원시 자료형(`str`, `float`, `bool`) 외에도 복잡한 데이터 타입을 선언하여 사용할 수 있다.



**순서 문제**

경로 동작은 순차적으로 평가되기 때문에 경로 매개변수를 가지는 경로를 가장 마지막에 정의해야 한다.

```python
@app.get("/users/me") # 경로 매개변수보다 앞에서 정의해야 한다.
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}") # 경로 매개변수를 가지므로 뒤에서 정의한다.
async def read_user(user_id: str):
    return {"user_id": user_id}
```



### 사전정의 값

**Enum**

```python
from enum import Enum # python 3.4↑

from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName): # 타입 주석으로 Enum을 상속받은 ModelName 클래스를 사용했다.
    if model_name == ModelName.alexnet: # 열거형 멤버 비교
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet": # 열거형 값 비교
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"} # 열거형 멤버 반환
```



### 경로를 포함하는 매개변수

`/files/{file_path}`가 있는 경로 동작이 있다고 가정하자. 파일을 불러오려면 `home/winters/file.txt`처럼 파일 경로가 필요하므로 URL은 `/files/home/winters/file.txt`가 된다. OpenAPI는 경로를 포함하는 경로 매개변수를 내부에 선언하는 방법을 지원하지 않지만, Starlette의 내부 도구중 하나를 이용하여 FastAPI에서는 가능하다.



**경로 변환기**

Starlette에서 직접 옵션을 사용하여 URL에 경로를 포함하는 경로 매개변수를 선언할 수 있다.

`/files/{file_path:path}`

매개변수의 이름은 `file_path`이며, `:path`는 매개변수가 경로와 일치해야함을 알려준다.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/files/{files_path}:path")
async def read_file(file_path: str):
    return {"file_path": file_path}
```



### 요약

FastAPI에서 타입 주석을 통해 다음과 같은 장점을 가질 수 있다.

- 편집기 지원 : 오류 검사, 자동완성 등
- 데이터 파싱
- 데이터 검증
- API 주석과 자동 문서