# 쿼리 매개변수

### 쿼리 매개변수

경로 매개변수의 일부가 아닌 다른 함수 매개변수를 선언할 때, "쿼리" 매개변수로 자동 해석한다.

```python
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/") # 경로에 매개변수가 없다.
async def read_item(skip: int = 0, limit: int = 10): # 경로에 매개변수가 없으므로 쿼리 매개변수로 자동 해석된다.
    return fake_items_db[skip : skip + limit]
```

 경로 매개변수에 적용된 동일한 프로세스가 쿼리 매개변수에도 적용된다.

- 편집기 지원
- 데이터 파싱
- 데이터 검증
- 자동 문서화



**기본값**

쿼리 매개변수는 경로에서 고정된 부분이 아니기 때문에 선택적일 수 있고, 기본값을 가질 수 있다.

```python
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10): # 기본값 : skip=0, limit=10
    return fake_items_db[skip : skip + limit]
```



**선택적 매개변수**

기본값을 `None`으로 설정하여 선택적 매개변수를 선언할 수 있다.

```python
from typing import Optional

...

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None): # q는 선택적 매개변수
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```

`Optional[str]`은 FastAPI가 아니라 편집기 단계에서 코드의 오류를 찾기 위한 타입 주석이다.



**쿼리 매개변수 형변환**

```python
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
```

매개변수 `short`는 `bool` 타입이지만 형변환 되어 URL에서는 여러가지 다른 값(`bool`의 형변환값)으로 나타난다.



**다수의 경로/쿼리 매개변수**

경로 매개변수와 쿼리 매개변수는 함께, 그리고 다수를 순서에 상관없이 선언할 수 있다.

```python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/users/{user_id}/items/{item_id}") # 경로 매개변수 : user_id, item_id
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
): # 쿼리 매개변수 : q, short
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
```



**필수 쿼리 매개변수**

경로 매개변수가 아닌 매개변수(쿼리 매개변수)에 대한 기본값을 선언하지 않는다면, 해당 쿼리 매개변수는 필수 쿼리 매개변수가 된다.

```python
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item
```

`needy`는 경로에 없으므로 쿼리 매개변수다. 그런데 기본값이 없으므로 `needy`는 필수 쿼리 매개변수다. 필수 쿼리 매개변수는 URL에 입력되지 않으면 에러 메세지를 반환한다.