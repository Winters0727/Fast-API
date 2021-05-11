# Request Body

클라이언트에서 API 서버로 데이터를 보낼 때, request body를 통해 보내야한다. 클라이언트에서 API 서버로 request body를 보내면(`POST`, `PUT`, `PATCH`, `DELETE`), API 서버는 클라이언트에게 response body를 보낸다. API 서버는 항상 response body를 보내지만 클라이언트는 매번 request body를 보낼 필요가 없다.

request body를 선언할 때 **Pydantic**이 매우 유용하다.



### Pydantic의 BaseModel

```python
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel): # 데이터 모델 생성
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
```

데이터 모델을 생성할 때는 Pydantic의 `BaseModel`을 상속받는 클래스를 선언한다.

클래스의 모든 인자들은 파이썬 기본 타입들을 사용할 수 있다.

```python
class Item(BaseModel):
    name: str # str, 필수
    description: Optional[str] = None # str, 선택
    price: float # float, 필수
    tax: Optional[float] = None # float, 선택
```

쿼리 매개변수를 선언할 때와 마찬가지로 데이터 모델 클래스의 인자가 기본값을 가지면 선택 인자, 기본값이 없으면 필수 인자다.



**매개변수로 선언**

작업 경로를 추가할 때, 쿼리 매개변수를 선언했을 때와 같은 방법으로 생성한 데이터 모델을 선언하면 된다.

```python
@app.post("/items/")
async def create_item(item: Item):
    return item
```



**결과**

파이썬 타입 선언을 통해 FastAPI는

- request body를 JSON으로 읽는다.
- (필요하다면) 상응하는 타입으로 형변환을 한다.
- 데이터를 검증한다.
  - 데이터가 유효하지 않다면, 잘못된 데이터가 어떤 것인지 명확하게 알려주는 에러를 반환하는 것이 좋다.
- `item` 매개변수로 데이터를 받는다.
  - `Item` 데이터 모델 타입을 선언함으로써 편집기가 데이터 모델의 인자들의 값과 타입을 검증할 수 있게 도와준다.
- 모델에 사용할 JSON 스키마를 정의하면, 프로젝트 내에 어떤 곳에서든 사용이 가능하다.
- 여기서 스키마들은 생성된 OpenAPI의 스키마의 부분으로 문서의 UI에 자동으로 반영된다.



### 모델 사용

함수 내에서 데이터 모델 객체의 인자에 접근이 가능하다.

```python
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
```



### request body + 경로 매개변수

경로 매개변수와 request body를 동시에 선언할 수 있다.

FastAPI는 경로에 있는 경로 매개변수와 일치하는 함수 매개변수인지, request body로부터 가져와야하는 Pydantic 데이터 모델 클래스에 선언된 함수 매개변수들인지 구분한다.

```python
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item): # 함수 매개변수 item_id, item
    return {"item_id": item_id, **item.dict()}
```

`item_id`는 경로에 있으므로 경로 매개변수이며, URL에서 값을 가져온다. `item`은 타입이 Pydantic 데이터 모델 클래스이므로 request body에서 값을 가져온다.



### request body + 경로 + 쿼리 매개변수

request body, 경로, 쿼리 매개변수를 동시에 선언할 수 있다.

FastAPI는 각각이 어떤 역할을 하며, 어디에서 데이터를 가져와야 하는지 구분한다.

```python
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
```

함수 매개변수들은 다음과 같은 방법으로 구분된다.

- 매개변수가 경로에도 선언되었다면, 경로 매개변수로 해석한다.
- 매개변수가 단일 타입이라면 쿼리 매개변수로 해석한다.
- 매개변수가 Pydantic 데이터 모델 타입으로 선언되었다면, request body로 해석한다.



**Pydantic 없이...**

Pydantic 데이터 모델을 사용하기 싫다면 Body 매개변수를 사용할 수 있다.