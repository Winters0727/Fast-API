# 쿼리 매개변수와 문자열 검증

FastAPI는 매개변수에 추가적인 정보와 검증을 선언할 수 있다.

```python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
async def read_items(q: Optional[str] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```



**추가적인 검증**

쿼리 매개변수 `q`에 50글자 제한을 추가해보자.

```python
from typing import Optional

from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

지금까지 쿼리 매개변수 `q`의 기본값을 다음과 같이 암시적으로 선언했었다.

```python
q: Optional[str] = None
```

`Query(None)`은 이를 좀 더 명시적으로 선언한 것이다. 두 코드 모두 같은 의미다.

그 외에도 많은 검증을 추가할 수 있다.



**정규표현식 추가**

```python
async def read_items(q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^fixedquery$")):
```

- `^` : 정규식의 시작을 의미하는 문자. 이 앞에는 어떤 문자도 없다.
- `fixedquery` : 정확히 같아야할 문자열 `fixedquery`를 의미한다.
- `$` : 정규식의 끝을 의미하는 문자. 이 뒤에는 어떤 문자도 없다.



**필수 쿼리 매개변수**

쿼리 매개변수의 기본값을 설정하지 않으면 필수 쿼리 매개변수라고 앞에서 언급했다. `Query`를 사용할 경우에는 `None` 대신에 `...`를 넣으면 필수 쿼리 매개변수가 된다.

```python
async def read_items(q: Optional[str] = Query(..., min_length=3, max_length=50)):
```

`...`는 Ellipsis 연산자로 자세한건 문서를 참조하자.



### 쿼리 매개변수 리스트 / 다중값

쿼리 매개변수는 리스트를 받을 수 있다.

```python
from typing import List, Optional

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: Optional[List[str]] = Query(None)):
    query_items = {"q": q}
    return query_items
```

URL은 다음과 같이 작성된다.

```http
http://localhost:8000/items/?q=foo&q=bar
```

경로 작업 과정에서 쿼리 파라미터 `q`는 두개의 값을 받았고, 이는 파이썬 리스트로 응답을 반환한다.

```json
{
  "q": [
    "foo",
    "bar"
  ]
}
```

쿼리 매개변수를 다중값으로 사용할 때도 기본값을 지정해줄 수 있다.

```python
@app.get("/items/")
async def read_items(q: Optional[List[str]] = Query(["foo", "bar"])):
    query_items = {"q": q}
    return query_items
```

또는, 리스트로 직접 타입을 선언할 수 있다.

```python
@app.get("/items/")
async def read_items(q: list = Query([])):
    query_items = {"q": q}
    return query_items
```

