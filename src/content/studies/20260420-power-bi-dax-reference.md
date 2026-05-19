---
title: "Power BI — DAX 함수 레퍼런스 (부록 D)"
date: 2026-04-20
description: "DAX 함수·색인·예제를 함수 단위로 모은 부록이다."
tags: ["Power BI", "DAX"]
topic: "Power BI"
originalTitle: "Data Analysis Expressions (DAX)"
authors: "Microsoft Learn · dax.guide 기반"
sources:
  - title: "DAX 참조"
    url: "https://learn.microsoft.com/dax/"
---
## 부록 D: DAX 함수 레퍼런스

이 부록은 **읽고 바로 따라 할 수 있도록** 다음 순서로 구성한다.

1. **D.0 기초 개념과 샘플 모델** — 모든 예제에서 공통으로 쓰는 테이블(`Sales`, `'Date'`, `Product`, `Customer`)과 필터·행 컨텍스트, `CALCULATE`의 역할을 설명한다.
2. **D.1 실무 중심 심층 예제** — 가장 자주 쓰이는 약 140개 함수를 **시그니처 → 의미 → 입력 → DAX 식 → 결과**로 보여 준다.
3. **D.2 카테고리별 전 함수 색인** — dax.guide 사이트맵에서 확인한 DAX 함수 전수를 카테고리별로 나눠 한 줄 설명 + Microsoft Learn·DAX Guide 링크로 정리한다. 심층 예제에 포함된 함수도 색인에 함께 실어 완결성을 유지한다.

### D.0 기초 개념과 샘플 모델

**샘플 모델(예제에서 공통 사용)**:

| 테이블 | 주요 열 | 관계 |
| --- | --- | --- |
| `Sales` | `OrderId`, `OrderDate`, `ShipDate`, `CustomerId`, `ProductId`, `Qty`, `UnitPrice`, `Amount`(= Qty×UnitPrice), `Note` | `Sales[CustomerId] → Customer[Id]`, `Sales[ProductId] → Product[Id]`, `Sales[OrderDate] → 'Date'[Date]` |
| `'Date'` | `Date`, `Year`, `Quarter`, `Month`, `MonthName`, `DayOfWeek` | 날짜 테이블로 표시 |
| `Customer` | `Id`, `Name`, `Country`, `Email` | |
| `Product` | `Id`, `Name`, `Category`, `Color`, `Cost` | |

**샘플 데이터 일부**:

```
Sales
OrderId | OrderDate   | CustomerId | ProductId | Qty | UnitPrice | Amount
1001    | 2026-01-03  | C001       | P001      | 2   | 100       | 200
1002    | 2026-01-05  | C002       | P002      |10   |  20       | 200
1003    | 2026-02-11  | C001       | P003      | 1   | 500       | 500
1004    | 2026-03-02  | C003       | P001      | 5   | 100       | 500
```

**필터 컨텍스트(Filter context)**: 보고서 시각화의 축·슬라이서·페이지 필터로 만들어지는 **WHERE 조건 모음**. 측정값이 평가될 때 이 조건으로 테이블이 먼저 걸러진다.

**행 컨텍스트(Row context)**: 계산 열과 `SUMX`·`FILTER` 같은 **행 반복 함수(iterator)** 내부에서만 존재한다. 행 하나를 가리키고, 그 행의 열 값을 식에서 직접 참조할 수 있다. 행 컨텍스트에서 다른 테이블 열을 보려면 `RELATED`가 필요하다.

**CALCULATE**: 필터 컨텍스트를 **수정하고** 식을 다시 평가한다. 인수로 주어지는 열=값 형태의 조건은 내부적으로 `FILTER(ALL(<table>), ...)`로 해석된다. `CALCULATE` 호출은 동시에 **행 컨텍스트 → 필터 컨텍스트 전환**을 수행하므로, 계산 열 내부에서 측정값을 호출하면 자동으로 `CALCULATE`로 감싸는 효과가 난다.

**VAR / RETURN**: 중간 결과를 변수에 담아 **한 번만 평가**하고 재사용한다. 가독성·성능 모두에서 권장.

```
[Profit Margin] =
VAR _sales = SUM(Sales[Amount])
VAR _cost = SUMX(Sales, Sales[Qty] * RELATED(Product[Cost]))
RETURN DIVIDE(_sales - _cost, _sales)
```

이 절의 모든 예제는 위 샘플 모델을 전제로 한다. `[측정값]` 대괄호 표기는 측정값 이름을 의미하며 테이블 참조가 생략된 형태이다.

### D.1 실무 중심 심층 예제

카테고리 순서대로 가장 자주 쓰이는 함수를 **시그니처 → 의미 → 입력 → DAX 식 → 결과** 형식으로 정리했다. 예제는 D.0의 샘플 모델을 전제로 한다.

#### 분류: 집계(Aggregation)

##### AVERAGE

- **시그니처**: `AVERAGE(<column>)`
- **의미**: 숫자 열의 산술 평균을 계산한다.
- **입력 예**: `Sales[Amount]` = { 100, 200, 300 }
- **DAX 식**:

    ```DAX
    [Avg Amount] = AVERAGE(Sales[Amount])
    ```

- **결과**: 200
- **주의**: 빈 값은 **개수에서 제외**된다. 0이 포함되면 평균이 달라진다.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/average-function-dax) · [DAX Guide](https://dax.guide/average/)

##### AVERAGEX

- **시그니처**: `AVERAGEX(<table>, <expression>)`
- **의미**: 테이블의 각 행에 식을 평가해 평균을 낸다. 식 내부에서 행 간 곱셈·비교가 필요한 경우에 쓴다.
- **입력 예**: Sales = { (Qty=2, UnitPrice=10), (Qty=3, UnitPrice=20) }
- **DAX 식**:

    ```DAX
    [Avg Line Revenue] = AVERAGEX(Sales, Sales[Qty] * Sales[UnitPrice])
    ```

- **결과**: (20 + 60) / 2 = 40
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/averagex-function-dax) · [DAX Guide](https://dax.guide/averagex/)

##### COUNT

- **시그니처**: `COUNT(<column>)`
- **의미**: 숫자·날짜·논리 열에서 **비어 있지 않은 값의 개수**를 센다.
- **입력 예**: Sales 행 5개 중 OrderId BLANK 1개
- **DAX 식**:

    ```DAX
    [Order Count] = COUNT(Sales[OrderId])
    ```

- **결과**: 4
- **주의**: 텍스트 열에는 `COUNTA`를 쓴다.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/count-function-dax) · [DAX Guide](https://dax.guide/count/)

##### COUNTA

- **시그니처**: `COUNTA(<column>)`
- **의미**: 빈 값을 제외한 **모든 형식**의 값 개수를 센다. 텍스트 열에 유용.
- **DAX 식**:

    ```DAX
    [With Note] = COUNTA(Sales[Note])
    ```

- **결과**: Sales 5행 중 Note가 비어있지 않은 3행 → 3
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/counta-function-dax) · [DAX Guide](https://dax.guide/counta/)

##### COUNTBLANK

- **시그니처**: `COUNTBLANK(<column>)`
- **의미**: 열에서 BLANK(공란)의 개수를 센다. 데이터 품질 측정에 유용.
- **DAX 식**:

    ```DAX
    [Missing Email] = COUNTBLANK(Customer[Email])
    ```

- **결과**: 빈 이메일 행 수
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/countblank-function-dax) · [DAX Guide](https://dax.guide/countblank/)

##### COUNTROWS

- **시그니처**: `COUNTROWS(<table>)`
- **의미**: 테이블(또는 식의 결과 테이블) 행 수를 센다. 집계 중 가장 명확·빠른 함수.
- **DAX 식**:

    ```DAX
    [Sales Lines] = COUNTROWS(Sales)
    ```

- **결과**: 예: 1204
- **주의**: `COUNT(Sales[OrderId])`는 빈 값을 빼지만 `COUNTROWS`는 BLANK 행도 포함한다.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/countrows-function-dax) · [DAX Guide](https://dax.guide/countrows/)

##### COUNTX

- **시그니처**: `COUNTX(<table>, <expression>)`
- **의미**: 식이 비어 있지 않은 행의 수를 센다. 필터 조건을 카운트로 표현할 때 쓴다.
- **DAX 식**:

    ```DAX
    [Big Orders] = COUNTX(Sales, IF(Sales[Amount] > 1000, 1))
    ```

- **결과**: Amount > 1000 인 행의 수
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/countx-function-dax) · [DAX Guide](https://dax.guide/countx/)

##### DISTINCTCOUNT

- **시그니처**: `DISTINCTCOUNT(<column>)`
- **의미**: 열의 **고유 값 수**(BLANK 포함).
- **DAX 식**:

    ```DAX
    [Customers] = DISTINCTCOUNT(Sales[CustomerId])
    ```

- **결과**: 예: 57
- **주의**: BLANK를 세고 싶지 않으면 `DISTINCTCOUNTNOBLANK`.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/distinctcount-function-dax) · [DAX Guide](https://dax.guide/distinctcount/)

##### DISTINCTCOUNTNOBLANK

- **시그니처**: `DISTINCTCOUNTNOBLANK(<column>)`
- **의미**: 열의 고유 값 수에서 BLANK를 제외한다.
- **DAX 식**:

    ```DAX
    [Customers (no blank)] = DISTINCTCOUNTNOBLANK(Sales[CustomerId])
    ```

- **결과**: 예: 56
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/distinctcountnoblank-function-dax) · [DAX Guide](https://dax.guide/distinctcountnoblank/)

##### MAX

- **시그니처**: `MAX(<column>)`
- **의미**: 숫자·날짜 열의 최댓값을 반환한다.
- **DAX 식**:

    ```DAX
    [Latest Order] = MAX(Sales[OrderDate])
    ```

- **결과**: 2026-04-20
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/max-function-dax) · [DAX Guide](https://dax.guide/max/)

##### MAXX

- **시그니처**: `MAXX(<table>, <expression>)`
- **의미**: 각 행에서 평가한 식의 최댓값을 돌려주는 행 반복 함수.
- **DAX 식**:

    ```DAX
    [Max Line Revenue] = MAXX(Sales, Sales[Qty] * Sales[UnitPrice])
    ```

- **결과**: 60
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/maxx-function-dax) · [DAX Guide](https://dax.guide/maxx/)

##### MIN

- **시그니처**: `MIN(<column>)`
- **의미**: 숫자·날짜 열의 최솟값을 반환한다.
- **입력 예**: Sales[OrderDate] 최솟값이 2026-01-03
- **DAX 식**:

    ```DAX
    [First Order] = MIN(Sales[OrderDate])
    ```

- **결과**: 2026-01-03
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/min-function-dax) · [DAX Guide](https://dax.guide/min/)

##### MINX

- **시그니처**: `MINX(<table>, <expression>)`
- **의미**: 각 행에서 평가한 식의 최솟값을 돌려주는 행 반복 함수.
- **입력 예**: Sales = { (2, 10), (3, 20) } → 20, 60
- **DAX 식**:

    ```DAX
    [Min Line Revenue] = MINX(Sales, Sales[Qty] * Sales[UnitPrice])
    ```

- **결과**: 20
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/minx-function-dax) · [DAX Guide](https://dax.guide/minx/)

##### PRODUCTX

- **시그니처**: `PRODUCTX(<table>, <expression>)`
- **의미**: 각 행에서 평가한 식의 **곱**을 반환한다(복합 성장률 등에 사용).
- **DAX 식**:

    ```DAX
    [Compound Growth] = PRODUCTX('Growth', 1 + 'Growth'[Rate]) - 1
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/productx-function-dax) · [DAX Guide](https://dax.guide/productx/)

##### SUM

- **시그니처**: `SUM(<column>)`
- **의미**: 한 숫자 열의 모든 값을 단순 합계한다. 내부적으로 `SUMX(VALUES(...), ...)`에 가깝게 동작하며 필터 컨텍스트를 존중한다.
- **입력 예**: `Sales[Amount]` = { 100, 200, 300 }
- **DAX 식**:

    ```DAX
    [Total Amount] = SUM(Sales[Amount])
    ```

- **결과**: 600
- **주의**: 빈(BLANK) 값은 무시, 비숫자가 섞이면 오류. 문자열 형태 숫자는 자동 변환되지 않는다.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/sum-function-dax) · [DAX Guide](https://dax.guide/sum/)

##### SUMX

- **시그니처**: `SUMX(<table>, <expression>)`
- **의미**: 테이블의 각 행에 식을 평가한 뒤 결과를 합산하는 행 반복 함수(iterator). 각 행이 **행 컨텍스트**를 만든다.
- **입력 예**: Sales = { (Qty=2, UnitPrice=10), (Qty=3, UnitPrice=20) }
- **DAX 식**:

    ```DAX
    [Revenue] = SUMX(Sales, Sales[Qty] * Sales[UnitPrice])
    ```

- **결과**: 2*10 + 3*20 = 80
- **주의**: 행 컨텍스트에서 다른 테이블 열을 참조하려면 `RELATED`가 필요하다.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/sumx-function-dax) · [DAX Guide](https://dax.guide/sumx/)

#### 분류: 논리(Logical)

##### AND

- **시그니처**: `AND(<logical1>, <logical2>)`
- **의미**: 두 식이 모두 TRUE면 TRUE. 연산자 `&&`와 동일하며 두 개 이상에는 `&&`가 가독성이 좋다.
- **DAX 식**:

    ```DAX
    IF(AND(Sales[Amount] > 1000, Sales[Qty] > 10), "VIP", "")
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/and-function-dax) · [DAX Guide](https://dax.guide/and/)

##### COALESCE

- **시그니처**: `COALESCE(<value1>, <value2>, ...)`
- **의미**: 첫 번째 **비-BLANK** 값을 반환한다. `IF(ISBLANK(x), y, x)`의 간결한 대안.
- **DAX 식**:

    ```DAX
    [Revenue Safe] = COALESCE(SUM(Sales[Amount]), 0)
    ```

- **결과**: 빈 필터에서 BLANK 대신 0
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/coalesce-function-dax) · [DAX Guide](https://dax.guide/coalesce/)

##### FALSE

- **시그니처**: `FALSE()`
- **의미**: 상수 FALSE.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/false-function-dax) · [DAX Guide](https://dax.guide/false/)

##### IF

- **시그니처**: `IF(<logical>, <value_if_true>, [<value_if_false>])`
- **의미**: 조건이 참이면 첫 값을, 아니면 둘째 값을 반환. 셋째 인수 생략 시 BLANK.
- **입력 예**: Amount=1500 행 → "High", Amount=200 행 → "Low"
- **DAX 식**:

    ```DAX
    [Segment] = IF(Sales[Amount] >= 1000, "High", "Low")
    ```

- **결과**: 각 행마다 문자열 라벨
- **주의**: 반환 타입이 두 가지면 두 분기의 데이터 형이 일치해야 예측 가능한 결과가 나온다. 복잡한 분기에는 `SWITCH`가 좋다.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/if-function-dax) · [DAX Guide](https://dax.guide/if/)

##### IFERROR

- **시그니처**: `IFERROR(<value>, <value_if_error>)`
- **의미**: 첫 식이 오류를 발생시키면 두 번째 식을 대신 반환한다.
- **DAX 식**:

    ```DAX
    [Ratio Safe] = IFERROR(DIVIDE(Sales[Amount], Sales[Qty]), 0)
    ```

- **결과**: Qty=0인 행에서도 오류 대신 0
- **주의**: 가능하면 `DIVIDE` 자체의 오류 방지를 먼저 쓰는 것이 빠르다.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/iferror-function-dax) · [DAX Guide](https://dax.guide/iferror/)

##### NOT

- **시그니처**: `NOT(<logical>)`
- **의미**: 논리값을 뒤집는다.
- **DAX 식**:

    ```DAX
    FILTER(Sales, NOT(ISBLANK(Sales[Discount])))
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/not-function-dax) · [DAX Guide](https://dax.guide/not/)

##### OR

- **시그니처**: `OR(<logical1>, <logical2>)`
- **의미**: 둘 중 하나만 TRUE면 TRUE. 연산자 `||`와 동일.
- **DAX 식**:

    ```DAX
    IF(OR(Customer[Country]="KR", Customer[Country]="JP"), 1, 0)
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/or-function-dax) · [DAX Guide](https://dax.guide/or/)

##### SWITCH

- **시그니처**: `SWITCH(<expression>, <v1>, <r1>, [v2, r2, ...], [<else>])`
- **의미**: 식 결과와 값 목록을 차례로 비교해 일치하는 결과를 돌려준다. `SWITCH(TRUE(), ...)` 패턴으로 다중 조건 분기에도 사용.
- **DAX 식**:

    ```DAX
    [Grade] = SWITCH(TRUE(), [Score] >= 90, "A", [Score] >= 80, "B", "C")
    ```

- **결과**: 점수별 A/B/C
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/switch-function-dax) · [DAX Guide](https://dax.guide/switch/)

##### TRUE

- **시그니처**: `TRUE()`
- **의미**: 상수 TRUE. `SWITCH(TRUE(), ...)` 패턴에 자주 쓴다.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/true-function-dax) · [DAX Guide](https://dax.guide/true/)

#### 분류: 필터(Filter)

##### ALL

- **시그니처**: `ALL([<table> | <column>[, <column>, ...]])`
- **의미**: 지정한 테이블 또는 열의 **필터를 제거**한 테이블을 돌려준다. `CALCULATE`의 필터 인수로 넣어 컨텍스트를 무시한다.
- **DAX 식**:

    ```DAX
    [Total (All Years)] = CALCULATE(SUM(Sales[Amount]), ALL('Date'))
    ```

- **결과**: 슬라이서·열 필터 무관 연도 합계
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/all-function-dax) · [DAX Guide](https://dax.guide/all/)

##### ALLEXCEPT

- **시그니처**: `ALLEXCEPT(<table>, <column1>[, <column2>, ...])`
- **의미**: 지정한 열 **외에는** 전부 필터 제거. 상위 총계 비율 계산 시 표준 패턴.
- **DAX 식**:

    ```DAX
    [% of Country] = DIVIDE([Sales], CALCULATE([Sales], ALLEXCEPT(Customer, Customer[Country])))
    ```

- **결과**: 각 행이 속한 국가 내 비중
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/allexcept-function-dax) · [DAX Guide](https://dax.guide/allexcept/)

##### ALLSELECTED

- **시그니처**: `ALLSELECTED([<table_or_column>])`
- **의미**: <strong>시각적 개체 외부 필터</strong>(슬라이서·페이지 필터)는 유지하고, **내부 좌표 축 필터**만 제거한다. “보이는 데이터 대비 비율”을 구할 때 쓴다.
- **DAX 식**:

    ```DAX
    [% Visible] = DIVIDE([Sales], CALCULATE([Sales], ALLSELECTED(Sales)))
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/allselected-function-dax) · [DAX Guide](https://dax.guide/allselected/)

##### CALCULATE

- **시그니처**: `CALCULATE(<expression>, [<filter1>, <filter2>, ...])`
- **의미**: 식을 **변경된 필터 컨텍스트**에서 평가한다. DAX에서 가장 중요한 함수이며, 행 컨텍스트를 필터 컨텍스트로 **컨텍스트 전환**하는 역할도 한다.
- **DAX 식**:

    ```DAX
    [Sales KR] = CALCULATE(SUM(Sales[Amount]), Customer[Country] = "KR")
    ```

- **결과**: 전체 Amount 1,000,000 중 KR 고객분 230,000
- **주의**: 암시적 필터 인수는 자동으로 `FILTER(ALL(table), ...)` 로 변환된다. 기존 필터를 유지하려면 `KEEPFILTERS(...)`를 감싼다.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/calculate-function-dax) · [DAX Guide](https://dax.guide/calculate/)

##### CALCULATETABLE

- **시그니처**: `CALCULATETABLE(<table_expr>, [<filter1>, ...])`
- **의미**: `CALCULATE`의 테이블 반환 버전. 변경된 컨텍스트에서 테이블을 돌려준다.
- **DAX 식**:

    ```DAX
    Top Customers KR = CALCULATETABLE(TOPN(10, Customer, [Revenue]), Customer[Country]="KR")
    ```

- **결과**: KR 고객 중 매출 상위 10행 테이블
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/calculatetable-function-dax) · [DAX Guide](https://dax.guide/calculatetable/)

##### CROSSFILTER

- **시그니처**: `CROSSFILTER(<col1>, <col2>, <direction>)`
- **의미**: 특정 계산에서만 관계의 교차 필터 방향을 바꾼다. `None`/`OneWay`/`Both`.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/crossfilter-function-dax) · [DAX Guide](https://dax.guide/crossfilter/)

##### FILTER

- **시그니처**: `FILTER(<table>, <condition>)`
- **의미**: 테이블에서 조건을 만족하는 **행만** 남긴다. `CALCULATE`의 부울식 필터보다 복잡한 조건을 쓸 때 사용.
- **DAX 식**:

    ```DAX
    [High Qty Sales] = CALCULATE(SUM(Sales[Amount]), FILTER(Sales, Sales[Qty] > 10))
    ```

- **결과**: Qty>10인 행만의 Amount 합
- **주의**: `FILTER(ALL(Sales), ...)` 처럼 `ALL`과 자주 조합해 “모든 행 중 조건”을 만든다.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/filter-function-dax) · [DAX Guide](https://dax.guide/filter/)

##### HASONEFILTER

- **시그니처**: `HASONEFILTER(<column>)`
- **의미**: 열에 **필터 자체가 1개**인지 확인한다(값이 1개와는 미묘하게 다르다).
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/hasonefilter-function-dax) · [DAX Guide](https://dax.guide/hasonefilter/)

##### HASONEVALUE

- **시그니처**: `HASONEVALUE(<column>)`
- **의미**: 열이 정확히 1개 값으로 필터되어 있으면 TRUE.
- **DAX 식**:

    ```DAX
    IF(HASONEVALUE('Date'[Year]), [YoY], BLANK())
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/hasonevalue-function-dax) · [DAX Guide](https://dax.guide/hasonevalue/)

##### ISCROSSFILTERED

- **시그니처**: `ISCROSSFILTERED(<table_or_column>)`
- **의미**: 다른 테이블의 관계 경로로 **교차 필터**되어 있는지 검사.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/iscrossfiltered-function-dax) · [DAX Guide](https://dax.guide/iscrossfiltered/)

##### ISFILTERED

- **시그니처**: `ISFILTERED(<table_or_column>)`
- **의미**: 직접 필터가 걸려 있는지 검사.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/isfiltered-function-dax) · [DAX Guide](https://dax.guide/isfiltered/)

##### KEEPFILTERS

- **시그니처**: `KEEPFILTERS(<expression>)`
- **의미**: `CALCULATE`의 필터 인수를 감싸, 같은 열의 기존 필터를 **대체하지 않고 교집합**으로 적용한다.
- **DAX 식**:

    ```DAX
    [Sales HE] = CALCULATE([Sales], KEEPFILTERS(Product[Color] = "Red"))
    ```

- **결과**: 기존 슬라이서로 고른 색 중 Red도 포함된 행만
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/keepfilters-function-dax) · [DAX Guide](https://dax.guide/keepfilters/)

##### LOOKUPVALUE

- **시그니처**: `LOOKUPVALUE(<result_col>, <search_col1>, <search_value1>[, ...])`
- **의미**: 조건을 만족하는 **단일 행**의 값을 돌려준다. 관계가 없을 때도 동작.
- **DAX 식**:

    ```DAX
    [Country] = LOOKUPVALUE(Customer[Country], Customer[Id], Sales[CustomerId])
    ```

- **주의**: 여러 행이 일치하면 오류. 네 번째 인수로 대체 값을 지정할 수 있다.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/lookupvalue-function-dax) · [DAX Guide](https://dax.guide/lookupvalue/)

##### REMOVEFILTERS

- **시그니처**: `REMOVEFILTERS([<table> | <column>[, ...]])`
- **의미**: `CALCULATE`의 **수식 한정 필터 인수**로 설계된 `ALL`의 명시적 대안. 필터만 제거하고 테이블을 반환하지 않는다.
- **DAX 식**:

    ```DAX
    [Grand Total] = CALCULATE([Sales], REMOVEFILTERS())
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/removefilters-function-dax) · [DAX Guide](https://dax.guide/removefilters/)

##### SELECTEDVALUE

- **시그니처**: `SELECTEDVALUE(<column>[, <alternate>])`
- **의미**: 현재 필터 컨텍스트에서 열에 **정확히 하나**의 값만 있으면 그 값, 아니면 대체 값(기본 BLANK)을 돌려준다.
- **DAX 식**:

    ```DAX
    [Current Country] = SELECTEDVALUE(Customer[Country], "(여러 국가)")
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/selectedvalue-function-dax) · [DAX Guide](https://dax.guide/selectedvalue/)

##### TREATAS

- **시그니처**: `TREATAS(<expression>, <column>[, <column>, ...])`
- **의미**: <strong>관계가 없는</strong> 테이블 간에도 열 값을 필터로 **가상 연결**한다.
- **DAX 식**:

    ```DAX
    VAR kr_ids = VALUES(Customer[Id]) RETURN CALCULATE([Sales Foreign], TREATAS(kr_ids, Foreign[CustId]))
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/treatas-function-dax) · [DAX Guide](https://dax.guide/treatas/)

##### USERELATIONSHIP

- **시그니처**: `USERELATIONSHIP(<col1>, <col2>)`
- **의미**: `CALCULATE`의 수식 한정 인수. **비활성 관계**를 이번 평가에만 활성화한다.
- **DAX 식**:

    ```DAX
    [Sales by Ship Date] = CALCULATE([Sales], USERELATIONSHIP(Sales[ShipDate], 'Date'[Date]))
    ```

- **주의**: 비활성 관계가 이미 모델 뷰에 정의되어 있어야 동작한다.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/userelationship-function-dax) · [DAX Guide](https://dax.guide/userelationship/)

#### 분류: 관계(Relationships)

##### RELATED

- **시그니처**: `RELATED(<column>)`
- **의미**: 현재 **행 컨텍스트**에서 관계의 ‘1’ 쪽 테이블의 열 값을 가져온다. 계산 열과 이터레이터 안에서 사용.
- **DAX 식**:

    ```DAX
    Sales[Country] = RELATED(Customer[Country])
    ```

- **결과**: 각 Sales 행에 고객 국가 값 추가
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/related-function-dax) · [DAX Guide](https://dax.guide/related/)

##### RELATEDTABLE

- **시그니처**: `RELATEDTABLE(<table>)`
- **의미**: 현재 행에 연결된 **다대일의 다(多)쪽** 테이블 서브셋을 반환한다.
- **DAX 식**:

    ```DAX
    Customer[Orders Count] = COUNTROWS(RELATEDTABLE(Sales))
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/relatedtable-function-dax) · [DAX Guide](https://dax.guide/relatedtable/)

#### 분류: 테이블(Table)

##### ADDCOLUMNS

- **시그니처**: `ADDCOLUMNS(<table>, <name1>, <expr1>[, ...])`
- **의미**: 테이블에 계산 열을 추가한 **새 테이블**을 반환한다. 시각화에 직접 보이는 계산 테이블 생성에 사용.
- **DAX 식**:

    ```DAX
    EVALUATE ADDCOLUMNS(VALUES(Customer[Country]), "Sales", [Total Sales])
    ```

- **결과**: 국가 | Sales 두 열의 테이블
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/addcolumns-function-dax) · [DAX Guide](https://dax.guide/addcolumns/)

##### CROSSJOIN

- **시그니처**: `CROSSJOIN(<table1>, <table2>[, ...])`
- **의미**: 모든 행의 카르테시안 곱.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/crossjoin-function-dax) · [DAX Guide](https://dax.guide/crossjoin/)

##### DATATABLE

- **시그니처**: `DATATABLE(<col1_name>, <col1_type>, ..., {{<row1>}, ...})`
- **의미**: DAX 내부에서 **정적 데이터 테이블**을 정의한다. 룩업 상수 테이블에 쓰인다.
- **DAX 식**:

    ```DAX
    DATATABLE("Grade", STRING, "Min", INTEGER, {{"A", 90}, {"B", 80}})
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/datatable-function-dax) · [DAX Guide](https://dax.guide/datatable/)

##### DISTINCT

- **시그니처**: `DISTINCT(<table_or_column>)`
- **의미**: BLANK를 포함해 **중복을 제거**한 테이블/열 값을 반환. `VALUES`와 달리 모델에 의해 자동 추가되는 빈 행(관계 위반)을 포함하지 않는다.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/distinct-function-dax) · [DAX Guide](https://dax.guide/distinct/)

##### EXCEPT

- **시그니처**: `EXCEPT(<table1>, <table2>)`
- **의미**: `<table1>`에서 `<table2>`의 행을 뺀 차집합.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/except-function-dax) · [DAX Guide](https://dax.guide/except/)

##### GENERATE

- **시그니처**: `GENERATE(<table1>, <table2_expr>)`
- **의미**: 왼쪽 테이블의 각 행마다 오른쪽 식을 평가해 **조인** 하듯 결합. 오른쪽이 빈 테이블이면 행이 제외된다.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/generate-function-dax) · [DAX Guide](https://dax.guide/generate/)

##### GENERATEALL

- **시그니처**: `GENERATEALL(<table1>, <table2_expr>)`
- **의미**: `GENERATE`와 유사하나 오른쪽이 비어도 왼쪽 행은 NULL과 함께 남긴다(왼쪽 외부 조인).
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/generateall-function-dax) · [DAX Guide](https://dax.guide/generateall/)

##### GENERATESERIES

- **시그니처**: `GENERATESERIES(<start>, <end>[, <increment>])`
- **의미**: 시작/끝/간격으로 **숫자 시퀀스 테이블**을 만든다. 파라미터 슬라이서용.
- **DAX 식**:

    ```DAX
    GENERATESERIES(0, 100, 10)
    ```

- **결과**: Value 열 { 0, 10, 20, ..., 100 }
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/generateseries-function-dax) · [DAX Guide](https://dax.guide/generateseries/)

##### GROUPBY

- **시그니처**: `GROUPBY(<table>, <groupCol1>[, ...][, <name>, <expression>])`
- **의미**: `SUMMARIZE`의 확장. `CURRENTGROUP()`을 통해 집계 식 내부에서 그룹의 서브셋을 참조할 수 있다.
- **DAX 식**:

    ```DAX
    GROUPBY(Sales, Customer[Country], "Qty", SUMX(CURRENTGROUP(), Sales[Qty]))
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/groupby-function-dax) · [DAX Guide](https://dax.guide/groupby/)

##### INTERSECT

- **시그니처**: `INTERSECT(<table1>, <table2>)`
- **의미**: 두 테이블의 **교집합**을 반환(왼쪽 테이블의 열 이름 사용).
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/intersect-function-dax) · [DAX Guide](https://dax.guide/intersect/)

##### NATURALINNERJOIN

- **시그니처**: `NATURALINNERJOIN(<table1>, <table2>)`
- **의미**: 공통 관계·이름으로 **내부 조인**한 표.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/naturalinnerjoin-function-dax) · [DAX Guide](https://dax.guide/naturalinnerjoin/)

##### NATURALLEFTOUTERJOIN

- **시그니처**: `NATURALLEFTOUTERJOIN(<table1>, <table2>)`
- **의미**: 공통 관계·이름으로 **좌외부 조인**한 표.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/naturalleftouterjoin-function-dax) · [DAX Guide](https://dax.guide/naturalleftouterjoin/)

##### ROW

- **시그니처**: `ROW(<name1>, <expr1>[, ...])`
- **의미**: 한 줄짜리 테이블을 만든다. 대시보드의 KPI 요약 테이블 생성에 유용.
- **DAX 식**:

    ```DAX
    EVALUATE ROW("Sales", [Total Sales], "Customers", [Customer Count])
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/row-function-dax) · [DAX Guide](https://dax.guide/row/)

##### SELECTCOLUMNS

- **시그니처**: `SELECTCOLUMNS(<table>, <name1>, <expr1>[, ...])`
- **의미**: 입력 테이블에서 원하는 열만 골라 **새 이름으로 투영**한다.
- **DAX 식**:

    ```DAX
    SELECTCOLUMNS(Customer, "Cust", Customer[Name], "Country", Customer[Country])
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/selectcolumns-function-dax) · [DAX Guide](https://dax.guide/selectcolumns/)

##### SUMMARIZE

- **시그니처**: `SUMMARIZE(<table>, <groupBy_col1>[, ...][, <name>, <expr>[, ...]])`
- **의미**: 그룹화 열로 집계한 표를 만든다. 단순 그룹화 용도로는 `SUMMARIZECOLUMNS`가 더 안전하다.
- **DAX 식**:

    ```DAX
    SUMMARIZE(Sales, Customer[Country], "Sales", SUM(Sales[Amount]))
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/summarize-function-dax) · [DAX Guide](https://dax.guide/summarize/)

##### SUMMARIZECOLUMNS

- **시그니처**: `SUMMARIZECOLUMNS(<groupBy_col1>[, ...][, <filter>][, <name>, <expr>[, ...]])`
- **의미**: `SUMMARIZE`를 단순화한 버전. 필터·그룹·측정값을 한 번에 쓸 수 있어 쿼리·계산 테이블의 **표준 집계 함수**이다.
- **DAX 식**:

    ```DAX
    SUMMARIZECOLUMNS(Customer[Country], 'Date'[Year], "Sales", [Total Sales])
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/summarizecolumns-function-dax) · [DAX Guide](https://dax.guide/summarizecolumns/)

##### TOPN

- **시그니처**: `TOPN(<n>, <table>, [<orderBy>, [<order>]...])`
- **의미**: 정렬 기준으로 상위 N개 행을 반환한다. 동률 포함.
- **DAX 식**:

    ```DAX
    TOPN(10, Customer, [Sales], DESC)
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/topn-function-dax) · [DAX Guide](https://dax.guide/topn/)

##### UNION

- **시그니처**: `UNION(<table1>, <table2>[, ...])`
- **의미**: 같은 열 구조를 가진 테이블들을 **세로로 결합**한다. 중복 유지.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/union-function-dax) · [DAX Guide](https://dax.guide/union/)

##### VALUES

- **시그니처**: `VALUES(<table_or_column>)`
- **의미**: 열의 **고유 값 테이블** 또는 테이블의 고유 행 테이블을 반환. 필터 컨텍스트를 존중한다.
- **DAX 식**:

    ```DAX
    COUNTROWS(VALUES(Customer[Country]))
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/values-function-dax) · [DAX Guide](https://dax.guide/values/)

#### 분류: 시간 인텔리전스(Time Intelligence)

##### CALENDAR

- **시그니처**: `CALENDAR(<start_date>, <end_date>)`
- **의미**: 지정 범위의 연속 날짜 테이블을 생성한다. 날짜 테이블 만들 때 기본.
- **DAX 식**:

    ```DAX
    DateTable = CALENDAR(DATE(2024,1,1), DATE(2026,12,31))
    ```

- **결과**: 1096행 Date 열
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/calendar-function-dax) · [DAX Guide](https://dax.guide/calendar/)

##### CALENDARAUTO

- **시그니처**: `CALENDARAUTO([<fiscal_year_end_month>])`
- **의미**: 모델의 모든 날짜 열 범위를 탐지해 **자동으로** 연속 날짜 테이블을 만든다.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/calendarauto-function-dax) · [DAX Guide](https://dax.guide/calendarauto/)

##### DATEADD

- **시그니처**: `DATEADD(<dates>, <number_of_intervals>, <interval>)`
- **의미**: 날짜 열을 **연/분기/월/일 단위로 이동**시킨 날짜 테이블 반환. `<interval>` = YEAR/QUARTER/MONTH/DAY.
- **DAX 식**:

    ```DAX
    [Sales LY] = CALCULATE([Sales], DATEADD('Date'[Date], -1, YEAR))
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/dateadd-function-dax) · [DAX Guide](https://dax.guide/dateadd/)

##### DATESBETWEEN

- **시그니처**: `DATESBETWEEN(<dates>, <start_date>, <end_date>)`
- **의미**: 두 날짜 사이의 날짜 집합 테이블. 누적 합계·지연 기간 계산에 쓴다.
- **DAX 식**:

    ```DAX
    [Running Sales] = CALCULATE([Sales], DATESBETWEEN('Date'[Date], BLANK(), MAX('Date'[Date])))
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/datesbetween-function-dax) · [DAX Guide](https://dax.guide/datesbetween/)

##### DATESINPERIOD

- **시그니처**: `DATESINPERIOD(<dates>, <start_date>, <number_of_intervals>, <interval>)`
- **의미**: 시작일로부터 N 단위 앞뒤 날짜를 반환.
- **DAX 식**:

    ```DAX
    [Last 3 Months] = CALCULATE([Sales], DATESINPERIOD('Date'[Date], MAX('Date'[Date]), -3, MONTH))
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/datesinperiod-function-dax) · [DAX Guide](https://dax.guide/datesinperiod/)

##### DATESYTD

- **시그니처**: `DATESYTD(<dates>[, <year_end_date>])`
- **의미**: 현재 필터 내 연초부터 오늘까지의 날짜 집합.
- **DAX 식**:

    ```DAX
    [Sales YTD] = CALCULATE([Sales], DATESYTD('Date'[Date]))
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/datesytd-function-dax) · [DAX Guide](https://dax.guide/datesytd/)

##### ENDOFMONTH

- **시그니처**: `ENDOFMONTH(<dates>)`
- **의미**: 현재 필터 내 최대 날짜가 속한 **월의 마지막 날**을 반환.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/endofmonth-function-dax) · [DAX Guide](https://dax.guide/endofmonth/)

##### PARALLELPERIOD

- **시그니처**: `PARALLELPERIOD(<dates>, <number>, <interval>)`
- **의미**: `DATEADD`와 유사하나 **전체 구간**(예: 한 달 전체)을 반환한다.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/parallelperiod-function-dax) · [DAX Guide](https://dax.guide/parallelperiod/)

##### PREVIOUSMONTH

- **시그니처**: `PREVIOUSMONTH(<dates>)`
- **의미**: 현재 필터된 달의 **바로 이전 월 전체**를 반환.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/previousmonth-function-dax) · [DAX Guide](https://dax.guide/previousmonth/)

##### SAMEPERIODLASTYEAR

- **시그니처**: `SAMEPERIODLASTYEAR(<dates>)`
- **의미**: 현재 필터된 날짜 구간을 **정확히 1년 전**으로 이동.
- **DAX 식**:

    ```DAX
    [Sales PY] = CALCULATE([Sales], SAMEPERIODLASTYEAR('Date'[Date]))
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/sameperiodlastyear-function-dax) · [DAX Guide](https://dax.guide/sameperiodlastyear/)

##### STARTOFMONTH

- **시그니처**: `STARTOFMONTH(<dates>)`
- **의미**: 현재 필터 내 최소 날짜가 속한 **월의 첫날**을 반환.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/startofmonth-function-dax) · [DAX Guide](https://dax.guide/startofmonth/)

##### TOTALYTD

- **시그니처**: `TOTALYTD(<expression>, <dates>[, <filter>][, <year_end_date>])`
- **의미**: `CALCULATE([Sales], DATESYTD(...))`의 단축형. 빠르게 YTD 측정값을 만들 때 쓴다.
- **DAX 식**:

    ```DAX
    [Sales YTD] = TOTALYTD([Sales], 'Date'[Date])
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/totalytd-function-dax) · [DAX Guide](https://dax.guide/totalytd/)

#### 분류: 날짜·시간(Date & Time)

##### DATE

- **시그니처**: `DATE(<year>, <month>, <day>)`
- **의미**: 세 숫자로부터 날짜 값을 생성.
- **DAX 식**:

    ```DAX
    DATE(2026, 4, 20)
    ```

- **결과**: 2026-04-20
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/date-function-dax) · [DAX Guide](https://dax.guide/date/)

##### DATEDIFF

- **시그니처**: `DATEDIFF(<start>, <end>, <interval>)`
- **의미**: 두 날짜 사이의 간격을 지정 단위로 측정. `<interval>` = SECOND/MINUTE/HOUR/DAY/WEEK/MONTH/QUARTER/YEAR.
- **DAX 식**:

    ```DAX
    DATEDIFF(Sales[OrderDate], Sales[ShipDate], DAY)
    ```

- **결과**: 배송 소요 일수
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/datediff-function-dax) · [DAX Guide](https://dax.guide/datediff/)

##### DAY

- **시그니처**: `DAY(<date>)`
- **의미**: 날짜에서 일(1~31) 추출.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/day-function-dax) · [DAX Guide](https://dax.guide/day/)

##### EDATE

- **시그니처**: `EDATE(<start>, <months>)`
- **의미**: 월 단위로 날짜를 이동. `EOMONTH`의 임의 날짜 버전.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/edate-function-dax) · [DAX Guide](https://dax.guide/edate/)

##### EOMONTH

- **시그니처**: `EOMONTH(<start>, <months>)`
- **의미**: 지정 월수만큼 이동한 월의 **마지막 날** 반환.
- **DAX 식**:

    ```DAX
    EOMONTH(DATE(2026,4,15), 0)
    ```

- **결과**: 2026-04-30
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/eomonth-function-dax) · [DAX Guide](https://dax.guide/eomonth/)

##### MONTH

- **시그니처**: `MONTH(<date>)`
- **의미**: 날짜에서 월(1~12) 추출.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/month-function-dax) · [DAX Guide](https://dax.guide/month/)

##### NOW

- **시그니처**: `NOW()`
- **의미**: 현재 날짜와 시각.
- **결과**: 2026-04-20 13:42:05
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/now-function-dax) · [DAX Guide](https://dax.guide/now/)

##### TODAY

- **시그니처**: `TODAY()`
- **의미**: 오늘의 날짜(시각 없음).
- **결과**: 2026-04-20
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/today-function-dax) · [DAX Guide](https://dax.guide/today/)

##### WEEKDAY

- **시그니처**: `WEEKDAY(<date>[, <return_type>])`
- **의미**: 요일을 숫자로 반환. `return_type`에 따라 기준이 다름(1: 일=1).
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/weekday-function-dax) · [DAX Guide](https://dax.guide/weekday/)

##### WEEKNUM

- **시그니처**: `WEEKNUM(<date>[, <return_type>])`
- **의미**: 해의 주 번호(1~54).
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/weeknum-function-dax) · [DAX Guide](https://dax.guide/weeknum/)

##### YEAR

- **시그니처**: `YEAR(<date>)`
- **의미**: 날짜에서 연도(숫자) 추출.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/year-function-dax) · [DAX Guide](https://dax.guide/year/)

##### YEARFRAC

- **시그니처**: `YEARFRAC(<start>, <end>[, <basis>])`
- **의미**: 두 날짜의 연 단위 소수 차이.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/yearfrac-function-dax) · [DAX Guide](https://dax.guide/yearfrac/)

#### 분류: 텍스트(Text)

##### COMBINEVALUES

- **시그니처**: `COMBINEVALUES(<delimiter>, <expr1>, <expr2>[, ...])`
- **의미**: 여러 값을 **키 구분자**로 합친다. 복합키 조인 준비 시 사용.
- **DAX 식**:

    ```DAX
    COMBINEVALUES("|", Sales[Year], Sales[Month])
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/combinevalues-function-dax) · [DAX Guide](https://dax.guide/combinevalues/)

##### CONCATENATE

- **시그니처**: `CONCATENATE(<t1>, <t2>)`
- **의미**: 두 문자열을 이어 붙인다. 연산자 `&`와 동일.
- **DAX 식**:

    ```DAX
    CONCATENATE("Hello ", "World")
    ```

- **결과**: "Hello World"
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/concatenate-function-dax) · [DAX Guide](https://dax.guide/concatenate/)

##### CONCATENATEX

- **시그니처**: `CONCATENATEX(<table>, <expression>[, <delimiter>[, <orderBy>[, <order>]]])`
- **의미**: 각 행에 식을 평가하고 구분자로 이어 붙여 하나의 문자열 반환.
- **DAX 식**:

    ```DAX
    CONCATENATEX(TOPN(3, Customer, [Sales], DESC), Customer[Name], ", ")
    ```

- **결과**: "Alice, Bob, Chan"
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/concatenatex-function-dax) · [DAX Guide](https://dax.guide/concatenatex/)

##### FIND

- **시그니처**: `FIND(<find_text>, <within>[, <start>[, <if_not_found>]])`
- **의미**: 대소문자 구분 위치 찾기(1부터). 없으면 오류 또는 대체 값.
- **DAX 식**:

    ```DAX
    FIND("BC", "ABCDE")
    ```

- **결과**: 2
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/find-function-dax) · [DAX Guide](https://dax.guide/find/)

##### FORMAT

- **시그니처**: `FORMAT(<value>, <format_string>[, <locale>])`
- **의미**: 값을 지정한 서식 문자열로 **문자열**로 변환.
- **DAX 식**:

    ```DAX
    FORMAT(TODAY(), "yyyy-MM-dd")
    ```

- **결과**: "2026-04-20"
- **주의**: 시각화 숫자 포맷과 달리 결과 타입이 문자열로 바뀌어 산술 집계에 바로 쓰기 어렵다.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/format-function-dax) · [DAX Guide](https://dax.guide/format/)

##### LEFT

- **시그니처**: `LEFT(<text>, <num>)`
- **의미**: 왼쪽에서 N자 문자열.
- **DAX 식**:

    ```DAX
    LEFT("ABCDE", 2)
    ```

- **결과**: "AB"
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/left-function-dax) · [DAX Guide](https://dax.guide/left/)

##### LEN

- **시그니처**: `LEN(<text>)`
- **의미**: 문자열 길이.
- **DAX 식**:

    ```DAX
    LEN("Seoul")
    ```

- **결과**: 5
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/len-function-dax) · [DAX Guide](https://dax.guide/len/)

##### LOWER

- **시그니처**: `LOWER(<text>)`
- **의미**: 소문자화.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/lower-function-dax) · [DAX Guide](https://dax.guide/lower/)

##### MID

- **시그니처**: `MID(<text>, <start>, <num>)`
- **의미**: 지정 위치부터 N자.
- **DAX 식**:

    ```DAX
    MID("ABCDE", 2, 3)
    ```

- **결과**: "BCD"
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/mid-function-dax) · [DAX Guide](https://dax.guide/mid/)

##### REPLACE

- **시그니처**: `REPLACE(<text>, <start>, <num>, <new_text>)`
- **의미**: 지정 위치의 N자를 새 문자열로 바꾼다.
- **DAX 식**:

    ```DAX
    REPLACE("ABCDE", 2, 2, "XX")
    ```

- **결과**: "AXXDE"
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/replace-function-dax) · [DAX Guide](https://dax.guide/replace/)

##### RIGHT

- **시그니처**: `RIGHT(<text>, <num>)`
- **의미**: 오른쪽에서 N자.
- **DAX 식**:

    ```DAX
    RIGHT("ABCDE", 2)
    ```

- **결과**: "DE"
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/right-function-dax) · [DAX Guide](https://dax.guide/right/)

##### SEARCH

- **시그니처**: `SEARCH(<find>, <within>[, <start>[, <if_not_found>]])`
- **의미**: 대소문자 **구분 없이** 찾기. 와일드카드 `?`, `*` 허용.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/search-function-dax) · [DAX Guide](https://dax.guide/search/)

##### SUBSTITUTE

- **시그니처**: `SUBSTITUTE(<text>, <old>, <new>[, <instance>])`
- **의미**: 문자열에서 지정 패턴을 치환. N번째 발생만 바꿀 수 있음.
- **DAX 식**:

    ```DAX
    SUBSTITUTE("A-B-C", "-", "/")
    ```

- **결과**: "A/B/C"
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/substitute-function-dax) · [DAX Guide](https://dax.guide/substitute/)

##### TRIM

- **시그니처**: `TRIM(<text>)`
- **의미**: 앞뒤 공백과 중간 중복 공백을 **단일 공백**으로 정리.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/trim-function-dax) · [DAX Guide](https://dax.guide/trim/)

##### UPPER

- **시그니처**: `UPPER(<text>)`
- **의미**: 대문자화.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/upper-function-dax) · [DAX Guide](https://dax.guide/upper/)

##### VALUE

- **시그니처**: `VALUE(<text>)`
- **의미**: 문자열을 숫자로 변환. 로케일 문제를 주의.
- **DAX 식**:

    ```DAX
    VALUE("1,234.5")
    ```

- **결과**: 1234.5(로케일에 따라 다를 수 있음)
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/value-function-dax) · [DAX Guide](https://dax.guide/value/)

#### 분류: 수학·삼각(Math & Trig)

##### ABS

- **시그니처**: `ABS(<number>)`
- **의미**: 절댓값.
- **DAX 식**:

    ```DAX
    ABS(-3)
    ```

- **결과**: 3
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/abs-function-dax) · [DAX Guide](https://dax.guide/abs/)

##### CEILING

- **시그니처**: `CEILING(<number>, <significance>)`
- **의미**: 지정 배수로 올림.
- **DAX 식**:

    ```DAX
    CEILING(7, 5)
    ```

- **결과**: 10
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/ceiling-function-dax) · [DAX Guide](https://dax.guide/ceiling/)

##### DIVIDE

- **시그니처**: `DIVIDE(<numerator>, <denominator>[, <alternate>])`
- **의미**: 안전 나눗셈. 분모가 0/BLANK면 대체값(기본 BLANK). `/`연산자보다 먼저 고려.
- **DAX 식**:

    ```DAX
    DIVIDE([Profit], [Sales], 0)
    ```

- **결과**: 매출이 0이면 0, 아니면 이익률
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/divide-function-dax) · [DAX Guide](https://dax.guide/divide/)

##### EXP

- **시그니처**: `EXP(<number>)`
- **의미**: `e`의 거듭제곱.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/exp-function-dax) · [DAX Guide](https://dax.guide/exp/)

##### FLOOR

- **시그니처**: `FLOOR(<number>, <significance>)`
- **의미**: 지정 배수로 내림.
- **DAX 식**:

    ```DAX
    FLOOR(7, 5)
    ```

- **결과**: 5
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/floor-function-dax) · [DAX Guide](https://dax.guide/floor/)

##### INT

- **시그니처**: `INT(<number>)`
- **의미**: 가장 가까운 **작은 정수**로 내림.
- **DAX 식**:

    ```DAX
    INT(-3.2)
    ```

- **결과**: -4
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/int-function-dax) · [DAX Guide](https://dax.guide/int/)

##### LN

- **시그니처**: `LN(<number>)`
- **의미**: 자연로그.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/ln-function-dax) · [DAX Guide](https://dax.guide/ln/)

##### LOG

- **시그니처**: `LOG(<number>[, <base>])`
- **의미**: 지정 밑의 로그(기본 10).
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/log-function-dax) · [DAX Guide](https://dax.guide/log/)

##### LOG10

- **시그니처**: `LOG10(<number>)`
- **의미**: 상용로그.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/log10-function-dax) · [DAX Guide](https://dax.guide/log10/)

##### MOD

- **시그니처**: `MOD(<number>, <divisor>)`
- **의미**: 나머지.
- **DAX 식**:

    ```DAX
    MOD(10, 3)
    ```

- **결과**: 1
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/mod-function-dax) · [DAX Guide](https://dax.guide/mod/)

##### POWER

- **시그니처**: `POWER(<number>, <power>)`
- **의미**: 거듭제곱.
- **DAX 식**:

    ```DAX
    POWER(2, 10)
    ```

- **결과**: 1024
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/power-function-dax) · [DAX Guide](https://dax.guide/power/)

##### RAND

- **시그니처**: `RAND()`
- **의미**: 0 이상 1 미만 난수.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/rand-function-dax) · [DAX Guide](https://dax.guide/rand/)

##### RANDBETWEEN

- **시그니처**: `RANDBETWEEN(<min>, <max>)`
- **의미**: 정수 난수.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/randbetween-function-dax) · [DAX Guide](https://dax.guide/randbetween/)

##### ROUND

- **시그니처**: `ROUND(<number>, <num_digits>)`
- **의미**: 반올림.
- **DAX 식**:

    ```DAX
    ROUND(123.456, 1)
    ```

- **결과**: 123.5
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/round-function-dax) · [DAX Guide](https://dax.guide/round/)

##### ROUNDDOWN

- **시그니처**: `ROUNDDOWN(<number>, <digits>)`
- **의미**: 0 쪽으로 내림.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/rounddown-function-dax) · [DAX Guide](https://dax.guide/rounddown/)

##### ROUNDUP

- **시그니처**: `ROUNDUP(<number>, <digits>)`
- **의미**: 0에서 먼 쪽으로 올림.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/roundup-function-dax) · [DAX Guide](https://dax.guide/roundup/)

##### SQRT

- **시그니처**: `SQRT(<number>)`
- **의미**: 양의 제곱근.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/sqrt-function-dax) · [DAX Guide](https://dax.guide/sqrt/)

#### 분류: 통계(Statistical)

##### GEOMEAN

- **시그니처**: `GEOMEAN(<column>)`
- **의미**: 기하 평균. 수익률 계열에 사용.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/geomean-function-dax) · [DAX Guide](https://dax.guide/geomean/)

##### MEDIAN

- **시그니처**: `MEDIAN(<column>)`
- **의미**: 중앙값.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/median-function-dax) · [DAX Guide](https://dax.guide/median/)

##### PERCENTILE.EXC

- **시그니처**: `PERCENTILE.EXC(<column>, <k>)`
- **의미**: k 분위수(배타식).
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/percentile-exc-function-dax) · [DAX Guide](https://dax.guide/percentile-exc/)

##### PERCENTILE.INC

- **시그니처**: `PERCENTILE.INC(<column>, <k>)`
- **의미**: 열의 **k 분위수**(0~1 포함식).
- **DAX 식**:

    ```DAX
    PERCENTILE.INC(Sales[Amount], 0.9)
    ```

- **결과**: 상위 10% 컷오프
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/percentile-inc-function-dax) · [DAX Guide](https://dax.guide/percentile-inc/)

##### RANK.EQ

- **시그니처**: `RANK.EQ(<value>, <ref>[, <order>])`
- **의미**: 값이 참조 열에서 차지하는 순위(동률 같은 순위).
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/rank-eq-function-dax) · [DAX Guide](https://dax.guide/rank-eq/)

##### RANKX

- **시그니처**: `RANKX(<table>, <expression>[, <value>[, <order>[, <ties>]]])`
- **의미**: 테이블을 식으로 정렬하고 현재 컨텍스트의 값 **순위**를 돌려준다.
- **DAX 식**:

    ```DAX
    [Sales Rank] = RANKX(ALL(Customer), [Sales], , DESC, DENSE)
    ```

- **주의**: ALL로 기준 테이블을 펼쳐야 전체 순위가 나온다.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/rankx-function-dax) · [DAX Guide](https://dax.guide/rankx/)

##### STDEV.P

- **시그니처**: `STDEV.P(<column>)`
- **의미**: 모집단 표준편차.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/stdev-p-function-dax) · [DAX Guide](https://dax.guide/stdev-p/)

##### STDEV.S

- **시그니처**: `STDEV.S(<column>)`
- **의미**: 표본 표준편차.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/stdev-s-function-dax) · [DAX Guide](https://dax.guide/stdev-s/)

##### VAR.P

- **시그니처**: `VAR.P(<column>)`
- **의미**: 모집단 분산.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/var-p-function-dax) · [DAX Guide](https://dax.guide/var-p/)

##### VAR.S

- **시그니처**: `VAR.S(<column>)`
- **의미**: 표본 분산.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/var-s-function-dax) · [DAX Guide](https://dax.guide/var-s/)

#### 분류: 정보(Information)

##### BLANK

- **시그니처**: `BLANK()`
- **의미**: NULL 상수. 집계 시 무시됨.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/blank-function-dax) · [DAX Guide](https://dax.guide/blank/)

##### COLUMNSTATISTICS

- **시그니처**: `COLUMNSTATISTICS()`
- **의미**: 엔진이 기록한 열 통계 테이블을 반환(엔지니어링 진단용).
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/columnstatistics-function-dax) · [DAX Guide](https://dax.guide/columnstatistics/)

##### CUSTOMDATA

- **시그니처**: `CUSTOMDATA()`
- **의미**: 연결 문자열에 담긴 사용자 지정 식별자. 임베드 시나리오에서 사용.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/customdata-function-dax) · [DAX Guide](https://dax.guide/customdata/)

##### ISBLANK

- **시그니처**: `ISBLANK(<value>)`
- **의미**: 값이 BLANK이면 TRUE. BLANK는 DAX의 NULL에 해당.
- **DAX 식**:

    ```DAX
    IF(ISBLANK([Sales]), 0, [Sales])
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/isblank-function-dax) · [DAX Guide](https://dax.guide/isblank/)

##### ISERROR

- **시그니처**: `ISERROR(<expr>)`
- **의미**: 식이 오류를 내는지 검사.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/iserror-function-dax) · [DAX Guide](https://dax.guide/iserror/)

##### ISINSCOPE

- **시그니처**: `ISINSCOPE(<column>)`
- **의미**: 현재 시각적 개체에서 그 **열이 그룹화 키**로 쓰이는 수준에 있는지 검사. 매트릭스의 소계 여부 판정에 쓴다.
- **DAX 식**:

    ```DAX
    IF(ISINSCOPE('Date'[Month]), "Month total", "Higher total")
    ```

- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/isinscope-function-dax) · [DAX Guide](https://dax.guide/isinscope/)

##### ISNUMBER

- **시그니처**: `ISNUMBER(<value>)`
- **의미**: 숫자형 값인지 검사.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/isnumber-function-dax) · [DAX Guide](https://dax.guide/isnumber/)

##### ISSUBTOTAL

- **시그니처**: `ISSUBTOTAL(<column>)`
- **의미**: `SUMMARIZE` 결과 행이 소계 행인지 표시. `ROLLUP*`과 함께 쓴다.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/issubtotal-function-dax) · [DAX Guide](https://dax.guide/issubtotal/)

##### ISTEXT

- **시그니처**: `ISTEXT(<value>)`
- **의미**: 텍스트형 값인지 검사.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/istext-function-dax) · [DAX Guide](https://dax.guide/istext/)

##### SELECTEDMEASURE

- **시그니처**: `SELECTEDMEASURE()`
- **의미**: <strong>계산 그룹</strong>에서 현재 적용되는 측정값을 나타낸다. 계산 항목의 식 안에서만 의미가 있다.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/selectedmeasure-function-dax) · [DAX Guide](https://dax.guide/selectedmeasure/)

##### SELECTEDMEASURENAME

- **시그니처**: `SELECTEDMEASURENAME()`
- **의미**: 현재 선택된 측정값의 이름(문자열).
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/selectedmeasurename-function-dax) · [DAX Guide](https://dax.guide/selectedmeasurename/)

##### USERNAME

- **시그니처**: `USERNAME()`
- **의미**: 현재 보고서 사용자 ID(`domain\user` 또는 UPN). RLS에 필수.
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/username-function-dax) · [DAX Guide](https://dax.guide/username/)

##### USERPRINCIPALNAME

- **시그니처**: `USERPRINCIPALNAME()`
- **의미**: 현재 사용자의 UPN(이메일 형식).
- **참고**: [Microsoft Learn](https://learn.microsoft.com/en-us/dax/userprincipalname-function-dax) · [DAX Guide](https://dax.guide/userprincipalname/)

### D.2 카테고리별 전 함수 색인

dax.guide 사이트맵에서 확인한 DAX 함수 전수를 카테고리별로 나눠 한 줄 설명과 공식 문서 링크로 정리한다. 심층 예제가 있는 함수는 표제 옆에 **(D.1 예제 있음)**이라고 덧붙인다.

#### 집계(Aggregation) (22개)

- **APPROXIMATEDISTINCTCOUNT** — APPROXIMATEDISTINCTCOUNT 집계 함수. 숫자 열/식을 대상으로 값을 계산한다. [Learn](https://learn.microsoft.com/en-us/dax/approximatedistinctcount-function-dax) · [DAX Guide](https://dax.guide/approximatedistinctcount/)
- **AVERAGE** **(D.1 예제 있음)** — 숫자 열의 산술 평균을 계산한다. [Learn](https://learn.microsoft.com/en-us/dax/average-function-dax) · [DAX Guide](https://dax.guide/average/)
- **AVERAGEA** — AVERAGEA 집계 함수. 숫자 열/식을 대상으로 값을 계산한다. [Learn](https://learn.microsoft.com/en-us/dax/averagea-function-dax) · [DAX Guide](https://dax.guide/averagea/)
- **AVERAGEX** **(D.1 예제 있음)** — 테이블의 각 행에 식을 평가해 평균을 낸다. 식 내부에서 행 간 곱셈·비교가 필요한 경우에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/averagex-function-dax) · [DAX Guide](https://dax.guide/averagex/)
- **COUNT** **(D.1 예제 있음)** — 숫자·날짜·논리 열에서 **비어 있지 않은 값의 개수**를 센다. [Learn](https://learn.microsoft.com/en-us/dax/count-function-dax) · [DAX Guide](https://dax.guide/count/)
- **COUNTA** **(D.1 예제 있음)** — 빈 값을 제외한 **모든 형식**의 값 개수를 센다. 텍스트 열에 유용. [Learn](https://learn.microsoft.com/en-us/dax/counta-function-dax) · [DAX Guide](https://dax.guide/counta/)
- **COUNTAX** — COUNTAX 집계 함수. 숫자 열/식을 대상으로 값을 계산한다. [Learn](https://learn.microsoft.com/en-us/dax/countax-function-dax) · [DAX Guide](https://dax.guide/countax/)
- **COUNTBLANK** **(D.1 예제 있음)** — 열에서 BLANK(공란)의 개수를 센다. 데이터 품질 측정에 유용. [Learn](https://learn.microsoft.com/en-us/dax/countblank-function-dax) · [DAX Guide](https://dax.guide/countblank/)
- **COUNTROWS** **(D.1 예제 있음)** — 테이블(또는 식의 결과 테이블) 행 수를 센다. 집계 중 가장 명확·빠른 함수. [Learn](https://learn.microsoft.com/en-us/dax/countrows-function-dax) · [DAX Guide](https://dax.guide/countrows/)
- **COUNTX** **(D.1 예제 있음)** — 식이 비어 있지 않은 행의 수를 센다. 필터 조건을 카운트로 표현할 때 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/countx-function-dax) · [DAX Guide](https://dax.guide/countx/)
- **DISTINCTCOUNT** **(D.1 예제 있음)** — 열의 **고유 값 수**(BLANK 포함). [Learn](https://learn.microsoft.com/en-us/dax/distinctcount-function-dax) · [DAX Guide](https://dax.guide/distinctcount/)
- **DISTINCTCOUNTNOBLANK** **(D.1 예제 있음)** — 열의 고유 값 수에서 BLANK를 제외한다. [Learn](https://learn.microsoft.com/en-us/dax/distinctcountnoblank-function-dax) · [DAX Guide](https://dax.guide/distinctcountnoblank/)
- **MAX** **(D.1 예제 있음)** — 숫자·날짜 열의 최댓값을 반환한다. [Learn](https://learn.microsoft.com/en-us/dax/max-function-dax) · [DAX Guide](https://dax.guide/max/)
- **MAXA** — MAXA 집계 함수. 숫자 열/식을 대상으로 값을 계산한다. [Learn](https://learn.microsoft.com/en-us/dax/maxa-function-dax) · [DAX Guide](https://dax.guide/maxa/)
- **MAXX** **(D.1 예제 있음)** — 각 행에서 평가한 식의 최댓값을 돌려주는 행 반복 함수. [Learn](https://learn.microsoft.com/en-us/dax/maxx-function-dax) · [DAX Guide](https://dax.guide/maxx/)
- **MIN** **(D.1 예제 있음)** — 숫자·날짜 열의 최솟값을 반환한다. [Learn](https://learn.microsoft.com/en-us/dax/min-function-dax) · [DAX Guide](https://dax.guide/min/)
- **MINA** — MINA 집계 함수. 숫자 열/식을 대상으로 값을 계산한다. [Learn](https://learn.microsoft.com/en-us/dax/mina-function-dax) · [DAX Guide](https://dax.guide/mina/)
- **MINX** **(D.1 예제 있음)** — 각 행에서 평가한 식의 최솟값을 돌려주는 행 반복 함수. [Learn](https://learn.microsoft.com/en-us/dax/minx-function-dax) · [DAX Guide](https://dax.guide/minx/)
- **PRODUCT** — PRODUCT 집계 함수. 숫자 열/식을 대상으로 값을 계산한다. [Learn](https://learn.microsoft.com/en-us/dax/product-function-dax) · [DAX Guide](https://dax.guide/product/)
- **PRODUCTX** **(D.1 예제 있음)** — 각 행에서 평가한 식의 **곱**을 반환한다(복합 성장률 등에 사용). [Learn](https://learn.microsoft.com/en-us/dax/productx-function-dax) · [DAX Guide](https://dax.guide/productx/)
- **SUM** **(D.1 예제 있음)** — 한 숫자 열의 모든 값을 단순 합계한다. 내부적으로 `SUMX(VALUES(...), ...)`에 가깝게 동작하며 필터 컨텍스트를 존중한다. [Learn](https://learn.microsoft.com/en-us/dax/sum-function-dax) · [DAX Guide](https://dax.guide/sum/)
- **SUMX** **(D.1 예제 있음)** — 테이블의 각 행에 식을 평가한 뒤 결과를 합산하는 행 반복 함수(iterator). 각 행이 **행 컨텍스트**를 만든다. [Learn](https://learn.microsoft.com/en-us/dax/sumx-function-dax) · [DAX Guide](https://dax.guide/sumx/)

#### 논리(Logical) (10개)

- **AND** **(D.1 예제 있음)** — 두 식이 모두 TRUE면 TRUE. 연산자 `&&`와 동일하며 두 개 이상에는 `&&`가 가독성이 좋다. [Learn](https://learn.microsoft.com/en-us/dax/and-function-dax) · [DAX Guide](https://dax.guide/and/)
- **COALESCE** **(D.1 예제 있음)** — 첫 번째 **비-BLANK** 값을 반환한다. `IF(ISBLANK(x), y, x)`의 간결한 대안. [Learn](https://learn.microsoft.com/en-us/dax/coalesce-function-dax) · [DAX Guide](https://dax.guide/coalesce/)
- **FALSE** **(D.1 예제 있음)** — 상수 FALSE. [Learn](https://learn.microsoft.com/en-us/dax/false-function-dax) · [DAX Guide](https://dax.guide/false/)
- **IF** **(D.1 예제 있음)** — 조건이 참이면 첫 값을, 아니면 둘째 값을 반환. 셋째 인수 생략 시 BLANK. [Learn](https://learn.microsoft.com/en-us/dax/if-function-dax) · [DAX Guide](https://dax.guide/if/)
- **IF.EAGER** — IF.EAGER 논리 연산자/함수. TRUE·FALSE·BLANK 중 하나를 돌려준다. [Learn](https://learn.microsoft.com/en-us/dax/if-eager-function-dax) · [DAX Guide](https://dax.guide/if-eager/)
- **IFERROR** **(D.1 예제 있음)** — 첫 식이 오류를 발생시키면 두 번째 식을 대신 반환한다. [Learn](https://learn.microsoft.com/en-us/dax/iferror-function-dax) · [DAX Guide](https://dax.guide/iferror/)
- **NOT** **(D.1 예제 있음)** — 논리값을 뒤집는다. [Learn](https://learn.microsoft.com/en-us/dax/not-function-dax) · [DAX Guide](https://dax.guide/not/)
- **OR** **(D.1 예제 있음)** — 둘 중 하나만 TRUE면 TRUE. 연산자 `||`와 동일. [Learn](https://learn.microsoft.com/en-us/dax/or-function-dax) · [DAX Guide](https://dax.guide/or/)
- **SWITCH** **(D.1 예제 있음)** — 식 결과와 값 목록을 차례로 비교해 일치하는 결과를 돌려준다. `SWITCH(TRUE(), ...)` 패턴으로 다중 조건 분기에도 사용. [Learn](https://learn.microsoft.com/en-us/dax/switch-function-dax) · [DAX Guide](https://dax.guide/switch/)
- **TRUE** **(D.1 예제 있음)** — 상수 TRUE. `SWITCH(TRUE(), ...)` 패턴에 자주 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/true-function-dax) · [DAX Guide](https://dax.guide/true/)

#### 필터(Filter) (37개)

- **ALL** **(D.1 예제 있음)** — 지정한 테이블 또는 열의 **필터를 제거**한 테이블을 돌려준다. `CALCULATE`의 필터 인수로 넣어 컨텍스트를 무시한다. [Learn](https://learn.microsoft.com/en-us/dax/all-function-dax) · [DAX Guide](https://dax.guide/all/)
- **ALLCROSSFILTERED** — ALLCROSSFILTERED 필터 함수. `CALCULATE` 등과 조합해 현재 컨텍스트를 수정하거나 조회한다. [Learn](https://learn.microsoft.com/en-us/dax/allcrossfiltered-function-dax) · [DAX Guide](https://dax.guide/allcrossfiltered/)
- **ALLEXCEPT** **(D.1 예제 있음)** — 지정한 열 **외에는** 전부 필터 제거. 상위 총계 비율 계산 시 표준 패턴. [Learn](https://learn.microsoft.com/en-us/dax/allexcept-function-dax) · [DAX Guide](https://dax.guide/allexcept/)
- **ALLNOBLANKROW** — ALLNOBLANKROW 필터 함수. `CALCULATE` 등과 조합해 현재 컨텍스트를 수정하거나 조회한다. [Learn](https://learn.microsoft.com/en-us/dax/allnoblankrow-function-dax) · [DAX Guide](https://dax.guide/allnoblankrow/)
- **ALLSELECTED** **(D.1 예제 있음)** — **시각적 개체 외부 필터**(슬라이서·페이지 필터)는 유지하고, **내부 좌표 축 필터**만 제거한다. “보이는 데이터 대비 비율”을 구할 때 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/allselected-function-dax) · [DAX Guide](https://dax.guide/allselected/)
- **ALLSELECTEDAPPLY** — ALLSELECTEDAPPLY 필터 함수. `CALCULATE` 등과 조합해 현재 컨텍스트를 수정하거나 조회한다. [Learn](https://learn.microsoft.com/en-us/dax/allselectedapply-function-dax) · [DAX Guide](https://dax.guide/allselectedapply/)
- **ALLSELECTEDREMOVE** — ALLSELECTEDREMOVE 필터 함수. `CALCULATE` 등과 조합해 현재 컨텍스트를 수정하거나 조회한다. [Learn](https://learn.microsoft.com/en-us/dax/allselectedremove-function-dax) · [DAX Guide](https://dax.guide/allselectedremove/)
- **ALWAYSAPPLY** — ALWAYSAPPLY 필터 함수. `CALCULATE` 등과 조합해 현재 컨텍스트를 수정하거나 조회한다. [Learn](https://learn.microsoft.com/en-us/dax/alwaysapply-function-dax) · [DAX Guide](https://dax.guide/alwaysapply/)
- **CALCULATE** **(D.1 예제 있음)** — 식을 **변경된 필터 컨텍스트**에서 평가한다. DAX에서 가장 중요한 함수이며, 행 컨텍스트를 필터 컨텍스트로 **컨텍스트 전환**하는 역할도 한다. [Learn](https://learn.microsoft.com/en-us/dax/calculate-function-dax) · [DAX Guide](https://dax.guide/calculate/)
- **CALCULATETABLE** **(D.1 예제 있음)** — `CALCULATE`의 테이블 반환 버전. 변경된 컨텍스트에서 테이블을 돌려준다. [Learn](https://learn.microsoft.com/en-us/dax/calculatetable-function-dax) · [DAX Guide](https://dax.guide/calculatetable/)
- **CROSSFILTER** **(D.1 예제 있음)** — 특정 계산에서만 관계의 교차 필터 방향을 바꾼다. `None`/`OneWay`/`Both`. [Learn](https://learn.microsoft.com/en-us/dax/crossfilter-function-dax) · [DAX Guide](https://dax.guide/crossfilter/)
- **FILTER** **(D.1 예제 있음)** — 테이블에서 조건을 만족하는 **행만** 남긴다. `CALCULATE`의 부울식 필터보다 복잡한 조건을 쓸 때 사용. [Learn](https://learn.microsoft.com/en-us/dax/filter-function-dax) · [DAX Guide](https://dax.guide/filter/)
- **FILTERCLUSTER** — FILTERCLUSTER 필터 함수. `CALCULATE` 등과 조합해 현재 컨텍스트를 수정하거나 조회한다. [Learn](https://learn.microsoft.com/en-us/dax/filtercluster-function-dax) · [DAX Guide](https://dax.guide/filtercluster/)
- **FILTERS** — FILTERS 필터 함수. `CALCULATE` 등과 조합해 현재 컨텍스트를 수정하거나 조회한다. [Learn](https://learn.microsoft.com/en-us/dax/filters-function-dax) · [DAX Guide](https://dax.guide/filters/)
- **HASONEFILTER** **(D.1 예제 있음)** — 열에 **필터 자체가 1개**인지 확인한다(값이 1개와는 미묘하게 다르다). [Learn](https://learn.microsoft.com/en-us/dax/hasonefilter-function-dax) · [DAX Guide](https://dax.guide/hasonefilter/)
- **HASONEVALUE** **(D.1 예제 있음)** — 열이 정확히 1개 값으로 필터되어 있으면 TRUE. [Learn](https://learn.microsoft.com/en-us/dax/hasonevalue-function-dax) · [DAX Guide](https://dax.guide/hasonevalue/)
- **IGNORE** — IGNORE 필터 함수. `CALCULATE` 등과 조합해 현재 컨텍스트를 수정하거나 조회한다. [Learn](https://learn.microsoft.com/en-us/dax/ignore-function-dax) · [DAX Guide](https://dax.guide/ignore/)
- **INDEX** — INDEX 필터 함수. `CALCULATE` 등과 조합해 현재 컨텍스트를 수정하거나 조회한다. [Learn](https://learn.microsoft.com/en-us/dax/index-function-dax) · [DAX Guide](https://dax.guide/index/)
- **ISCROSSFILTERED** **(D.1 예제 있음)** — 다른 테이블의 관계 경로로 **교차 필터**되어 있는지 검사. [Learn](https://learn.microsoft.com/en-us/dax/iscrossfiltered-function-dax) · [DAX Guide](https://dax.guide/iscrossfiltered/)
- **ISFILTERED** **(D.1 예제 있음)** — 직접 필터가 걸려 있는지 검사. [Learn](https://learn.microsoft.com/en-us/dax/isfiltered-function-dax) · [DAX Guide](https://dax.guide/isfiltered/)
- **KEEPFILTERS** **(D.1 예제 있음)** — `CALCULATE`의 필터 인수를 감싸, 같은 열의 기존 필터를 **대체하지 않고 교집합**으로 적용한다. [Learn](https://learn.microsoft.com/en-us/dax/keepfilters-function-dax) · [DAX Guide](https://dax.guide/keepfilters/)
- **LOOKUPVALUE** **(D.1 예제 있음)** — 조건을 만족하는 **단일 행**의 값을 돌려준다. 관계가 없을 때도 동작. [Learn](https://learn.microsoft.com/en-us/dax/lookupvalue-function-dax) · [DAX Guide](https://dax.guide/lookupvalue/)
- **LOOKUPWITHTOTALS** — LOOKUPWITHTOTALS 필터 함수. `CALCULATE` 등과 조합해 현재 컨텍스트를 수정하거나 조회한다. [Learn](https://learn.microsoft.com/en-us/dax/lookupwithtotals-function-dax) · [DAX Guide](https://dax.guide/lookupwithtotals/)
- **MATCHBY** — MATCHBY 필터 함수. `CALCULATE` 등과 조합해 현재 컨텍스트를 수정하거나 조회한다. [Learn](https://learn.microsoft.com/en-us/dax/matchby-function-dax) · [DAX Guide](https://dax.guide/matchby/)
- **NONFILTER** — NONFILTER 필터 함수. `CALCULATE` 등과 조합해 현재 컨텍스트를 수정하거나 조회한다. [Learn](https://learn.microsoft.com/en-us/dax/nonfilter-function-dax) · [DAX Guide](https://dax.guide/nonfilter/)
- **NONVISUAL** — NONVISUAL 필터 함수. `CALCULATE` 등과 조합해 현재 컨텍스트를 수정하거나 조회한다. [Learn](https://learn.microsoft.com/en-us/dax/nonvisual-function-dax) · [DAX Guide](https://dax.guide/nonvisual/)
- **OFFSET** — OFFSET 필터 함수. `CALCULATE` 등과 조합해 현재 컨텍스트를 수정하거나 조회한다. [Learn](https://learn.microsoft.com/en-us/dax/offset-function-dax) · [DAX Guide](https://dax.guide/offset/)
- **ORDERBY** — ORDERBY 필터 함수. `CALCULATE` 등과 조합해 현재 컨텍스트를 수정하거나 조회한다. [Learn](https://learn.microsoft.com/en-us/dax/orderby-function-dax) · [DAX Guide](https://dax.guide/orderby/)
- **PARTITIONBY** — PARTITIONBY 필터 함수. `CALCULATE` 등과 조합해 현재 컨텍스트를 수정하거나 조회한다. [Learn](https://learn.microsoft.com/en-us/dax/partitionby-function-dax) · [DAX Guide](https://dax.guide/partitionby/)
- **RANK** — RANK 필터 함수. `CALCULATE` 등과 조합해 현재 컨텍스트를 수정하거나 조회한다. [Learn](https://learn.microsoft.com/en-us/dax/rank-function-dax) · [DAX Guide](https://dax.guide/rank/)
- **REMOVEFILTERS** **(D.1 예제 있음)** — `CALCULATE`의 **수식 한정 필터 인수**로 설계된 `ALL`의 명시적 대안. 필터만 제거하고 테이블을 반환하지 않는다. [Learn](https://learn.microsoft.com/en-us/dax/removefilters-function-dax) · [DAX Guide](https://dax.guide/removefilters/)
- **ROWNUMBER** — ROWNUMBER 필터 함수. `CALCULATE` 등과 조합해 현재 컨텍스트를 수정하거나 조회한다. [Learn](https://learn.microsoft.com/en-us/dax/rownumber-function-dax) · [DAX Guide](https://dax.guide/rownumber/)
- **SELECTEDVALUE** **(D.1 예제 있음)** — 현재 필터 컨텍스트에서 열에 **정확히 하나**의 값만 있으면 그 값, 아니면 대체 값(기본 BLANK)을 돌려준다. [Learn](https://learn.microsoft.com/en-us/dax/selectedvalue-function-dax) · [DAX Guide](https://dax.guide/selectedvalue/)
- **SHADOWCLUSTER** — SHADOWCLUSTER 필터 함수. `CALCULATE` 등과 조합해 현재 컨텍스트를 수정하거나 조회한다. [Learn](https://learn.microsoft.com/en-us/dax/shadowcluster-function-dax) · [DAX Guide](https://dax.guide/shadowcluster/)
- **TREATAS** **(D.1 예제 있음)** — **관계가 없는** 테이블 간에도 열 값을 필터로 **가상 연결**한다. [Learn](https://learn.microsoft.com/en-us/dax/treatas-function-dax) · [DAX Guide](https://dax.guide/treatas/)
- **USERELATIONSHIP** **(D.1 예제 있음)** — `CALCULATE`의 수식 한정 인수. **비활성 관계**를 이번 평가에만 활성화한다. [Learn](https://learn.microsoft.com/en-us/dax/userelationship-function-dax) · [DAX Guide](https://dax.guide/userelationship/)
- **WINDOW** — WINDOW 필터 함수. `CALCULATE` 등과 조합해 현재 컨텍스트를 수정하거나 조회한다. [Learn](https://learn.microsoft.com/en-us/dax/window-function-dax) · [DAX Guide](https://dax.guide/window/)

#### 관계(Relationships) (2개)

- **RELATED** **(D.1 예제 있음)** — 현재 **행 컨텍스트**에서 관계의 ‘1’ 쪽 테이블의 열 값을 가져온다. 계산 열과 이터레이터 안에서 사용. [Learn](https://learn.microsoft.com/en-us/dax/related-function-dax) · [DAX Guide](https://dax.guide/related/)
- **RELATEDTABLE** **(D.1 예제 있음)** — 현재 행에 연결된 **다대일의 다(多)쪽** 테이블 서브셋을 반환한다. [Learn](https://learn.microsoft.com/en-us/dax/relatedtable-function-dax) · [DAX Guide](https://dax.guide/relatedtable/)

#### 테이블(Table) (46개)

- **ADDCOLUMNS** **(D.1 예제 있음)** — 테이블에 계산 열을 추가한 **새 테이블**을 반환한다. 시각화에 직접 보이는 계산 테이블 생성에 사용. [Learn](https://learn.microsoft.com/en-us/dax/addcolumns-function-dax) · [DAX Guide](https://dax.guide/addcolumns/)
- **ADDMISSINGITEMS** — ADDMISSINGITEMS 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/addmissingitems-function-dax) · [DAX Guide](https://dax.guide/addmissingitems/)
- **COLLAPSE** — COLLAPSE 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/collapse-function-dax) · [DAX Guide](https://dax.guide/collapse/)
- **COLLAPSEALL** — COLLAPSEALL 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/collapseall-function-dax) · [DAX Guide](https://dax.guide/collapseall/)
- **CROSSJOIN** **(D.1 예제 있음)** — 모든 행의 카르테시안 곱. [Learn](https://learn.microsoft.com/en-us/dax/crossjoin-function-dax) · [DAX Guide](https://dax.guide/crossjoin/)
- **CURRENTGROUP** — CURRENTGROUP 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/currentgroup-function-dax) · [DAX Guide](https://dax.guide/currentgroup/)
- **DATATABLE** **(D.1 예제 있음)** — DAX 내부에서 **정적 데이터 테이블**을 정의한다. 룩업 상수 테이블에 쓰인다. [Learn](https://learn.microsoft.com/en-us/dax/datatable-function-dax) · [DAX Guide](https://dax.guide/datatable/)
- **DETAILROWS** — DETAILROWS 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/detailrows-function-dax) · [DAX Guide](https://dax.guide/detailrows/)
- **DISTINCT** **(D.1 예제 있음)** — BLANK를 포함해 **중복을 제거**한 테이블/열 값을 반환. `VALUES`와 달리 모델에 의해 자동 추가되는 빈 행(관계 위반)을 포함하지 않는다. [Learn](https://learn.microsoft.com/en-us/dax/distinct-function-dax) · [DAX Guide](https://dax.guide/distinct/)
- **EARLIER** — EARLIER 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/earlier-function-dax) · [DAX Guide](https://dax.guide/earlier/)
- **EARLIEST** — EARLIEST 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/earliest-function-dax) · [DAX Guide](https://dax.guide/earliest/)
- **EXCEPT** **(D.1 예제 있음)** — `<table1>`에서 `<table2>`의 행을 뺀 차집합. [Learn](https://learn.microsoft.com/en-us/dax/except-function-dax) · [DAX Guide](https://dax.guide/except/)
- **EXPAND** — EXPAND 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/expand-function-dax) · [DAX Guide](https://dax.guide/expand/)
- **EXPANDALL** — EXPANDALL 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/expandall-function-dax) · [DAX Guide](https://dax.guide/expandall/)
- **EXTERNALMEASURE** — EXTERNALMEASURE 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/externalmeasure-function-dax) · [DAX Guide](https://dax.guide/externalmeasure/)
- **FIRST** — FIRST 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/first-function-dax) · [DAX Guide](https://dax.guide/first/)
- **GENERATE** **(D.1 예제 있음)** — 왼쪽 테이블의 각 행마다 오른쪽 식을 평가해 **조인** 하듯 결합. 오른쪽이 빈 테이블이면 행이 제외된다. [Learn](https://learn.microsoft.com/en-us/dax/generate-function-dax) · [DAX Guide](https://dax.guide/generate/)
- **GENERATEALL** **(D.1 예제 있음)** — `GENERATE`와 유사하나 오른쪽이 비어도 왼쪽 행은 NULL과 함께 남긴다(왼쪽 외부 조인). [Learn](https://learn.microsoft.com/en-us/dax/generateall-function-dax) · [DAX Guide](https://dax.guide/generateall/)
- **GENERATESERIES** **(D.1 예제 있음)** — 시작/끝/간격으로 **숫자 시퀀스 테이블**을 만든다. 파라미터 슬라이서용. [Learn](https://learn.microsoft.com/en-us/dax/generateseries-function-dax) · [DAX Guide](https://dax.guide/generateseries/)
- **GROUPBY** **(D.1 예제 있음)** — `SUMMARIZE`의 확장. `CURRENTGROUP()`을 통해 집계 식 내부에서 그룹의 서브셋을 참조할 수 있다. [Learn](https://learn.microsoft.com/en-us/dax/groupby-function-dax) · [DAX Guide](https://dax.guide/groupby/)
- **GROUPCROSSAPPLY** — GROUPCROSSAPPLY 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/groupcrossapply-function-dax) · [DAX Guide](https://dax.guide/groupcrossapply/)
- **GROUPCROSSAPPLYTABLE** — GROUPCROSSAPPLYTABLE 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/groupcrossapplytable-function-dax) · [DAX Guide](https://dax.guide/groupcrossapplytable/)
- **INTERSECT** **(D.1 예제 있음)** — 두 테이블의 **교집합**을 반환(왼쪽 테이블의 열 이름 사용). [Learn](https://learn.microsoft.com/en-us/dax/intersect-function-dax) · [DAX Guide](https://dax.guide/intersect/)
- **LAST** — LAST 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/last-function-dax) · [DAX Guide](https://dax.guide/last/)
- **NAMEOF** — NAMEOF 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/nameof-function-dax) · [DAX Guide](https://dax.guide/nameof/)
- **NATURALINNERJOIN** **(D.1 예제 있음)** — 공통 관계·이름으로 **내부 조인**한 표. [Learn](https://learn.microsoft.com/en-us/dax/naturalinnerjoin-function-dax) · [DAX Guide](https://dax.guide/naturalinnerjoin/)
- **NATURALJOINUSAGE** — NATURALJOINUSAGE 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/naturaljoinusage-function-dax) · [DAX Guide](https://dax.guide/naturaljoinusage/)
- **NATURALLEFTOUTERJOIN** **(D.1 예제 있음)** — 공통 관계·이름으로 **좌외부 조인**한 표. [Learn](https://learn.microsoft.com/en-us/dax/naturalleftouterjoin-function-dax) · [DAX Guide](https://dax.guide/naturalleftouterjoin/)
- **NEXT** — NEXT 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/next-function-dax) · [DAX Guide](https://dax.guide/next/)
- **PREVIOUS** — PREVIOUS 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/previous-function-dax) · [DAX Guide](https://dax.guide/previous/)
- **RANGE** — RANGE 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/range-function-dax) · [DAX Guide](https://dax.guide/range/)
- **ROLLUP** — ROLLUP 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/rollup-function-dax) · [DAX Guide](https://dax.guide/rollup/)
- **ROLLUPADDISSUBTOTAL** — ROLLUPADDISSUBTOTAL 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/rollupaddissubtotal-function-dax) · [DAX Guide](https://dax.guide/rollupaddissubtotal/)
- **ROLLUPGROUP** — ROLLUPGROUP 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/rollupgroup-function-dax) · [DAX Guide](https://dax.guide/rollupgroup/)
- **ROLLUPISSUBTOTAL** — ROLLUPISSUBTOTAL 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/rollupissubtotal-function-dax) · [DAX Guide](https://dax.guide/rollupissubtotal/)
- **ROW** **(D.1 예제 있음)** — 한 줄짜리 테이블을 만든다. 대시보드의 KPI 요약 테이블 생성에 유용. [Learn](https://learn.microsoft.com/en-us/dax/row-function-dax) · [DAX Guide](https://dax.guide/row/)
- **SELECTCOLUMNS** **(D.1 예제 있음)** — 입력 테이블에서 원하는 열만 골라 **새 이름으로 투영**한다. [Learn](https://learn.microsoft.com/en-us/dax/selectcolumns-function-dax) · [DAX Guide](https://dax.guide/selectcolumns/)
- **SUBSTITUTEWITHINDEX** — SUBSTITUTEWITHINDEX 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/substitutewithindex-function-dax) · [DAX Guide](https://dax.guide/substitutewithindex/)
- **SUMMARIZE** **(D.1 예제 있음)** — 그룹화 열로 집계한 표를 만든다. 단순 그룹화 용도로는 `SUMMARIZECOLUMNS`가 더 안전하다. [Learn](https://learn.microsoft.com/en-us/dax/summarize-function-dax) · [DAX Guide](https://dax.guide/summarize/)
- **SUMMARIZECOLUMNS** **(D.1 예제 있음)** — `SUMMARIZE`를 단순화한 버전. 필터·그룹·측정값을 한 번에 쓸 수 있어 쿼리·계산 테이블의 **표준 집계 함수**이다. [Learn](https://learn.microsoft.com/en-us/dax/summarizecolumns-function-dax) · [DAX Guide](https://dax.guide/summarizecolumns/)
- **TABLEOF** — TABLEOF 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/tableof-function-dax) · [DAX Guide](https://dax.guide/tableof/)
- **TOPN** **(D.1 예제 있음)** — 정렬 기준으로 상위 N개 행을 반환한다. 동률 포함. [Learn](https://learn.microsoft.com/en-us/dax/topn-function-dax) · [DAX Guide](https://dax.guide/topn/)
- **TOPNPERLEVEL** — TOPNPERLEVEL 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/topnperlevel-function-dax) · [DAX Guide](https://dax.guide/topnperlevel/)
- **TOPNSKIP** — TOPNSKIP 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다. [Learn](https://learn.microsoft.com/en-us/dax/topnskip-function-dax) · [DAX Guide](https://dax.guide/topnskip/)
- **UNION** **(D.1 예제 있음)** — 같은 열 구조를 가진 테이블들을 **세로로 결합**한다. 중복 유지. [Learn](https://learn.microsoft.com/en-us/dax/union-function-dax) · [DAX Guide](https://dax.guide/union/)
- **VALUES** **(D.1 예제 있음)** — 열의 **고유 값 테이블** 또는 테이블의 고유 행 테이블을 반환. 필터 컨텍스트를 존중한다. [Learn](https://learn.microsoft.com/en-us/dax/values-function-dax) · [DAX Guide](https://dax.guide/values/)

#### 시간 인텔리전스(Time Intelligence) (47개)

- **CALENDAR** **(D.1 예제 있음)** — 지정 범위의 연속 날짜 테이블을 생성한다. 날짜 테이블 만들 때 기본. [Learn](https://learn.microsoft.com/en-us/dax/calendar-function-dax) · [DAX Guide](https://dax.guide/calendar/)
- **CALENDARAUTO** **(D.1 예제 있음)** — 모델의 모든 날짜 열 범위를 탐지해 **자동으로** 연속 날짜 테이블을 만든다. [Learn](https://learn.microsoft.com/en-us/dax/calendarauto-function-dax) · [DAX Guide](https://dax.guide/calendarauto/)
- **CLOSINGBALANCEMONTH** — CLOSINGBALANCEMONTH 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/closingbalancemonth-function-dax) · [DAX Guide](https://dax.guide/closingbalancemonth/)
- **CLOSINGBALANCEQUARTER** — CLOSINGBALANCEQUARTER 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/closingbalancequarter-function-dax) · [DAX Guide](https://dax.guide/closingbalancequarter/)
- **CLOSINGBALANCEWEEK** — CLOSINGBALANCEWEEK 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/closingbalanceweek-function-dax) · [DAX Guide](https://dax.guide/closingbalanceweek/)
- **CLOSINGBALANCEYEAR** — CLOSINGBALANCEYEAR 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/closingbalanceyear-function-dax) · [DAX Guide](https://dax.guide/closingbalanceyear/)
- **DATEADD** **(D.1 예제 있음)** — 날짜 열을 **연/분기/월/일 단위로 이동**시킨 날짜 테이블 반환. `<interval>` = YEAR/QUARTER/MONTH/DAY. [Learn](https://learn.microsoft.com/en-us/dax/dateadd-function-dax) · [DAX Guide](https://dax.guide/dateadd/)
- **DATESBETWEEN** **(D.1 예제 있음)** — 두 날짜 사이의 날짜 집합 테이블. 누적 합계·지연 기간 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/datesbetween-function-dax) · [DAX Guide](https://dax.guide/datesbetween/)
- **DATESINPERIOD** **(D.1 예제 있음)** — 시작일로부터 N 단위 앞뒤 날짜를 반환. [Learn](https://learn.microsoft.com/en-us/dax/datesinperiod-function-dax) · [DAX Guide](https://dax.guide/datesinperiod/)
- **DATESMTD** — DATESMTD 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/datesmtd-function-dax) · [DAX Guide](https://dax.guide/datesmtd/)
- **DATESQTD** — DATESQTD 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/datesqtd-function-dax) · [DAX Guide](https://dax.guide/datesqtd/)
- **DATESWTD** — DATESWTD 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/dateswtd-function-dax) · [DAX Guide](https://dax.guide/dateswtd/)
- **DATESYTD** **(D.1 예제 있음)** — 현재 필터 내 연초부터 오늘까지의 날짜 집합. [Learn](https://learn.microsoft.com/en-us/dax/datesytd-function-dax) · [DAX Guide](https://dax.guide/datesytd/)
- **ENDOFMONTH** **(D.1 예제 있음)** — 현재 필터 내 최대 날짜가 속한 **월의 마지막 날**을 반환. [Learn](https://learn.microsoft.com/en-us/dax/endofmonth-function-dax) · [DAX Guide](https://dax.guide/endofmonth/)
- **ENDOFQUARTER** — ENDOFQUARTER 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/endofquarter-function-dax) · [DAX Guide](https://dax.guide/endofquarter/)
- **ENDOFWEEK** — ENDOFWEEK 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/endofweek-function-dax) · [DAX Guide](https://dax.guide/endofweek/)
- **ENDOFYEAR** — ENDOFYEAR 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/endofyear-function-dax) · [DAX Guide](https://dax.guide/endofyear/)
- **FIRSTDATE** — FIRSTDATE 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/firstdate-function-dax) · [DAX Guide](https://dax.guide/firstdate/)
- **FIRSTNONBLANK** — FIRSTNONBLANK 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/firstnonblank-function-dax) · [DAX Guide](https://dax.guide/firstnonblank/)
- **FIRSTNONBLANKVALUE** — FIRSTNONBLANKVALUE 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/firstnonblankvalue-function-dax) · [DAX Guide](https://dax.guide/firstnonblankvalue/)
- **LASTDATE** — LASTDATE 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/lastdate-function-dax) · [DAX Guide](https://dax.guide/lastdate/)
- **LASTNONBLANK** — LASTNONBLANK 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/lastnonblank-function-dax) · [DAX Guide](https://dax.guide/lastnonblank/)
- **LASTNONBLANKVALUE** — LASTNONBLANKVALUE 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/lastnonblankvalue-function-dax) · [DAX Guide](https://dax.guide/lastnonblankvalue/)
- **NEXTDAY** — NEXTDAY 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/nextday-function-dax) · [DAX Guide](https://dax.guide/nextday/)
- **NEXTMONTH** — NEXTMONTH 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/nextmonth-function-dax) · [DAX Guide](https://dax.guide/nextmonth/)
- **NEXTQUARTER** — NEXTQUARTER 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/nextquarter-function-dax) · [DAX Guide](https://dax.guide/nextquarter/)
- **NEXTWEEK** — NEXTWEEK 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/nextweek-function-dax) · [DAX Guide](https://dax.guide/nextweek/)
- **NEXTYEAR** — NEXTYEAR 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/nextyear-function-dax) · [DAX Guide](https://dax.guide/nextyear/)
- **OPENINGBALANCEMONTH** — OPENINGBALANCEMONTH 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/openingbalancemonth-function-dax) · [DAX Guide](https://dax.guide/openingbalancemonth/)
- **OPENINGBALANCEQUARTER** — OPENINGBALANCEQUARTER 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/openingbalancequarter-function-dax) · [DAX Guide](https://dax.guide/openingbalancequarter/)
- **OPENINGBALANCEWEEK** — OPENINGBALANCEWEEK 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/openingbalanceweek-function-dax) · [DAX Guide](https://dax.guide/openingbalanceweek/)
- **OPENINGBALANCEYEAR** — OPENINGBALANCEYEAR 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/openingbalanceyear-function-dax) · [DAX Guide](https://dax.guide/openingbalanceyear/)
- **PARALLELPERIOD** **(D.1 예제 있음)** — `DATEADD`와 유사하나 **전체 구간**(예: 한 달 전체)을 반환한다. [Learn](https://learn.microsoft.com/en-us/dax/parallelperiod-function-dax) · [DAX Guide](https://dax.guide/parallelperiod/)
- **PREVIOUSDAY** — PREVIOUSDAY 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/previousday-function-dax) · [DAX Guide](https://dax.guide/previousday/)
- **PREVIOUSMONTH** **(D.1 예제 있음)** — 현재 필터된 달의 **바로 이전 월 전체**를 반환. [Learn](https://learn.microsoft.com/en-us/dax/previousmonth-function-dax) · [DAX Guide](https://dax.guide/previousmonth/)
- **PREVIOUSQUARTER** — PREVIOUSQUARTER 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/previousquarter-function-dax) · [DAX Guide](https://dax.guide/previousquarter/)
- **PREVIOUSWEEK** — PREVIOUSWEEK 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/previousweek-function-dax) · [DAX Guide](https://dax.guide/previousweek/)
- **PREVIOUSYEAR** — PREVIOUSYEAR 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/previousyear-function-dax) · [DAX Guide](https://dax.guide/previousyear/)
- **SAMEPERIODLASTYEAR** **(D.1 예제 있음)** — 현재 필터된 날짜 구간을 **정확히 1년 전**으로 이동. [Learn](https://learn.microsoft.com/en-us/dax/sameperiodlastyear-function-dax) · [DAX Guide](https://dax.guide/sameperiodlastyear/)
- **STARTOFMONTH** **(D.1 예제 있음)** — 현재 필터 내 최소 날짜가 속한 **월의 첫날**을 반환. [Learn](https://learn.microsoft.com/en-us/dax/startofmonth-function-dax) · [DAX Guide](https://dax.guide/startofmonth/)
- **STARTOFQUARTER** — STARTOFQUARTER 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/startofquarter-function-dax) · [DAX Guide](https://dax.guide/startofquarter/)
- **STARTOFWEEK** — STARTOFWEEK 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/startofweek-function-dax) · [DAX Guide](https://dax.guide/startofweek/)
- **STARTOFYEAR** — STARTOFYEAR 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/startofyear-function-dax) · [DAX Guide](https://dax.guide/startofyear/)
- **TOTALMTD** — TOTALMTD 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/totalmtd-function-dax) · [DAX Guide](https://dax.guide/totalmtd/)
- **TOTALQTD** — TOTALQTD 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/totalqtd-function-dax) · [DAX Guide](https://dax.guide/totalqtd/)
- **TOTALWTD** — TOTALWTD 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다. [Learn](https://learn.microsoft.com/en-us/dax/totalwtd-function-dax) · [DAX Guide](https://dax.guide/totalwtd/)
- **TOTALYTD** **(D.1 예제 있음)** — `CALCULATE([Sales], DATESYTD(...))`의 단축형. 빠르게 YTD 측정값을 만들 때 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/totalytd-function-dax) · [DAX Guide](https://dax.guide/totalytd/)

#### 날짜·시간(Date & Time) (23개)

- **DATE** **(D.1 예제 있음)** — 세 숫자로부터 날짜 값을 생성. [Learn](https://learn.microsoft.com/en-us/dax/date-function-dax) · [DAX Guide](https://dax.guide/date/)
- **DATEDIFF** **(D.1 예제 있음)** — 두 날짜 사이의 간격을 지정 단위로 측정. `<interval>` = SECOND/MINUTE/HOUR/DAY/WEEK/MONTH/QUARTER/YEAR. [Learn](https://learn.microsoft.com/en-us/dax/datediff-function-dax) · [DAX Guide](https://dax.guide/datediff/)
- **DATEVALUE** — DATEVALUE 날짜/시간 조작 함수. 스칼라 날짜 값을 다룬다. [Learn](https://learn.microsoft.com/en-us/dax/datevalue-function-dax) · [DAX Guide](https://dax.guide/datevalue/)
- **DAY** **(D.1 예제 있음)** — 날짜에서 일(1~31) 추출. [Learn](https://learn.microsoft.com/en-us/dax/day-function-dax) · [DAX Guide](https://dax.guide/day/)
- **DURATION** — DURATION 날짜/시간 조작 함수. 스칼라 날짜 값을 다룬다. [Learn](https://learn.microsoft.com/en-us/dax/duration-function-dax) · [DAX Guide](https://dax.guide/duration/)
- **EDATE** **(D.1 예제 있음)** — 월 단위로 날짜를 이동. `EOMONTH`의 임의 날짜 버전. [Learn](https://learn.microsoft.com/en-us/dax/edate-function-dax) · [DAX Guide](https://dax.guide/edate/)
- **EOMONTH** **(D.1 예제 있음)** — 지정 월수만큼 이동한 월의 **마지막 날** 반환. [Learn](https://learn.microsoft.com/en-us/dax/eomonth-function-dax) · [DAX Guide](https://dax.guide/eomonth/)
- **HOUR** — HOUR 날짜/시간 조작 함수. 스칼라 날짜 값을 다룬다. [Learn](https://learn.microsoft.com/en-us/dax/hour-function-dax) · [DAX Guide](https://dax.guide/hour/)
- **MINUTE** — MINUTE 날짜/시간 조작 함수. 스칼라 날짜 값을 다룬다. [Learn](https://learn.microsoft.com/en-us/dax/minute-function-dax) · [DAX Guide](https://dax.guide/minute/)
- **MONTH** **(D.1 예제 있음)** — 날짜에서 월(1~12) 추출. [Learn](https://learn.microsoft.com/en-us/dax/month-function-dax) · [DAX Guide](https://dax.guide/month/)
- **NETWORKDAYS** — NETWORKDAYS 날짜/시간 조작 함수. 스칼라 날짜 값을 다룬다. [Learn](https://learn.microsoft.com/en-us/dax/networkdays-function-dax) · [DAX Guide](https://dax.guide/networkdays/)
- **NOW** **(D.1 예제 있음)** — 현재 날짜와 시각. [Learn](https://learn.microsoft.com/en-us/dax/now-function-dax) · [DAX Guide](https://dax.guide/now/)
- **QUARTER** — QUARTER 날짜/시간 조작 함수. 스칼라 날짜 값을 다룬다. [Learn](https://learn.microsoft.com/en-us/dax/quarter-function-dax) · [DAX Guide](https://dax.guide/quarter/)
- **SECOND** — SECOND 날짜/시간 조작 함수. 스칼라 날짜 값을 다룬다. [Learn](https://learn.microsoft.com/en-us/dax/second-function-dax) · [DAX Guide](https://dax.guide/second/)
- **TIME** — TIME 날짜/시간 조작 함수. 스칼라 날짜 값을 다룬다. [Learn](https://learn.microsoft.com/en-us/dax/time-function-dax) · [DAX Guide](https://dax.guide/time/)
- **TIMEVALUE** — TIMEVALUE 날짜/시간 조작 함수. 스칼라 날짜 값을 다룬다. [Learn](https://learn.microsoft.com/en-us/dax/timevalue-function-dax) · [DAX Guide](https://dax.guide/timevalue/)
- **TODAY** **(D.1 예제 있음)** — 오늘의 날짜(시각 없음). [Learn](https://learn.microsoft.com/en-us/dax/today-function-dax) · [DAX Guide](https://dax.guide/today/)
- **UTCNOW** — UTCNOW 날짜/시간 조작 함수. 스칼라 날짜 값을 다룬다. [Learn](https://learn.microsoft.com/en-us/dax/utcnow-function-dax) · [DAX Guide](https://dax.guide/utcnow/)
- **UTCTODAY** — UTCTODAY 날짜/시간 조작 함수. 스칼라 날짜 값을 다룬다. [Learn](https://learn.microsoft.com/en-us/dax/utctoday-function-dax) · [DAX Guide](https://dax.guide/utctoday/)
- **WEEKDAY** **(D.1 예제 있음)** — 요일을 숫자로 반환. `return_type`에 따라 기준이 다름(1: 일=1). [Learn](https://learn.microsoft.com/en-us/dax/weekday-function-dax) · [DAX Guide](https://dax.guide/weekday/)
- **WEEKNUM** **(D.1 예제 있음)** — 해의 주 번호(1~54). [Learn](https://learn.microsoft.com/en-us/dax/weeknum-function-dax) · [DAX Guide](https://dax.guide/weeknum/)
- **YEAR** **(D.1 예제 있음)** — 날짜에서 연도(숫자) 추출. [Learn](https://learn.microsoft.com/en-us/dax/year-function-dax) · [DAX Guide](https://dax.guide/year/)
- **YEARFRAC** **(D.1 예제 있음)** — 두 날짜의 연 단위 소수 차이. [Learn](https://learn.microsoft.com/en-us/dax/yearfrac-function-dax) · [DAX Guide](https://dax.guide/yearfrac/)

#### 텍스트(Text) (25개)

- **COMBINEVALUES** **(D.1 예제 있음)** — 여러 값을 **키 구분자**로 합친다. 복합키 조인 준비 시 사용. [Learn](https://learn.microsoft.com/en-us/dax/combinevalues-function-dax) · [DAX Guide](https://dax.guide/combinevalues/)
- **CONCATENATE** **(D.1 예제 있음)** — 두 문자열을 이어 붙인다. 연산자 `&`와 동일. [Learn](https://learn.microsoft.com/en-us/dax/concatenate-function-dax) · [DAX Guide](https://dax.guide/concatenate/)
- **CONCATENATEX** **(D.1 예제 있음)** — 각 행에 식을 평가하고 구분자로 이어 붙여 하나의 문자열 반환. [Learn](https://learn.microsoft.com/en-us/dax/concatenatex-function-dax) · [DAX Guide](https://dax.guide/concatenatex/)
- **EXACT** — EXACT 문자열 조작 함수. [Learn](https://learn.microsoft.com/en-us/dax/exact-function-dax) · [DAX Guide](https://dax.guide/exact/)
- **FIND** **(D.1 예제 있음)** — 대소문자 구분 위치 찾기(1부터). 없으면 오류 또는 대체 값. [Learn](https://learn.microsoft.com/en-us/dax/find-function-dax) · [DAX Guide](https://dax.guide/find/)
- **FIXED** — FIXED 문자열 조작 함수. [Learn](https://learn.microsoft.com/en-us/dax/fixed-function-dax) · [DAX Guide](https://dax.guide/fixed/)
- **FORMAT** **(D.1 예제 있음)** — 값을 지정한 서식 문자열로 **문자열**로 변환. [Learn](https://learn.microsoft.com/en-us/dax/format-function-dax) · [DAX Guide](https://dax.guide/format/)
- **HASH** — HASH 문자열 조작 함수. [Learn](https://learn.microsoft.com/en-us/dax/hash-function-dax) · [DAX Guide](https://dax.guide/hash/)
- **KEYWORDMATCH** — KEYWORDMATCH 문자열 조작 함수. [Learn](https://learn.microsoft.com/en-us/dax/keywordmatch-function-dax) · [DAX Guide](https://dax.guide/keywordmatch/)
- **LEFT** **(D.1 예제 있음)** — 왼쪽에서 N자 문자열. [Learn](https://learn.microsoft.com/en-us/dax/left-function-dax) · [DAX Guide](https://dax.guide/left/)
- **LEN** **(D.1 예제 있음)** — 문자열 길이. [Learn](https://learn.microsoft.com/en-us/dax/len-function-dax) · [DAX Guide](https://dax.guide/len/)
- **LOWER** **(D.1 예제 있음)** — 소문자화. [Learn](https://learn.microsoft.com/en-us/dax/lower-function-dax) · [DAX Guide](https://dax.guide/lower/)
- **MID** **(D.1 예제 있음)** — 지정 위치부터 N자. [Learn](https://learn.microsoft.com/en-us/dax/mid-function-dax) · [DAX Guide](https://dax.guide/mid/)
- **REPLACE** **(D.1 예제 있음)** — 지정 위치의 N자를 새 문자열로 바꾼다. [Learn](https://learn.microsoft.com/en-us/dax/replace-function-dax) · [DAX Guide](https://dax.guide/replace/)
- **REPT** — REPT 문자열 조작 함수. [Learn](https://learn.microsoft.com/en-us/dax/rept-function-dax) · [DAX Guide](https://dax.guide/rept/)
- **RIGHT** **(D.1 예제 있음)** — 오른쪽에서 N자. [Learn](https://learn.microsoft.com/en-us/dax/right-function-dax) · [DAX Guide](https://dax.guide/right/)
- **SEARCH** **(D.1 예제 있음)** — 대소문자 **구분 없이** 찾기. 와일드카드 `?`, `*` 허용. [Learn](https://learn.microsoft.com/en-us/dax/search-function-dax) · [DAX Guide](https://dax.guide/search/)
- **SUBSTITUTE** **(D.1 예제 있음)** — 문자열에서 지정 패턴을 치환. N번째 발생만 바꿀 수 있음. [Learn](https://learn.microsoft.com/en-us/dax/substitute-function-dax) · [DAX Guide](https://dax.guide/substitute/)
- **TOCSV** — TOCSV 문자열 조작 함수. [Learn](https://learn.microsoft.com/en-us/dax/tocsv-function-dax) · [DAX Guide](https://dax.guide/tocsv/)
- **TOJSON** — TOJSON 문자열 조작 함수. [Learn](https://learn.microsoft.com/en-us/dax/tojson-function-dax) · [DAX Guide](https://dax.guide/tojson/)
- **TRIM** **(D.1 예제 있음)** — 앞뒤 공백과 중간 중복 공백을 **단일 공백**으로 정리. [Learn](https://learn.microsoft.com/en-us/dax/trim-function-dax) · [DAX Guide](https://dax.guide/trim/)
- **UNICHAR** — UNICHAR 문자열 조작 함수. [Learn](https://learn.microsoft.com/en-us/dax/unichar-function-dax) · [DAX Guide](https://dax.guide/unichar/)
- **UNICODE** — UNICODE 문자열 조작 함수. [Learn](https://learn.microsoft.com/en-us/dax/unicode-function-dax) · [DAX Guide](https://dax.guide/unicode/)
- **UPPER** **(D.1 예제 있음)** — 대문자화. [Learn](https://learn.microsoft.com/en-us/dax/upper-function-dax) · [DAX Guide](https://dax.guide/upper/)
- **VALUE** **(D.1 예제 있음)** — 문자열을 숫자로 변환. 로케일 문제를 주의. [Learn](https://learn.microsoft.com/en-us/dax/value-function-dax) · [DAX Guide](https://dax.guide/value/)

#### 수학·삼각(Math & Trig) (59개)

- **ABS** **(D.1 예제 있음)** — 절댓값. [Learn](https://learn.microsoft.com/en-us/dax/abs-function-dax) · [DAX Guide](https://dax.guide/abs/)
- **ACOS** — ACOS 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/acos-function-dax) · [DAX Guide](https://dax.guide/acos/)
- **ACOSH** — ACOSH 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/acosh-function-dax) · [DAX Guide](https://dax.guide/acosh/)
- **ACOT** — ACOT 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/acot-function-dax) · [DAX Guide](https://dax.guide/acot/)
- **ACOTH** — ACOTH 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/acoth-function-dax) · [DAX Guide](https://dax.guide/acoth/)
- **ASIN** — ASIN 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/asin-function-dax) · [DAX Guide](https://dax.guide/asin/)
- **ASINH** — ASINH 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/asinh-function-dax) · [DAX Guide](https://dax.guide/asinh/)
- **ATAN** — ATAN 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/atan-function-dax) · [DAX Guide](https://dax.guide/atan/)
- **ATANH** — ATANH 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/atanh-function-dax) · [DAX Guide](https://dax.guide/atanh/)
- **BITAND** — BITAND 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/bitand-function-dax) · [DAX Guide](https://dax.guide/bitand/)
- **BITLSHIFT** — BITLSHIFT 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/bitlshift-function-dax) · [DAX Guide](https://dax.guide/bitlshift/)
- **BITOR** — BITOR 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/bitor-function-dax) · [DAX Guide](https://dax.guide/bitor/)
- **BITRSHIFT** — BITRSHIFT 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/bitrshift-function-dax) · [DAX Guide](https://dax.guide/bitrshift/)
- **BITXOR** — BITXOR 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/bitxor-function-dax) · [DAX Guide](https://dax.guide/bitxor/)
- **CEILING** **(D.1 예제 있음)** — 지정 배수로 올림. [Learn](https://learn.microsoft.com/en-us/dax/ceiling-function-dax) · [DAX Guide](https://dax.guide/ceiling/)
- **COMBIN** — COMBIN 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/combin-function-dax) · [DAX Guide](https://dax.guide/combin/)
- **COMBINA** — COMBINA 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/combina-function-dax) · [DAX Guide](https://dax.guide/combina/)
- **CONVERT** — CONVERT 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/convert-function-dax) · [DAX Guide](https://dax.guide/convert/)
- **COS** — COS 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/cos-function-dax) · [DAX Guide](https://dax.guide/cos/)
- **COSH** — COSH 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/cosh-function-dax) · [DAX Guide](https://dax.guide/cosh/)
- **COT** — COT 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/cot-function-dax) · [DAX Guide](https://dax.guide/cot/)
- **COTH** — COTH 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/coth-function-dax) · [DAX Guide](https://dax.guide/coth/)
- **CURRENCY** — CURRENCY 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/currency-function-dax) · [DAX Guide](https://dax.guide/currency/)
- **DEGREES** — DEGREES 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/degrees-function-dax) · [DAX Guide](https://dax.guide/degrees/)
- **DIVIDE** **(D.1 예제 있음)** — 안전 나눗셈. 분모가 0/BLANK면 대체값(기본 BLANK). `/`연산자보다 먼저 고려. [Learn](https://learn.microsoft.com/en-us/dax/divide-function-dax) · [DAX Guide](https://dax.guide/divide/)
- **EVEN** — EVEN 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/even-function-dax) · [DAX Guide](https://dax.guide/even/)
- **EXP** **(D.1 예제 있음)** — `e`의 거듭제곱. [Learn](https://learn.microsoft.com/en-us/dax/exp-function-dax) · [DAX Guide](https://dax.guide/exp/)
- **FACT** — FACT 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/fact-function-dax) · [DAX Guide](https://dax.guide/fact/)
- **FLOOR** **(D.1 예제 있음)** — 지정 배수로 내림. [Learn](https://learn.microsoft.com/en-us/dax/floor-function-dax) · [DAX Guide](https://dax.guide/floor/)
- **GCD** — GCD 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/gcd-function-dax) · [DAX Guide](https://dax.guide/gcd/)
- **INT** **(D.1 예제 있음)** — 가장 가까운 **작은 정수**로 내림. [Learn](https://learn.microsoft.com/en-us/dax/int-function-dax) · [DAX Guide](https://dax.guide/int/)
- **ISO.CEILING** — ISO.CEILING 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/iso-ceiling-function-dax) · [DAX Guide](https://dax.guide/iso-ceiling/)
- **LCM** — LCM 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/lcm-function-dax) · [DAX Guide](https://dax.guide/lcm/)
- **LN** **(D.1 예제 있음)** — 자연로그. [Learn](https://learn.microsoft.com/en-us/dax/ln-function-dax) · [DAX Guide](https://dax.guide/ln/)
- **LOG** **(D.1 예제 있음)** — 지정 밑의 로그(기본 10). [Learn](https://learn.microsoft.com/en-us/dax/log-function-dax) · [DAX Guide](https://dax.guide/log/)
- **LOG10** **(D.1 예제 있음)** — 상용로그. [Learn](https://learn.microsoft.com/en-us/dax/log10-function-dax) · [DAX Guide](https://dax.guide/log10/)
- **MOD** **(D.1 예제 있음)** — 나머지. [Learn](https://learn.microsoft.com/en-us/dax/mod-function-dax) · [DAX Guide](https://dax.guide/mod/)
- **MOVINGAVERAGE** — MOVINGAVERAGE 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/movingaverage-function-dax) · [DAX Guide](https://dax.guide/movingaverage/)
- **MROUND** — MROUND 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/mround-function-dax) · [DAX Guide](https://dax.guide/mround/)
- **ODD** — ODD 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/odd-function-dax) · [DAX Guide](https://dax.guide/odd/)
- **PERMUT** — PERMUT 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/permut-function-dax) · [DAX Guide](https://dax.guide/permut/)
- **PI** — PI 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/pi-function-dax) · [DAX Guide](https://dax.guide/pi/)
- **POWER** **(D.1 예제 있음)** — 거듭제곱. [Learn](https://learn.microsoft.com/en-us/dax/power-function-dax) · [DAX Guide](https://dax.guide/power/)
- **QUOTIENT** — QUOTIENT 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/quotient-function-dax) · [DAX Guide](https://dax.guide/quotient/)
- **RADIANS** — RADIANS 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/radians-function-dax) · [DAX Guide](https://dax.guide/radians/)
- **RAND** **(D.1 예제 있음)** — 0 이상 1 미만 난수. [Learn](https://learn.microsoft.com/en-us/dax/rand-function-dax) · [DAX Guide](https://dax.guide/rand/)
- **RANDBETWEEN** **(D.1 예제 있음)** — 정수 난수. [Learn](https://learn.microsoft.com/en-us/dax/randbetween-function-dax) · [DAX Guide](https://dax.guide/randbetween/)
- **ROUND** **(D.1 예제 있음)** — 반올림. [Learn](https://learn.microsoft.com/en-us/dax/round-function-dax) · [DAX Guide](https://dax.guide/round/)
- **ROUNDDOWN** **(D.1 예제 있음)** — 0 쪽으로 내림. [Learn](https://learn.microsoft.com/en-us/dax/rounddown-function-dax) · [DAX Guide](https://dax.guide/rounddown/)
- **ROUNDUP** **(D.1 예제 있음)** — 0에서 먼 쪽으로 올림. [Learn](https://learn.microsoft.com/en-us/dax/roundup-function-dax) · [DAX Guide](https://dax.guide/roundup/)
- **RUNNINGSUM** — RUNNINGSUM 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/runningsum-function-dax) · [DAX Guide](https://dax.guide/runningsum/)
- **SIGN** — SIGN 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/sign-function-dax) · [DAX Guide](https://dax.guide/sign/)
- **SIN** — SIN 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/sin-function-dax) · [DAX Guide](https://dax.guide/sin/)
- **SINH** — SINH 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/sinh-function-dax) · [DAX Guide](https://dax.guide/sinh/)
- **SQRT** **(D.1 예제 있음)** — 양의 제곱근. [Learn](https://learn.microsoft.com/en-us/dax/sqrt-function-dax) · [DAX Guide](https://dax.guide/sqrt/)
- **SQRTPI** — SQRTPI 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/sqrtpi-function-dax) · [DAX Guide](https://dax.guide/sqrtpi/)
- **TAN** — TAN 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/tan-function-dax) · [DAX Guide](https://dax.guide/tan/)
- **TANH** — TANH 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/tanh-function-dax) · [DAX Guide](https://dax.guide/tanh/)
- **TRUNC** — TRUNC 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다. [Learn](https://learn.microsoft.com/en-us/dax/trunc-function-dax) · [DAX Guide](https://dax.guide/trunc/)

#### 통계(Statistical) (42개)

- **BETA.DIST** — BETA.DIST 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/beta-dist-function-dax) · [DAX Guide](https://dax.guide/beta-dist/)
- **BETA.INV** — BETA.INV 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/beta-inv-function-dax) · [DAX Guide](https://dax.guide/beta-inv/)
- **CHISQ.DIST** — CHISQ.DIST 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/chisq-dist-function-dax) · [DAX Guide](https://dax.guide/chisq-dist/)
- **CHISQ.DIST.RT** — CHISQ.DIST.RT 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/chisq-dist-rt-function-dax) · [DAX Guide](https://dax.guide/chisq-dist-rt/)
- **CHISQ.INV** — CHISQ.INV 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/chisq-inv-function-dax) · [DAX Guide](https://dax.guide/chisq-inv/)
- **CHISQ.INV.RT** — CHISQ.INV.RT 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/chisq-inv-rt-function-dax) · [DAX Guide](https://dax.guide/chisq-inv-rt/)
- **CONFIDENCE.NORM** — CONFIDENCE.NORM 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/confidence-norm-function-dax) · [DAX Guide](https://dax.guide/confidence-norm/)
- **CONFIDENCE.T** — CONFIDENCE.T 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/confidence-t-function-dax) · [DAX Guide](https://dax.guide/confidence-t/)
- **EXPON.DIST** — EXPON.DIST 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/expon-dist-function-dax) · [DAX Guide](https://dax.guide/expon-dist/)
- **GEOMEAN** **(D.1 예제 있음)** — 기하 평균. 수익률 계열에 사용. [Learn](https://learn.microsoft.com/en-us/dax/geomean-function-dax) · [DAX Guide](https://dax.guide/geomean/)
- **GEOMEANX** — GEOMEANX 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/geomeanx-function-dax) · [DAX Guide](https://dax.guide/geomeanx/)
- **LINEST** — LINEST 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/linest-function-dax) · [DAX Guide](https://dax.guide/linest/)
- **LINESTX** — LINESTX 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/linestx-function-dax) · [DAX Guide](https://dax.guide/linestx/)
- **MEDIAN** **(D.1 예제 있음)** — 중앙값. [Learn](https://learn.microsoft.com/en-us/dax/median-function-dax) · [DAX Guide](https://dax.guide/median/)
- **MEDIANX** — MEDIANX 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/medianx-function-dax) · [DAX Guide](https://dax.guide/medianx/)
- **NORM.DIST** — NORM.DIST 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/norm-dist-function-dax) · [DAX Guide](https://dax.guide/norm-dist/)
- **NORM.INV** — NORM.INV 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/norm-inv-function-dax) · [DAX Guide](https://dax.guide/norm-inv/)
- **NORM.S.DIST** — NORM.S.DIST 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/norm-s-dist-function-dax) · [DAX Guide](https://dax.guide/norm-s-dist/)
- **NORM.S.INV** — NORM.S.INV 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/norm-s-inv-function-dax) · [DAX Guide](https://dax.guide/norm-s-inv/)
- **PERCENTILE.EXC** **(D.1 예제 있음)** — k 분위수(배타식). [Learn](https://learn.microsoft.com/en-us/dax/percentile-exc-function-dax) · [DAX Guide](https://dax.guide/percentile-exc/)
- **PERCENTILE.INC** **(D.1 예제 있음)** — 열의 **k 분위수**(0~1 포함식). [Learn](https://learn.microsoft.com/en-us/dax/percentile-inc-function-dax) · [DAX Guide](https://dax.guide/percentile-inc/)
- **PERCENTILEX.EXC** — PERCENTILEX.EXC 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/percentilex-exc-function-dax) · [DAX Guide](https://dax.guide/percentilex-exc/)
- **PERCENTILEX.INC** — PERCENTILEX.INC 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/percentilex-inc-function-dax) · [DAX Guide](https://dax.guide/percentilex-inc/)
- **POISSON.DIST** — POISSON.DIST 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/poisson-dist-function-dax) · [DAX Guide](https://dax.guide/poisson-dist/)
- **RANK.EQ** **(D.1 예제 있음)** — 값이 참조 열에서 차지하는 순위(동률 같은 순위). [Learn](https://learn.microsoft.com/en-us/dax/rank-eq-function-dax) · [DAX Guide](https://dax.guide/rank-eq/)
- **RANKX** **(D.1 예제 있음)** — 테이블을 식으로 정렬하고 현재 컨텍스트의 값 **순위**를 돌려준다. [Learn](https://learn.microsoft.com/en-us/dax/rankx-function-dax) · [DAX Guide](https://dax.guide/rankx/)
- **SAMPLE** — SAMPLE 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/sample-function-dax) · [DAX Guide](https://dax.guide/sample/)
- **SAMPLEAXISWITHLOCALMINMAX** — SAMPLEAXISWITHLOCALMINMAX 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/sampleaxiswithlocalminmax-function-dax) · [DAX Guide](https://dax.guide/sampleaxiswithlocalminmax/)
- **SAMPLECARTESIANPOINTSBYCOVER** — SAMPLECARTESIANPOINTSBYCOVER 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/samplecartesianpointsbycover-function-dax) · [DAX Guide](https://dax.guide/samplecartesianpointsbycover/)
- **STDEV.P** **(D.1 예제 있음)** — 모집단 표준편차. [Learn](https://learn.microsoft.com/en-us/dax/stdev-p-function-dax) · [DAX Guide](https://dax.guide/stdev-p/)
- **STDEV.S** **(D.1 예제 있음)** — 표본 표준편차. [Learn](https://learn.microsoft.com/en-us/dax/stdev-s-function-dax) · [DAX Guide](https://dax.guide/stdev-s/)
- **STDEVX.P** — STDEVX.P 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/stdevx-p-function-dax) · [DAX Guide](https://dax.guide/stdevx-p/)
- **STDEVX.S** — STDEVX.S 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/stdevx-s-function-dax) · [DAX Guide](https://dax.guide/stdevx-s/)
- **T.DIST** — T.DIST 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/t-dist-function-dax) · [DAX Guide](https://dax.guide/t-dist/)
- **T.DIST.2T** — T.DIST.2T 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/t-dist-2t-function-dax) · [DAX Guide](https://dax.guide/t-dist-2t/)
- **T.DIST.RT** — T.DIST.RT 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/t-dist-rt-function-dax) · [DAX Guide](https://dax.guide/t-dist-rt/)
- **T.INV** — T.INV 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/t-inv-function-dax) · [DAX Guide](https://dax.guide/t-inv/)
- **T.INV.2T** — T.INV.2T 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/t-inv-2t-function-dax) · [DAX Guide](https://dax.guide/t-inv-2t/)
- **VAR.P** **(D.1 예제 있음)** — 모집단 분산. [Learn](https://learn.microsoft.com/en-us/dax/var-p-function-dax) · [DAX Guide](https://dax.guide/var-p/)
- **VAR.S** **(D.1 예제 있음)** — 표본 분산. [Learn](https://learn.microsoft.com/en-us/dax/var-s-function-dax) · [DAX Guide](https://dax.guide/var-s/)
- **VARX.P** — VARX.P 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/varx-p-function-dax) · [DAX Guide](https://dax.guide/varx-p/)
- **VARX.S** — VARX.S 통계·분포 함수. 확률·분포·적합 계산에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/varx-s-function-dax) · [DAX Guide](https://dax.guide/varx-s/)

#### 정보(Information) (37개)

- **BLANK** **(D.1 예제 있음)** — NULL 상수. 집계 시 무시됨. [Learn](https://learn.microsoft.com/en-us/dax/blank-function-dax) · [DAX Guide](https://dax.guide/blank/)
- **COLUMNSTATISTICS** **(D.1 예제 있음)** — 엔진이 기록한 열 통계 테이블을 반환(엔지니어링 진단용). [Learn](https://learn.microsoft.com/en-us/dax/columnstatistics-function-dax) · [DAX Guide](https://dax.guide/columnstatistics/)
- **CUSTOMDATA** **(D.1 예제 있음)** — 연결 문자열에 담긴 사용자 지정 식별자. 임베드 시나리오에서 사용. [Learn](https://learn.microsoft.com/en-us/dax/customdata-function-dax) · [DAX Guide](https://dax.guide/customdata/)
- **ERROR** — ERROR 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/error-function-dax) · [DAX Guide](https://dax.guide/error/)
- **EVALUATEANDLOG** — EVALUATEANDLOG 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/evaluateandlog-function-dax) · [DAX Guide](https://dax.guide/evaluateandlog/)
- **ISAFTER** — ISAFTER 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/isafter-function-dax) · [DAX Guide](https://dax.guide/isafter/)
- **ISATLEVEL** — ISATLEVEL 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/isatlevel-function-dax) · [DAX Guide](https://dax.guide/isatlevel/)
- **ISBLANK** **(D.1 예제 있음)** — 값이 BLANK이면 TRUE. BLANK는 DAX의 NULL에 해당. [Learn](https://learn.microsoft.com/en-us/dax/isblank-function-dax) · [DAX Guide](https://dax.guide/isblank/)
- **ISBOOLEAN** — ISBOOLEAN 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/isboolean-function-dax) · [DAX Guide](https://dax.guide/isboolean/)
- **ISCURRENCY** — ISCURRENCY 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/iscurrency-function-dax) · [DAX Guide](https://dax.guide/iscurrency/)
- **ISDATETIME** — ISDATETIME 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/isdatetime-function-dax) · [DAX Guide](https://dax.guide/isdatetime/)
- **ISDECIMAL** — ISDECIMAL 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/isdecimal-function-dax) · [DAX Guide](https://dax.guide/isdecimal/)
- **ISDOUBLE** — ISDOUBLE 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/isdouble-function-dax) · [DAX Guide](https://dax.guide/isdouble/)
- **ISEMPTY** — ISEMPTY 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/isempty-function-dax) · [DAX Guide](https://dax.guide/isempty/)
- **ISERROR** **(D.1 예제 있음)** — 식이 오류를 내는지 검사. [Learn](https://learn.microsoft.com/en-us/dax/iserror-function-dax) · [DAX Guide](https://dax.guide/iserror/)
- **ISEVEN** — ISEVEN 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/iseven-function-dax) · [DAX Guide](https://dax.guide/iseven/)
- **ISINSCOPE** **(D.1 예제 있음)** — 현재 시각적 개체에서 그 **열이 그룹화 키**로 쓰이는 수준에 있는지 검사. 매트릭스의 소계 여부 판정에 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/isinscope-function-dax) · [DAX Guide](https://dax.guide/isinscope/)
- **ISINT64** — ISINT64 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/isint64-function-dax) · [DAX Guide](https://dax.guide/isint64/)
- **ISINTEGER** — ISINTEGER 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/isinteger-function-dax) · [DAX Guide](https://dax.guide/isinteger/)
- **ISLOGICAL** — ISLOGICAL 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/islogical-function-dax) · [DAX Guide](https://dax.guide/islogical/)
- **ISNONTEXT** — ISNONTEXT 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/isnontext-function-dax) · [DAX Guide](https://dax.guide/isnontext/)
- **ISNUMBER** **(D.1 예제 있음)** — 숫자형 값인지 검사. [Learn](https://learn.microsoft.com/en-us/dax/isnumber-function-dax) · [DAX Guide](https://dax.guide/isnumber/)
- **ISNUMERIC** — ISNUMERIC 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/isnumeric-function-dax) · [DAX Guide](https://dax.guide/isnumeric/)
- **ISODD** — ISODD 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/isodd-function-dax) · [DAX Guide](https://dax.guide/isodd/)
- **ISONORAFTER** — ISONORAFTER 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/isonorafter-function-dax) · [DAX Guide](https://dax.guide/isonorafter/)
- **ISSELECTEDMEASURE** — ISSELECTEDMEASURE 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/isselectedmeasure-function-dax) · [DAX Guide](https://dax.guide/isselectedmeasure/)
- **ISSTRING** — ISSTRING 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/isstring-function-dax) · [DAX Guide](https://dax.guide/isstring/)
- **ISSUBTOTAL** **(D.1 예제 있음)** — `SUMMARIZE` 결과 행이 소계 행인지 표시. `ROLLUP*`과 함께 쓴다. [Learn](https://learn.microsoft.com/en-us/dax/issubtotal-function-dax) · [DAX Guide](https://dax.guide/issubtotal/)
- **ISTEXT** **(D.1 예제 있음)** — 텍스트형 값인지 검사. [Learn](https://learn.microsoft.com/en-us/dax/istext-function-dax) · [DAX Guide](https://dax.guide/istext/)
- **LOOKUP** — LOOKUP 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/lookup-function-dax) · [DAX Guide](https://dax.guide/lookup/)
- **SELECTEDMEASURE** **(D.1 예제 있음)** — **계산 그룹**에서 현재 적용되는 측정값을 나타낸다. 계산 항목의 식 안에서만 의미가 있다. [Learn](https://learn.microsoft.com/en-us/dax/selectedmeasure-function-dax) · [DAX Guide](https://dax.guide/selectedmeasure/)
- **SELECTEDMEASUREFORMATSTRING** — SELECTEDMEASUREFORMATSTRING 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/selectedmeasureformatstring-function-dax) · [DAX Guide](https://dax.guide/selectedmeasureformatstring/)
- **SELECTEDMEASURENAME** **(D.1 예제 있음)** — 현재 선택된 측정값의 이름(문자열). [Learn](https://learn.microsoft.com/en-us/dax/selectedmeasurename-function-dax) · [DAX Guide](https://dax.guide/selectedmeasurename/)
- **USERCULTURE** — USERCULTURE 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/userculture-function-dax) · [DAX Guide](https://dax.guide/userculture/)
- **USERNAME** **(D.1 예제 있음)** — 현재 보고서 사용자 ID(`domain\user` 또는 UPN). RLS에 필수. [Learn](https://learn.microsoft.com/en-us/dax/username-function-dax) · [DAX Guide](https://dax.guide/username/)
- **USEROBJECTID** — USEROBJECTID 정보 함수. 값의 형식·상태·환경을 검사한다. [Learn](https://learn.microsoft.com/en-us/dax/userobjectid-function-dax) · [DAX Guide](https://dax.guide/userobjectid/)
- **USERPRINCIPALNAME** **(D.1 예제 있음)** — 현재 사용자의 UPN(이메일 형식). [Learn](https://learn.microsoft.com/en-us/dax/userprincipalname-function-dax) · [DAX Guide](https://dax.guide/userprincipalname/)

#### 재무(Financial) (50개)

- **ACCRINT** — ACCRINT 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/accrint-function-dax) · [DAX Guide](https://dax.guide/accrint/)
- **ACCRINTM** — ACCRINTM 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/accrintm-function-dax) · [DAX Guide](https://dax.guide/accrintm/)
- **AMORDEGRC** — AMORDEGRC 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/amordegrc-function-dax) · [DAX Guide](https://dax.guide/amordegrc/)
- **AMORLINC** — AMORLINC 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/amorlinc-function-dax) · [DAX Guide](https://dax.guide/amorlinc/)
- **COUPDAYBS** — COUPDAYBS 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/coupdaybs-function-dax) · [DAX Guide](https://dax.guide/coupdaybs/)
- **COUPDAYS** — COUPDAYS 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/coupdays-function-dax) · [DAX Guide](https://dax.guide/coupdays/)
- **COUPDAYSNC** — COUPDAYSNC 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/coupdaysnc-function-dax) · [DAX Guide](https://dax.guide/coupdaysnc/)
- **COUPNCD** — COUPNCD 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/coupncd-function-dax) · [DAX Guide](https://dax.guide/coupncd/)
- **COUPNUM** — COUPNUM 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/coupnum-function-dax) · [DAX Guide](https://dax.guide/coupnum/)
- **COUPPCD** — COUPPCD 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/couppcd-function-dax) · [DAX Guide](https://dax.guide/couppcd/)
- **CUMIPMT** — CUMIPMT 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/cumipmt-function-dax) · [DAX Guide](https://dax.guide/cumipmt/)
- **CUMPRINC** — CUMPRINC 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/cumprinc-function-dax) · [DAX Guide](https://dax.guide/cumprinc/)
- **DB** — DB 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/db-function-dax) · [DAX Guide](https://dax.guide/db/)
- **DDB** — DDB 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/ddb-function-dax) · [DAX Guide](https://dax.guide/ddb/)
- **DISC** — DISC 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/disc-function-dax) · [DAX Guide](https://dax.guide/disc/)
- **DOLLARDE** — DOLLARDE 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/dollarde-function-dax) · [DAX Guide](https://dax.guide/dollarde/)
- **DOLLARFR** — DOLLARFR 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/dollarfr-function-dax) · [DAX Guide](https://dax.guide/dollarfr/)
- **EFFECT** — EFFECT 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/effect-function-dax) · [DAX Guide](https://dax.guide/effect/)
- **FV** — FV 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/fv-function-dax) · [DAX Guide](https://dax.guide/fv/)
- **INTRATE** — INTRATE 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/intrate-function-dax) · [DAX Guide](https://dax.guide/intrate/)
- **IPMT** — IPMT 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/ipmt-function-dax) · [DAX Guide](https://dax.guide/ipmt/)
- **ISPMT** — ISPMT 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/ispmt-function-dax) · [DAX Guide](https://dax.guide/ispmt/)
- **MDURATION** — MDURATION 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/mduration-function-dax) · [DAX Guide](https://dax.guide/mduration/)
- **NOMINAL** — NOMINAL 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/nominal-function-dax) · [DAX Guide](https://dax.guide/nominal/)
- **NPER** — NPER 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/nper-function-dax) · [DAX Guide](https://dax.guide/nper/)
- **ODDFPRICE** — ODDFPRICE 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/oddfprice-function-dax) · [DAX Guide](https://dax.guide/oddfprice/)
- **ODDFYIELD** — ODDFYIELD 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/oddfyield-function-dax) · [DAX Guide](https://dax.guide/oddfyield/)
- **ODDLPRICE** — ODDLPRICE 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/oddlprice-function-dax) · [DAX Guide](https://dax.guide/oddlprice/)
- **ODDLYIELD** — ODDLYIELD 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/oddlyield-function-dax) · [DAX Guide](https://dax.guide/oddlyield/)
- **PDURATION** — PDURATION 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/pduration-function-dax) · [DAX Guide](https://dax.guide/pduration/)
- **PMT** — PMT 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/pmt-function-dax) · [DAX Guide](https://dax.guide/pmt/)
- **PPMT** — PPMT 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/ppmt-function-dax) · [DAX Guide](https://dax.guide/ppmt/)
- **PRICE** — PRICE 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/price-function-dax) · [DAX Guide](https://dax.guide/price/)
- **PRICEDISC** — PRICEDISC 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/pricedisc-function-dax) · [DAX Guide](https://dax.guide/pricedisc/)
- **PRICEMAT** — PRICEMAT 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/pricemat-function-dax) · [DAX Guide](https://dax.guide/pricemat/)
- **PV** — PV 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/pv-function-dax) · [DAX Guide](https://dax.guide/pv/)
- **RATE** — RATE 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/rate-function-dax) · [DAX Guide](https://dax.guide/rate/)
- **RECEIVED** — RECEIVED 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/received-function-dax) · [DAX Guide](https://dax.guide/received/)
- **RRI** — RRI 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/rri-function-dax) · [DAX Guide](https://dax.guide/rri/)
- **SLN** — SLN 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/sln-function-dax) · [DAX Guide](https://dax.guide/sln/)
- **SYD** — SYD 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/syd-function-dax) · [DAX Guide](https://dax.guide/syd/)
- **TBILLEQ** — TBILLEQ 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/tbilleq-function-dax) · [DAX Guide](https://dax.guide/tbilleq/)
- **TBILLPRICE** — TBILLPRICE 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/tbillprice-function-dax) · [DAX Guide](https://dax.guide/tbillprice/)
- **TBILLYIELD** — TBILLYIELD 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/tbillyield-function-dax) · [DAX Guide](https://dax.guide/tbillyield/)
- **VDB** — VDB 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/vdb-function-dax) · [DAX Guide](https://dax.guide/vdb/)
- **XIRR** — XIRR 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/xirr-function-dax) · [DAX Guide](https://dax.guide/xirr/)
- **XNPV** — XNPV 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/xnpv-function-dax) · [DAX Guide](https://dax.guide/xnpv/)
- **YIELD** — YIELD 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/yield-function-dax) · [DAX Guide](https://dax.guide/yield/)
- **YIELDDISC** — YIELDDISC 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/yielddisc-function-dax) · [DAX Guide](https://dax.guide/yielddisc/)
- **YIELDMAT** — YIELDMAT 재무 함수. Excel 계열 재무 공식과 동일한 모델. [Learn](https://learn.microsoft.com/en-us/dax/yieldmat-function-dax) · [DAX Guide](https://dax.guide/yieldmat/)

#### 부모-자식(Parent-Child) (5개)

- **PATH** — PATH 부모-자식 경로 함수. 관계 대신 경로 문자열로 계층을 표현한다. [Learn](https://learn.microsoft.com/en-us/dax/path-function-dax) · [DAX Guide](https://dax.guide/path/)
- **PATHCONTAINS** — PATHCONTAINS 부모-자식 경로 함수. 관계 대신 경로 문자열로 계층을 표현한다. [Learn](https://learn.microsoft.com/en-us/dax/pathcontains-function-dax) · [DAX Guide](https://dax.guide/pathcontains/)
- **PATHITEM** — PATHITEM 부모-자식 경로 함수. 관계 대신 경로 문자열로 계층을 표현한다. [Learn](https://learn.microsoft.com/en-us/dax/pathitem-function-dax) · [DAX Guide](https://dax.guide/pathitem/)
- **PATHITEMREVERSE** — PATHITEMREVERSE 부모-자식 경로 함수. 관계 대신 경로 문자열로 계층을 표현한다. [Learn](https://learn.microsoft.com/en-us/dax/pathitemreverse-function-dax) · [DAX Guide](https://dax.guide/pathitemreverse/)
- **PATHLENGTH** — PATHLENGTH 부모-자식 경로 함수. 관계 대신 경로 문자열로 계층을 표현한다. [Learn](https://learn.microsoft.com/en-us/dax/pathlength-function-dax) · [DAX Guide](https://dax.guide/pathlength/)

#### 기타(Other) (4개)

- **CONTAINS** — CONTAINS 함수. 세부 동작은 Learn 문서를 따른다. [Learn](https://learn.microsoft.com/en-us/dax/contains-function-dax) · [DAX Guide](https://dax.guide/contains/)
- **CONTAINSROW** — CONTAINSROW 함수. 세부 동작은 Learn 문서를 따른다. [Learn](https://learn.microsoft.com/en-us/dax/containsrow-function-dax) · [DAX Guide](https://dax.guide/containsrow/)
- **CONTAINSSTRING** — CONTAINSSTRING 함수. 세부 동작은 Learn 문서를 따른다. [Learn](https://learn.microsoft.com/en-us/dax/containsstring-function-dax) · [DAX Guide](https://dax.guide/containsstring/)
- **CONTAINSSTRINGEXACT** — CONTAINSSTRINGEXACT 함수. 세부 동작은 Learn 문서를 따른다. [Learn](https://learn.microsoft.com/en-us/dax/containsstringexact-function-dax) · [DAX Guide](https://dax.guide/containsstringexact/)

_총 409개 DAX 함수 색인(그 중 143개는 D.1 심층 예제를 제공)._

<!-- annotation: M appendix generated by scripts/generate_power_bi_dax_m_appendices.py -->

---

## 이 시리즈의 다른 글

- [← 본문 가이드](/paper_review/studies/20260420-power-bi-desktop-guide/)
- [부록 E — M](/paper_review/studies/20260420-power-bi-m-reference/)
- [부록 F — 체크리스트](/paper_review/studies/20260420-power-bi-review-checklist/)
