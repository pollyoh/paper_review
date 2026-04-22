"""Curated DAX function catalog for the Power BI report appendix.

Contains three data structures:

- `CATEGORY_ORDER`: ordered list of category labels used in the appendix.
- `CATEGORY`: maps every known DAX slug (from dax.guide) to one category label.
- `DETAILED`: rich input/output examples for the most important ~100 functions.

Examples are intentionally minimal and self-contained so a reader can paste
them into Power BI Desktop against the sample model documented at the top of
appendix D (Sales, 'Date', Product).
"""

from __future__ import annotations

from typing import TypedDict


class Example(TypedDict, total=False):
    sig: str  # signature
    summary: str  # one-line purpose in Korean
    ctx: str  # optional: required context
    code: str  # DAX formula body (without leading measure name)
    call: str  # optional: how it is wired (measure/calc table)
    data: str  # optional: short note on input data precondition
    output: str  # expected return value or returned table sketch
    note: str  # optional: pitfalls / caveats


CATEGORY_ORDER: list[str] = [
    "집계(Aggregation)",
    "논리(Logical)",
    "필터(Filter)",
    "관계(Relationships)",
    "테이블(Table)",
    "시간 인텔리전스(Time Intelligence)",
    "날짜·시간(Date & Time)",
    "텍스트(Text)",
    "수학·삼각(Math & Trig)",
    "통계(Statistical)",
    "정보(Information)",
    "재무(Financial)",
    "부모-자식(Parent-Child)",
    "기타(Other)",
]


CATEGORY: dict[str, str] = {
    # Aggregation
    **{s: "집계(Aggregation)" for s in [
        "sum", "sumx", "average", "averagea", "averagex",
        "min", "mina", "minx", "max", "maxa", "maxx",
        "count", "counta", "countax", "countblank", "countrows", "countx",
        "distinctcount", "distinctcountnoblank", "approximatedistinctcount",
        "product", "productx",
    ]},
    # Logical
    **{s: "논리(Logical)" for s in [
        "and", "or", "not", "true", "false",
        "if", "if-eager", "iferror", "switch", "coalesce",
    ]},
    # Filter
    **{s: "필터(Filter)" for s in [
        "calculate", "calculatetable",
        "all", "allcrossfiltered", "allexcept", "allnoblankrow",
        "allselected", "allselectedapply", "allselectedremove", "alwaysapply",
        "filter", "filtercluster", "filters",
        "hasonefilter", "hasonevalue",
        "iscrossfiltered", "isfiltered",
        "keepfilters", "removefilters",
        "selectedvalue", "lookupvalue", "lookupwithtotals",
        "userelationship", "crossfilter", "treatas",
        "index", "offset", "orderby", "partitionby",
        "rank", "rownumber", "window", "matchby",
        "ignore", "nonvisual", "nonfilter", "shadowcluster",
    ]},
    # Relationships
    **{s: "관계(Relationships)" for s in [
        "related", "relatedtable",
    ]},
    # Table
    **{s: "테이블(Table)" for s in [
        "addcolumns", "addmissingitems", "selectcolumns", "summarize",
        "summarizecolumns", "row", "datatable",
        "union", "intersect", "except", "crossjoin",
        "distinct", "values", "topn", "topnperlevel", "topnskip",
        "generate", "generateall", "generateseries",
        "groupby", "currentgroup", "groupcrossapply", "groupcrossapplytable",
        "naturalinnerjoin", "naturalleftouterjoin", "naturaljoinusage",
        "substitutewithindex", "rollup", "rollupaddissubtotal", "rollupgroup", "rollupissubtotal",
        "collapse", "collapseall", "expand", "expandall",
        "detailrows", "tableof", "nameof", "externalmeasure",
        "first", "last", "next", "previous", "range",
        "earlier", "earliest",
    ]},
    # Time intelligence
    **{s: "시간 인텔리전스(Time Intelligence)" for s in [
        "calendar", "calendarauto",
        "dateadd", "datesbetween", "datesinperiod",
        "datesmtd", "datesqtd", "datesytd", "dateswtd",
        "sameperiodlastyear", "parallelperiod",
        "previousday", "previousmonth", "previousquarter", "previousweek", "previousyear",
        "nextday", "nextmonth", "nextquarter", "nextweek", "nextyear",
        "startofmonth", "startofquarter", "startofweek", "startofyear",
        "endofmonth", "endofquarter", "endofweek", "endofyear",
        "firstdate", "lastdate", "firstnonblank", "lastnonblank",
        "firstnonblankvalue", "lastnonblankvalue",
        "openingbalancemonth", "openingbalancequarter", "openingbalanceweek", "openingbalanceyear",
        "closingbalancemonth", "closingbalancequarter", "closingbalanceweek", "closingbalanceyear",
        "totalmtd", "totalqtd", "totalwtd", "totalytd",
    ]},
    # Date & Time
    **{s: "날짜·시간(Date & Time)" for s in [
        "date", "datediff", "datevalue",
        "day", "edate", "eomonth",
        "hour", "minute", "month", "now", "quarter", "second",
        "time", "timevalue", "today", "utcnow", "utctoday",
        "weekday", "weeknum", "year", "yearfrac",
        "networkdays", "duration",
    ]},
    # Text
    **{s: "텍스트(Text)" for s in [
        "concatenate", "concatenatex", "combinevalues",
        "exact", "find", "fixed", "format", "left", "len",
        "lower", "mid", "replace", "rept", "right", "search",
        "substitute", "trim", "unichar", "unicode", "upper",
        "value", "tocsv", "tojson", "hash", "keywordmatch",
    ]},
    # Math & Trig
    **{s: "수학·삼각(Math & Trig)" for s in [
        "abs", "acos", "acosh", "acot", "acoth", "asin", "asinh",
        "atan", "atanh", "ceiling", "combin", "combina",
        "convert", "cos", "cosh", "cot", "coth", "currency",
        "degrees", "divide", "even", "exp", "fact", "floor",
        "gcd", "int", "iso-ceiling", "lcm", "ln", "log", "log10",
        "mod", "mround", "odd", "permut", "pi", "power",
        "quotient", "radians", "rand", "randbetween",
        "round", "rounddown", "roundup", "sign", "sin", "sinh",
        "sqrt", "sqrtpi", "tan", "tanh", "trunc",
        "bitand", "bitlshift", "bitor", "bitrshift", "bitxor",
        "runningsum", "movingaverage",
    ]},
    # Statistical
    **{s: "통계(Statistical)" for s in [
        "beta-dist", "beta-inv", "chisq-dist", "chisq-dist-rt",
        "chisq-inv", "chisq-inv-rt", "confidence-norm", "confidence-t",
        "expon-dist", "geomean", "geomeanx", "linest", "linestx",
        "median", "medianx", "norm-dist", "norm-inv", "norm-s-dist", "norm-s-inv",
        "percentile-exc", "percentile-inc", "percentilex-exc", "percentilex-inc",
        "poisson-dist", "rank-eq", "rankx", "sample", "sampleaxiswithlocalminmax",
        "samplecartesianpointsbycover",
        "stdev-p", "stdev-s", "stdevx-p", "stdevx-s",
        "t-dist", "t-dist-2t", "t-dist-rt", "t-inv", "t-inv-2t",
        "var-p", "var-s", "varx-p", "varx-s",
    ]},
    # Information
    **{s: "정보(Information)" for s in [
        "blank", "columnstatistics", "customdata",
        "error", "evaluateandlog",
        "hasonevalue_dup_marker_not_used",
        "isafter", "isatlevel", "isblank",
        "isboolean", "iscurrency", "isdatetime", "isdecimal",
        "isdouble", "isempty", "iserror", "iseven", "isint64",
        "isinteger", "islogical", "isnontext", "isnumber", "isnumeric",
        "isodd", "isonorafter", "isselectedmeasure", "isstring",
        "issubtotal", "istext", "isfiltered_dup_marker_not_used",
        "isinscope",
        "lookup",
        "selectedmeasure", "selectedmeasureformatstring", "selectedmeasurename",
        "userculture", "username", "userobjectid", "userprincipalname",
    ]},
    # Financial
    **{s: "재무(Financial)" for s in [
        "accrint", "accrintm", "amordegrc", "amorlinc",
        "coupdaybs", "coupdays", "coupdaysnc", "coupncd", "coupnum", "couppcd",
        "cumipmt", "cumprinc",
        "db", "ddb", "disc", "dollarde", "dollarfr",
        "effect", "fv", "intrate", "ipmt", "ispmt",
        "mduration", "nominal", "nper", "oddfprice", "oddfyield",
        "oddlprice", "oddlyield", "pduration", "pmt", "ppmt",
        "price", "pricedisc", "pricemat", "pv", "rate", "received",
        "rri", "sln", "syd",
        "tbilleq", "tbillprice", "tbillyield",
        "vdb", "xirr", "xnpv", "yield", "yielddisc", "yieldmat",
        "ispmt_alt_not_used",
        "containsstring_dup_not_used",
    ]},
    # Parent-Child
    **{s: "부모-자식(Parent-Child)" for s in [
        "path", "pathcontains", "pathitem", "pathitemreverse", "pathlength",
    ]},
    # Other / misc (catch-all for rare or engine-internal slugs)
    **{s: "기타(Other)" for s in [
        "contains", "containsrow", "containsstring", "containsstringexact",
    ]},
}


# ---------------------------------------------------------------------------
# Detailed input/output examples for the most important functions.
# Each entry targets the sample model described in appendix D preamble.
# ---------------------------------------------------------------------------

DETAILED: dict[str, Example] = {
    # -------------- Aggregation --------------
    "sum": {
        "sig": "SUM(<column>)",
        "summary": "한 숫자 열의 모든 값을 단순 합계한다. 내부적으로 `SUMX(VALUES(...), ...)`에 가깝게 동작하며 필터 컨텍스트를 존중한다.",
        "code": "[Total Amount] = SUM(Sales[Amount])",
        "data": "`Sales[Amount]` = { 100, 200, 300 }",
        "output": "600",
        "note": "빈(BLANK) 값은 무시, 비숫자가 섞이면 오류. 문자열 형태 숫자는 자동 변환되지 않는다.",
    },
    "sumx": {
        "sig": "SUMX(<table>, <expression>)",
        "summary": "테이블의 각 행에 식을 평가한 뒤 결과를 합산하는 행 반복 함수(iterator). 각 행이 **행 컨텍스트**를 만든다.",
        "code": "[Revenue] = SUMX(Sales, Sales[Qty] * Sales[UnitPrice])",
        "data": "Sales = { (Qty=2, UnitPrice=10), (Qty=3, UnitPrice=20) }",
        "output": "2*10 + 3*20 = 80",
        "note": "행 컨텍스트에서 다른 테이블 열을 참조하려면 `RELATED`가 필요하다.",
    },
    "average": {
        "sig": "AVERAGE(<column>)",
        "summary": "숫자 열의 산술 평균을 계산한다.",
        "code": "[Avg Amount] = AVERAGE(Sales[Amount])",
        "data": "`Sales[Amount]` = { 100, 200, 300 }",
        "output": "200",
        "note": "빈 값은 **개수에서 제외**된다. 0이 포함되면 평균이 달라진다.",
    },
    "averagex": {
        "sig": "AVERAGEX(<table>, <expression>)",
        "summary": "테이블의 각 행에 식을 평가해 평균을 낸다. 식 내부에서 행 간 곱셈·비교가 필요한 경우에 쓴다.",
        "code": "[Avg Line Revenue] = AVERAGEX(Sales, Sales[Qty] * Sales[UnitPrice])",
        "data": "Sales = { (Qty=2, UnitPrice=10), (Qty=3, UnitPrice=20) }",
        "output": "(20 + 60) / 2 = 40",
    },
    "min": {
        "sig": "MIN(<column>)",
        "summary": "숫자·날짜 열의 최솟값을 반환한다.",
        "code": "[First Order] = MIN(Sales[OrderDate])",
        "data": "Sales[OrderDate] 최솟값이 2026-01-03",
        "output": "2026-01-03",
    },
    "max": {
        "sig": "MAX(<column>)",
        "summary": "숫자·날짜 열의 최댓값을 반환한다.",
        "code": "[Latest Order] = MAX(Sales[OrderDate])",
        "output": "2026-04-20",
    },
    "minx": {
        "sig": "MINX(<table>, <expression>)",
        "summary": "각 행에서 평가한 식의 최솟값을 돌려주는 행 반복 함수.",
        "code": "[Min Line Revenue] = MINX(Sales, Sales[Qty] * Sales[UnitPrice])",
        "data": "Sales = { (2, 10), (3, 20) } → 20, 60",
        "output": "20",
    },
    "maxx": {
        "sig": "MAXX(<table>, <expression>)",
        "summary": "각 행에서 평가한 식의 최댓값을 돌려주는 행 반복 함수.",
        "code": "[Max Line Revenue] = MAXX(Sales, Sales[Qty] * Sales[UnitPrice])",
        "output": "60",
    },
    "count": {
        "sig": "COUNT(<column>)",
        "summary": "숫자·날짜·논리 열에서 **비어 있지 않은 값의 개수**를 센다.",
        "code": "[Order Count] = COUNT(Sales[OrderId])",
        "data": "Sales 행 5개 중 OrderId BLANK 1개",
        "output": "4",
        "note": "텍스트 열에는 `COUNTA`를 쓴다.",
    },
    "counta": {
        "sig": "COUNTA(<column>)",
        "summary": "빈 값을 제외한 **모든 형식**의 값 개수를 센다. 텍스트 열에 유용.",
        "code": "[With Note] = COUNTA(Sales[Note])",
        "output": "Sales 5행 중 Note가 비어있지 않은 3행 → 3",
    },
    "countrows": {
        "sig": "COUNTROWS(<table>)",
        "summary": "테이블(또는 식의 결과 테이블) 행 수를 센다. 집계 중 가장 명확·빠른 함수.",
        "code": "[Sales Lines] = COUNTROWS(Sales)",
        "output": "예: 1204",
        "note": "`COUNT(Sales[OrderId])`는 빈 값을 빼지만 `COUNTROWS`는 BLANK 행도 포함한다.",
    },
    "countx": {
        "sig": "COUNTX(<table>, <expression>)",
        "summary": "식이 비어 있지 않은 행의 수를 센다. 필터 조건을 카운트로 표현할 때 쓴다.",
        "code": "[Big Orders] = COUNTX(Sales, IF(Sales[Amount] > 1000, 1))",
        "output": "Amount > 1000 인 행의 수",
    },
    "distinctcount": {
        "sig": "DISTINCTCOUNT(<column>)",
        "summary": "열의 **고유 값 수**(BLANK 포함).",
        "code": "[Customers] = DISTINCTCOUNT(Sales[CustomerId])",
        "output": "예: 57",
        "note": "BLANK를 세고 싶지 않으면 `DISTINCTCOUNTNOBLANK`.",
    },
    "distinctcountnoblank": {
        "sig": "DISTINCTCOUNTNOBLANK(<column>)",
        "summary": "열의 고유 값 수에서 BLANK를 제외한다.",
        "code": "[Customers (no blank)] = DISTINCTCOUNTNOBLANK(Sales[CustomerId])",
        "output": "예: 56",
    },
    "countblank": {
        "sig": "COUNTBLANK(<column>)",
        "summary": "열에서 BLANK(공란)의 개수를 센다. 데이터 품질 측정에 유용.",
        "code": "[Missing Email] = COUNTBLANK(Customer[Email])",
        "output": "빈 이메일 행 수",
    },
    "productx": {
        "sig": "PRODUCTX(<table>, <expression>)",
        "summary": "각 행에서 평가한 식의 **곱**을 반환한다(복합 성장률 등에 사용).",
        "code": "[Compound Growth] = PRODUCTX('Growth', 1 + 'Growth'[Rate]) - 1",
    },

    # -------------- Logical --------------
    "if": {
        "sig": "IF(<logical>, <value_if_true>, [<value_if_false>])",
        "summary": "조건이 참이면 첫 값을, 아니면 둘째 값을 반환. 셋째 인수 생략 시 BLANK.",
        "code": "[Segment] = IF(Sales[Amount] >= 1000, \"High\", \"Low\")",
        "data": "Amount=1500 행 → \"High\", Amount=200 행 → \"Low\"",
        "output": "각 행마다 문자열 라벨",
        "note": "반환 타입이 두 가지면 두 분기의 데이터 형이 일치해야 예측 가능한 결과가 나온다. 복잡한 분기에는 `SWITCH`가 좋다.",
    },
    "iferror": {
        "sig": "IFERROR(<value>, <value_if_error>)",
        "summary": "첫 식이 오류를 발생시키면 두 번째 식을 대신 반환한다.",
        "code": "[Ratio Safe] = IFERROR(DIVIDE(Sales[Amount], Sales[Qty]), 0)",
        "output": "Qty=0인 행에서도 오류 대신 0",
        "note": "가능하면 `DIVIDE` 자체의 오류 방지를 먼저 쓰는 것이 빠르다.",
    },
    "switch": {
        "sig": "SWITCH(<expression>, <v1>, <r1>, [v2, r2, ...], [<else>])",
        "summary": "식 결과와 값 목록을 차례로 비교해 일치하는 결과를 돌려준다. `SWITCH(TRUE(), ...)` 패턴으로 다중 조건 분기에도 사용.",
        "code": "[Grade] = SWITCH(TRUE(), [Score] >= 90, \"A\", [Score] >= 80, \"B\", \"C\")",
        "output": "점수별 A/B/C",
    },
    "and": {
        "sig": "AND(<logical1>, <logical2>)",
        "summary": "두 식이 모두 TRUE면 TRUE. 연산자 `&&`와 동일하며 두 개 이상에는 `&&`가 가독성이 좋다.",
        "code": "IF(AND(Sales[Amount] > 1000, Sales[Qty] > 10), \"VIP\", \"\")",
    },
    "or": {
        "sig": "OR(<logical1>, <logical2>)",
        "summary": "둘 중 하나만 TRUE면 TRUE. 연산자 `||`와 동일.",
        "code": "IF(OR(Customer[Country]=\"KR\", Customer[Country]=\"JP\"), 1, 0)",
    },
    "not": {
        "sig": "NOT(<logical>)",
        "summary": "논리값을 뒤집는다.",
        "code": "FILTER(Sales, NOT(ISBLANK(Sales[Discount])))",
    },
    "true": {
        "sig": "TRUE()",
        "summary": "상수 TRUE. `SWITCH(TRUE(), ...)` 패턴에 자주 쓴다.",
    },
    "false": {
        "sig": "FALSE()",
        "summary": "상수 FALSE.",
    },
    "coalesce": {
        "sig": "COALESCE(<value1>, <value2>, ...)",
        "summary": "첫 번째 **비-BLANK** 값을 반환한다. `IF(ISBLANK(x), y, x)`의 간결한 대안.",
        "code": "[Revenue Safe] = COALESCE(SUM(Sales[Amount]), 0)",
        "output": "빈 필터에서 BLANK 대신 0",
    },

    # -------------- Filter --------------
    "calculate": {
        "sig": "CALCULATE(<expression>, [<filter1>, <filter2>, ...])",
        "summary": "식을 **변경된 필터 컨텍스트**에서 평가한다. DAX에서 가장 중요한 함수이며, 행 컨텍스트를 필터 컨텍스트로 **컨텍스트 전환**하는 역할도 한다.",
        "code": "[Sales KR] = CALCULATE(SUM(Sales[Amount]), Customer[Country] = \"KR\")",
        "output": "전체 Amount 1,000,000 중 KR 고객분 230,000",
        "note": "암시적 필터 인수는 자동으로 `FILTER(ALL(table), ...)` 로 변환된다. 기존 필터를 유지하려면 `KEEPFILTERS(...)`를 감싼다.",
    },
    "calculatetable": {
        "sig": "CALCULATETABLE(<table_expr>, [<filter1>, ...])",
        "summary": "`CALCULATE`의 테이블 반환 버전. 변경된 컨텍스트에서 테이블을 돌려준다.",
        "code": "Top Customers KR = CALCULATETABLE(TOPN(10, Customer, [Revenue]), Customer[Country]=\"KR\")",
        "output": "KR 고객 중 매출 상위 10행 테이블",
    },
    "filter": {
        "sig": "FILTER(<table>, <condition>)",
        "summary": "테이블에서 조건을 만족하는 **행만** 남긴다. `CALCULATE`의 부울식 필터보다 복잡한 조건을 쓸 때 사용.",
        "code": "[High Qty Sales] = CALCULATE(SUM(Sales[Amount]), FILTER(Sales, Sales[Qty] > 10))",
        "output": "Qty>10인 행만의 Amount 합",
        "note": "`FILTER(ALL(Sales), ...)` 처럼 `ALL`과 자주 조합해 “모든 행 중 조건”을 만든다.",
    },
    "all": {
        "sig": "ALL([<table> | <column>[, <column>, ...]])",
        "summary": "지정한 테이블 또는 열의 **필터를 제거**한 테이블을 돌려준다. `CALCULATE`의 필터 인수로 넣어 컨텍스트를 무시한다.",
        "code": "[Total (All Years)] = CALCULATE(SUM(Sales[Amount]), ALL('Date'))",
        "output": "슬라이서·열 필터 무관 연도 합계",
    },
    "allexcept": {
        "sig": "ALLEXCEPT(<table>, <column1>[, <column2>, ...])",
        "summary": "지정한 열 **외에는** 전부 필터 제거. 상위 총계 비율 계산 시 표준 패턴.",
        "code": "[% of Country] = DIVIDE([Sales], CALCULATE([Sales], ALLEXCEPT(Customer, Customer[Country])))",
        "output": "각 행이 속한 국가 내 비중",
    },
    "allselected": {
        "sig": "ALLSELECTED([<table_or_column>])",
        "summary": "**시각적 개체 외부 필터**(슬라이서·페이지 필터)는 유지하고, **내부 좌표 축 필터**만 제거한다. “보이는 데이터 대비 비율”을 구할 때 쓴다.",
        "code": "[% Visible] = DIVIDE([Sales], CALCULATE([Sales], ALLSELECTED(Sales)))",
    },
    "removefilters": {
        "sig": "REMOVEFILTERS([<table> | <column>[, ...]])",
        "summary": "`CALCULATE`의 **수식 한정 필터 인수**로 설계된 `ALL`의 명시적 대안. 필터만 제거하고 테이블을 반환하지 않는다.",
        "code": "[Grand Total] = CALCULATE([Sales], REMOVEFILTERS())",
    },
    "keepfilters": {
        "sig": "KEEPFILTERS(<expression>)",
        "summary": "`CALCULATE`의 필터 인수를 감싸, 같은 열의 기존 필터를 **대체하지 않고 교집합**으로 적용한다.",
        "code": "[Sales HE] = CALCULATE([Sales], KEEPFILTERS(Product[Color] = \"Red\"))",
        "output": "기존 슬라이서로 고른 색 중 Red도 포함된 행만",
    },
    "selectedvalue": {
        "sig": "SELECTEDVALUE(<column>[, <alternate>])",
        "summary": "현재 필터 컨텍스트에서 열에 **정확히 하나**의 값만 있으면 그 값, 아니면 대체 값(기본 BLANK)을 돌려준다.",
        "code": "[Current Country] = SELECTEDVALUE(Customer[Country], \"(여러 국가)\")",
    },
    "hasonevalue": {
        "sig": "HASONEVALUE(<column>)",
        "summary": "열이 정확히 1개 값으로 필터되어 있으면 TRUE.",
        "code": "IF(HASONEVALUE('Date'[Year]), [YoY], BLANK())",
    },
    "hasonefilter": {
        "sig": "HASONEFILTER(<column>)",
        "summary": "열에 **필터 자체가 1개**인지 확인한다(값이 1개와는 미묘하게 다르다).",
    },
    "isfiltered": {
        "sig": "ISFILTERED(<table_or_column>)",
        "summary": "직접 필터가 걸려 있는지 검사.",
    },
    "iscrossfiltered": {
        "sig": "ISCROSSFILTERED(<table_or_column>)",
        "summary": "다른 테이블의 관계 경로로 **교차 필터**되어 있는지 검사.",
    },
    "userelationship": {
        "sig": "USERELATIONSHIP(<col1>, <col2>)",
        "summary": "`CALCULATE`의 수식 한정 인수. **비활성 관계**를 이번 평가에만 활성화한다.",
        "code": "[Sales by Ship Date] = CALCULATE([Sales], USERELATIONSHIP(Sales[ShipDate], 'Date'[Date]))",
        "note": "비활성 관계가 이미 모델 뷰에 정의되어 있어야 동작한다.",
    },
    "crossfilter": {
        "sig": "CROSSFILTER(<col1>, <col2>, <direction>)",
        "summary": "특정 계산에서만 관계의 교차 필터 방향을 바꾼다. `None`/`OneWay`/`Both`.",
    },
    "treatas": {
        "sig": "TREATAS(<expression>, <column>[, <column>, ...])",
        "summary": "**관계가 없는** 테이블 간에도 열 값을 필터로 **가상 연결**한다.",
        "code": "VAR kr_ids = VALUES(Customer[Id]) RETURN CALCULATE([Sales Foreign], TREATAS(kr_ids, Foreign[CustId]))",
    },
    "lookupvalue": {
        "sig": "LOOKUPVALUE(<result_col>, <search_col1>, <search_value1>[, ...])",
        "summary": "조건을 만족하는 **단일 행**의 값을 돌려준다. 관계가 없을 때도 동작.",
        "code": "[Country] = LOOKUPVALUE(Customer[Country], Customer[Id], Sales[CustomerId])",
        "note": "여러 행이 일치하면 오류. 네 번째 인수로 대체 값을 지정할 수 있다.",
    },

    # -------------- Relationships --------------
    "related": {
        "sig": "RELATED(<column>)",
        "summary": "현재 **행 컨텍스트**에서 관계의 ‘1’ 쪽 테이블의 열 값을 가져온다. 계산 열과 이터레이터 안에서 사용.",
        "code": "Sales[Country] = RELATED(Customer[Country])",
        "output": "각 Sales 행에 고객 국가 값 추가",
    },
    "relatedtable": {
        "sig": "RELATEDTABLE(<table>)",
        "summary": "현재 행에 연결된 **다대일의 다(多)쪽** 테이블 서브셋을 반환한다.",
        "code": "Customer[Orders Count] = COUNTROWS(RELATEDTABLE(Sales))",
    },

    # -------------- Table --------------
    "addcolumns": {
        "sig": "ADDCOLUMNS(<table>, <name1>, <expr1>[, ...])",
        "summary": "테이블에 계산 열을 추가한 **새 테이블**을 반환한다. 시각화에 직접 보이는 계산 테이블 생성에 사용.",
        "code": "EVALUATE ADDCOLUMNS(VALUES(Customer[Country]), \"Sales\", [Total Sales])",
        "output": "국가 | Sales 두 열의 테이블",
    },
    "selectcolumns": {
        "sig": "SELECTCOLUMNS(<table>, <name1>, <expr1>[, ...])",
        "summary": "입력 테이블에서 원하는 열만 골라 **새 이름으로 투영**한다.",
        "code": "SELECTCOLUMNS(Customer, \"Cust\", Customer[Name], \"Country\", Customer[Country])",
    },
    "summarize": {
        "sig": "SUMMARIZE(<table>, <groupBy_col1>[, ...][, <name>, <expr>[, ...]])",
        "summary": "그룹화 열로 집계한 표를 만든다. 단순 그룹화 용도로는 `SUMMARIZECOLUMNS`가 더 안전하다.",
        "code": "SUMMARIZE(Sales, Customer[Country], \"Sales\", SUM(Sales[Amount]))",
    },
    "summarizecolumns": {
        "sig": "SUMMARIZECOLUMNS(<groupBy_col1>[, ...][, <filter>][, <name>, <expr>[, ...]])",
        "summary": "`SUMMARIZE`를 단순화한 버전. 필터·그룹·측정값을 한 번에 쓸 수 있어 쿼리·계산 테이블의 **표준 집계 함수**이다.",
        "code": "SUMMARIZECOLUMNS(Customer[Country], 'Date'[Year], \"Sales\", [Total Sales])",
    },
    "values": {
        "sig": "VALUES(<table_or_column>)",
        "summary": "열의 **고유 값 테이블** 또는 테이블의 고유 행 테이블을 반환. 필터 컨텍스트를 존중한다.",
        "code": "COUNTROWS(VALUES(Customer[Country]))",
    },
    "distinct": {
        "sig": "DISTINCT(<table_or_column>)",
        "summary": "BLANK를 포함해 **중복을 제거**한 테이블/열 값을 반환. `VALUES`와 달리 모델에 의해 자동 추가되는 빈 행(관계 위반)을 포함하지 않는다.",
    },
    "row": {
        "sig": "ROW(<name1>, <expr1>[, ...])",
        "summary": "한 줄짜리 테이블을 만든다. 대시보드의 KPI 요약 테이블 생성에 유용.",
        "code": "EVALUATE ROW(\"Sales\", [Total Sales], \"Customers\", [Customer Count])",
    },
    "datatable": {
        "sig": "DATATABLE(<col1_name>, <col1_type>, ..., {{<row1>}, ...})",
        "summary": "DAX 내부에서 **정적 데이터 테이블**을 정의한다. 룩업 상수 테이블에 쓰인다.",
        "code": "DATATABLE(\"Grade\", STRING, \"Min\", INTEGER, {{\"A\", 90}, {\"B\", 80}})",
    },
    "topn": {
        "sig": "TOPN(<n>, <table>, [<orderBy>, [<order>]...])",
        "summary": "정렬 기준으로 상위 N개 행을 반환한다. 동률 포함.",
        "code": "TOPN(10, Customer, [Sales], DESC)",
    },
    "union": {
        "sig": "UNION(<table1>, <table2>[, ...])",
        "summary": "같은 열 구조를 가진 테이블들을 **세로로 결합**한다. 중복 유지.",
    },
    "intersect": {
        "sig": "INTERSECT(<table1>, <table2>)",
        "summary": "두 테이블의 **교집합**을 반환(왼쪽 테이블의 열 이름 사용).",
    },
    "except": {
        "sig": "EXCEPT(<table1>, <table2>)",
        "summary": "`<table1>`에서 `<table2>`의 행을 뺀 차집합.",
    },
    "crossjoin": {
        "sig": "CROSSJOIN(<table1>, <table2>[, ...])",
        "summary": "모든 행의 카르테시안 곱.",
    },
    "generate": {
        "sig": "GENERATE(<table1>, <table2_expr>)",
        "summary": "왼쪽 테이블의 각 행마다 오른쪽 식을 평가해 **조인** 하듯 결합. 오른쪽이 빈 테이블이면 행이 제외된다.",
    },
    "generateall": {
        "sig": "GENERATEALL(<table1>, <table2_expr>)",
        "summary": "`GENERATE`와 유사하나 오른쪽이 비어도 왼쪽 행은 NULL과 함께 남긴다(왼쪽 외부 조인).",
    },
    "generateseries": {
        "sig": "GENERATESERIES(<start>, <end>[, <increment>])",
        "summary": "시작/끝/간격으로 **숫자 시퀀스 테이블**을 만든다. 파라미터 슬라이서용.",
        "code": "GENERATESERIES(0, 100, 10)",
        "output": "Value 열 { 0, 10, 20, ..., 100 }",
    },
    "naturalleftouterjoin": {
        "sig": "NATURALLEFTOUTERJOIN(<table1>, <table2>)",
        "summary": "공통 관계·이름으로 **좌외부 조인**한 표.",
    },
    "naturalinnerjoin": {
        "sig": "NATURALINNERJOIN(<table1>, <table2>)",
        "summary": "공통 관계·이름으로 **내부 조인**한 표.",
    },
    "groupby": {
        "sig": "GROUPBY(<table>, <groupCol1>[, ...][, <name>, <expression>])",
        "summary": "`SUMMARIZE`의 확장. `CURRENTGROUP()`을 통해 집계 식 내부에서 그룹의 서브셋을 참조할 수 있다.",
        "code": "GROUPBY(Sales, Customer[Country], \"Qty\", SUMX(CURRENTGROUP(), Sales[Qty]))",
    },

    # -------------- Time Intelligence --------------
    "calendar": {
        "sig": "CALENDAR(<start_date>, <end_date>)",
        "summary": "지정 범위의 연속 날짜 테이블을 생성한다. 날짜 테이블 만들 때 기본.",
        "code": "DateTable = CALENDAR(DATE(2024,1,1), DATE(2026,12,31))",
        "output": "1096행 Date 열",
    },
    "calendarauto": {
        "sig": "CALENDARAUTO([<fiscal_year_end_month>])",
        "summary": "모델의 모든 날짜 열 범위를 탐지해 **자동으로** 연속 날짜 테이블을 만든다.",
    },
    "dateadd": {
        "sig": "DATEADD(<dates>, <number_of_intervals>, <interval>)",
        "summary": "날짜 열을 **연/분기/월/일 단위로 이동**시킨 날짜 테이블 반환. `<interval>` = YEAR/QUARTER/MONTH/DAY.",
        "code": "[Sales LY] = CALCULATE([Sales], DATEADD('Date'[Date], -1, YEAR))",
    },
    "sameperiodlastyear": {
        "sig": "SAMEPERIODLASTYEAR(<dates>)",
        "summary": "현재 필터된 날짜 구간을 **정확히 1년 전**으로 이동.",
        "code": "[Sales PY] = CALCULATE([Sales], SAMEPERIODLASTYEAR('Date'[Date]))",
    },
    "datesytd": {
        "sig": "DATESYTD(<dates>[, <year_end_date>])",
        "summary": "현재 필터 내 연초부터 오늘까지의 날짜 집합.",
        "code": "[Sales YTD] = CALCULATE([Sales], DATESYTD('Date'[Date]))",
    },
    "totalytd": {
        "sig": "TOTALYTD(<expression>, <dates>[, <filter>][, <year_end_date>])",
        "summary": "`CALCULATE([Sales], DATESYTD(...))`의 단축형. 빠르게 YTD 측정값을 만들 때 쓴다.",
        "code": "[Sales YTD] = TOTALYTD([Sales], 'Date'[Date])",
    },
    "datesbetween": {
        "sig": "DATESBETWEEN(<dates>, <start_date>, <end_date>)",
        "summary": "두 날짜 사이의 날짜 집합 테이블. 누적 합계·지연 기간 계산에 쓴다.",
        "code": "[Running Sales] = CALCULATE([Sales], DATESBETWEEN('Date'[Date], BLANK(), MAX('Date'[Date])))",
    },
    "datesinperiod": {
        "sig": "DATESINPERIOD(<dates>, <start_date>, <number_of_intervals>, <interval>)",
        "summary": "시작일로부터 N 단위 앞뒤 날짜를 반환.",
        "code": "[Last 3 Months] = CALCULATE([Sales], DATESINPERIOD('Date'[Date], MAX('Date'[Date]), -3, MONTH))",
    },
    "parallelperiod": {
        "sig": "PARALLELPERIOD(<dates>, <number>, <interval>)",
        "summary": "`DATEADD`와 유사하나 **전체 구간**(예: 한 달 전체)을 반환한다.",
    },
    "previousmonth": {
        "sig": "PREVIOUSMONTH(<dates>)",
        "summary": "현재 필터된 달의 **바로 이전 월 전체**를 반환.",
    },
    "startofmonth": {"sig": "STARTOFMONTH(<dates>)", "summary": "현재 필터 내 최소 날짜가 속한 **월의 첫날**을 반환."},
    "endofmonth": {"sig": "ENDOFMONTH(<dates>)", "summary": "현재 필터 내 최대 날짜가 속한 **월의 마지막 날**을 반환."},

    # -------------- Date & Time --------------
    "today": {"sig": "TODAY()", "summary": "오늘의 날짜(시각 없음).", "output": "2026-04-20"},
    "now": {"sig": "NOW()", "summary": "현재 날짜와 시각.", "output": "2026-04-20 13:42:05"},
    "date": {
        "sig": "DATE(<year>, <month>, <day>)",
        "summary": "세 숫자로부터 날짜 값을 생성.",
        "code": "DATE(2026, 4, 20)",
        "output": "2026-04-20",
    },
    "datediff": {
        "sig": "DATEDIFF(<start>, <end>, <interval>)",
        "summary": "두 날짜 사이의 간격을 지정 단위로 측정. `<interval>` = SECOND/MINUTE/HOUR/DAY/WEEK/MONTH/QUARTER/YEAR.",
        "code": "DATEDIFF(Sales[OrderDate], Sales[ShipDate], DAY)",
        "output": "배송 소요 일수",
    },
    "eomonth": {
        "sig": "EOMONTH(<start>, <months>)",
        "summary": "지정 월수만큼 이동한 월의 **마지막 날** 반환.",
        "code": "EOMONTH(DATE(2026,4,15), 0)",
        "output": "2026-04-30",
    },
    "edate": {
        "sig": "EDATE(<start>, <months>)",
        "summary": "월 단위로 날짜를 이동. `EOMONTH`의 임의 날짜 버전.",
    },
    "year": {"sig": "YEAR(<date>)", "summary": "날짜에서 연도(숫자) 추출."},
    "month": {"sig": "MONTH(<date>)", "summary": "날짜에서 월(1~12) 추출."},
    "day": {"sig": "DAY(<date>)", "summary": "날짜에서 일(1~31) 추출."},
    "weekday": {
        "sig": "WEEKDAY(<date>[, <return_type>])",
        "summary": "요일을 숫자로 반환. `return_type`에 따라 기준이 다름(1: 일=1).",
    },
    "weeknum": {"sig": "WEEKNUM(<date>[, <return_type>])", "summary": "해의 주 번호(1~54)."},
    "yearfrac": {"sig": "YEARFRAC(<start>, <end>[, <basis>])", "summary": "두 날짜의 연 단위 소수 차이."},

    # -------------- Text --------------
    "concatenate": {
        "sig": "CONCATENATE(<t1>, <t2>)",
        "summary": "두 문자열을 이어 붙인다. 연산자 `&`와 동일.",
        "code": "CONCATENATE(\"Hello \", \"World\")",
        "output": "\"Hello World\"",
    },
    "concatenatex": {
        "sig": "CONCATENATEX(<table>, <expression>[, <delimiter>[, <orderBy>[, <order>]]])",
        "summary": "각 행에 식을 평가하고 구분자로 이어 붙여 하나의 문자열 반환.",
        "code": "CONCATENATEX(TOPN(3, Customer, [Sales], DESC), Customer[Name], \", \")",
        "output": "\"Alice, Bob, Chan\"",
    },
    "combinevalues": {
        "sig": "COMBINEVALUES(<delimiter>, <expr1>, <expr2>[, ...])",
        "summary": "여러 값을 **키 구분자**로 합친다. 복합키 조인 준비 시 사용.",
        "code": "COMBINEVALUES(\"|\", Sales[Year], Sales[Month])",
    },
    "format": {
        "sig": "FORMAT(<value>, <format_string>[, <locale>])",
        "summary": "값을 지정한 서식 문자열로 **문자열**로 변환.",
        "code": "FORMAT(TODAY(), \"yyyy-MM-dd\")",
        "output": "\"2026-04-20\"",
        "note": "시각화 숫자 포맷과 달리 결과 타입이 문자열로 바뀌어 산술 집계에 바로 쓰기 어렵다.",
    },
    "left": {"sig": "LEFT(<text>, <num>)", "summary": "왼쪽에서 N자 문자열.", "code": "LEFT(\"ABCDE\", 2)", "output": "\"AB\""},
    "right": {"sig": "RIGHT(<text>, <num>)", "summary": "오른쪽에서 N자.", "code": "RIGHT(\"ABCDE\", 2)", "output": "\"DE\""},
    "mid": {"sig": "MID(<text>, <start>, <num>)", "summary": "지정 위치부터 N자.", "code": "MID(\"ABCDE\", 2, 3)", "output": "\"BCD\""},
    "len": {"sig": "LEN(<text>)", "summary": "문자열 길이.", "code": "LEN(\"Seoul\")", "output": "5"},
    "substitute": {
        "sig": "SUBSTITUTE(<text>, <old>, <new>[, <instance>])",
        "summary": "문자열에서 지정 패턴을 치환. N번째 발생만 바꿀 수 있음.",
        "code": "SUBSTITUTE(\"A-B-C\", \"-\", \"/\")",
        "output": "\"A/B/C\"",
    },
    "replace": {
        "sig": "REPLACE(<text>, <start>, <num>, <new_text>)",
        "summary": "지정 위치의 N자를 새 문자열로 바꾼다.",
        "code": "REPLACE(\"ABCDE\", 2, 2, \"XX\")",
        "output": "\"AXXDE\"",
    },
    "find": {
        "sig": "FIND(<find_text>, <within>[, <start>[, <if_not_found>]])",
        "summary": "대소문자 구분 위치 찾기(1부터). 없으면 오류 또는 대체 값.",
        "code": "FIND(\"BC\", \"ABCDE\")",
        "output": "2",
    },
    "search": {"sig": "SEARCH(<find>, <within>[, <start>[, <if_not_found>]])", "summary": "대소문자 **구분 없이** 찾기. 와일드카드 `?`, `*` 허용."},
    "trim": {"sig": "TRIM(<text>)", "summary": "앞뒤 공백과 중간 중복 공백을 **단일 공백**으로 정리."},
    "upper": {"sig": "UPPER(<text>)", "summary": "대문자화."},
    "lower": {"sig": "LOWER(<text>)", "summary": "소문자화."},
    "value": {
        "sig": "VALUE(<text>)",
        "summary": "문자열을 숫자로 변환. 로케일 문제를 주의.",
        "code": "VALUE(\"1,234.5\")",
        "output": "1234.5(로케일에 따라 다를 수 있음)",
    },

    # -------------- Math --------------
    "divide": {
        "sig": "DIVIDE(<numerator>, <denominator>[, <alternate>])",
        "summary": "안전 나눗셈. 분모가 0/BLANK면 대체값(기본 BLANK). `/`연산자보다 먼저 고려.",
        "code": "DIVIDE([Profit], [Sales], 0)",
        "output": "매출이 0이면 0, 아니면 이익률",
    },
    "round": {"sig": "ROUND(<number>, <num_digits>)", "summary": "반올림.", "code": "ROUND(123.456, 1)", "output": "123.5"},
    "rounddown": {"sig": "ROUNDDOWN(<number>, <digits>)", "summary": "0 쪽으로 내림."},
    "roundup": {"sig": "ROUNDUP(<number>, <digits>)", "summary": "0에서 먼 쪽으로 올림."},
    "int": {"sig": "INT(<number>)", "summary": "가장 가까운 **작은 정수**로 내림.", "code": "INT(-3.2)", "output": "-4"},
    "mod": {"sig": "MOD(<number>, <divisor>)", "summary": "나머지.", "code": "MOD(10, 3)", "output": "1"},
    "ceiling": {"sig": "CEILING(<number>, <significance>)", "summary": "지정 배수로 올림.", "code": "CEILING(7, 5)", "output": "10"},
    "floor": {"sig": "FLOOR(<number>, <significance>)", "summary": "지정 배수로 내림.", "code": "FLOOR(7, 5)", "output": "5"},
    "abs": {"sig": "ABS(<number>)", "summary": "절댓값.", "code": "ABS(-3)", "output": "3"},
    "power": {"sig": "POWER(<number>, <power>)", "summary": "거듭제곱.", "code": "POWER(2, 10)", "output": "1024"},
    "sqrt": {"sig": "SQRT(<number>)", "summary": "양의 제곱근."},
    "exp": {"sig": "EXP(<number>)", "summary": "`e`의 거듭제곱."},
    "ln": {"sig": "LN(<number>)", "summary": "자연로그."},
    "log": {"sig": "LOG(<number>[, <base>])", "summary": "지정 밑의 로그(기본 10)."},
    "log10": {"sig": "LOG10(<number>)", "summary": "상용로그."},
    "rand": {"sig": "RAND()", "summary": "0 이상 1 미만 난수."},
    "randbetween": {"sig": "RANDBETWEEN(<min>, <max>)", "summary": "정수 난수."},

    # -------------- Statistical --------------
    "rankx": {
        "sig": "RANKX(<table>, <expression>[, <value>[, <order>[, <ties>]]])",
        "summary": "테이블을 식으로 정렬하고 현재 컨텍스트의 값 **순위**를 돌려준다.",
        "code": "[Sales Rank] = RANKX(ALL(Customer), [Sales], , DESC, DENSE)",
        "note": "ALL로 기준 테이블을 펼쳐야 전체 순위가 나온다.",
    },
    "rank-eq": {
        "sig": "RANK.EQ(<value>, <ref>[, <order>])",
        "summary": "값이 참조 열에서 차지하는 순위(동률 같은 순위).",
    },
    "percentile-inc": {
        "sig": "PERCENTILE.INC(<column>, <k>)",
        "summary": "열의 **k 분위수**(0~1 포함식).",
        "code": "PERCENTILE.INC(Sales[Amount], 0.9)",
        "output": "상위 10% 컷오프",
    },
    "percentile-exc": {"sig": "PERCENTILE.EXC(<column>, <k>)", "summary": "k 분위수(배타식)."},
    "median": {"sig": "MEDIAN(<column>)", "summary": "중앙값."},
    "stdev-s": {"sig": "STDEV.S(<column>)", "summary": "표본 표준편차."},
    "stdev-p": {"sig": "STDEV.P(<column>)", "summary": "모집단 표준편차."},
    "var-s": {"sig": "VAR.S(<column>)", "summary": "표본 분산."},
    "var-p": {"sig": "VAR.P(<column>)", "summary": "모집단 분산."},
    "geomean": {"sig": "GEOMEAN(<column>)", "summary": "기하 평균. 수익률 계열에 사용."},

    # -------------- Information --------------
    "isblank": {
        "sig": "ISBLANK(<value>)",
        "summary": "값이 BLANK이면 TRUE. BLANK는 DAX의 NULL에 해당.",
        "code": "IF(ISBLANK([Sales]), 0, [Sales])",
    },
    "blank": {"sig": "BLANK()", "summary": "NULL 상수. 집계 시 무시됨."},
    "iserror": {"sig": "ISERROR(<expr>)", "summary": "식이 오류를 내는지 검사."},
    "isnumber": {"sig": "ISNUMBER(<value>)", "summary": "숫자형 값인지 검사."},
    "istext": {"sig": "ISTEXT(<value>)", "summary": "텍스트형 값인지 검사."},
    "isinscope": {
        "sig": "ISINSCOPE(<column>)",
        "summary": "현재 시각적 개체에서 그 **열이 그룹화 키**로 쓰이는 수준에 있는지 검사. 매트릭스의 소계 여부 판정에 쓴다.",
        "code": "IF(ISINSCOPE('Date'[Month]), \"Month total\", \"Higher total\")",
    },
    "issubtotal": {
        "sig": "ISSUBTOTAL(<column>)",
        "summary": "`SUMMARIZE` 결과 행이 소계 행인지 표시. `ROLLUP*`과 함께 쓴다.",
    },
    "username": {
        "sig": "USERNAME()",
        "summary": "현재 보고서 사용자 ID(`domain\\user` 또는 UPN). RLS에 필수.",
    },
    "userprincipalname": {"sig": "USERPRINCIPALNAME()", "summary": "현재 사용자의 UPN(이메일 형식)."},
    "customdata": {"sig": "CUSTOMDATA()", "summary": "연결 문자열에 담긴 사용자 지정 식별자. 임베드 시나리오에서 사용."},
    "columnstatistics": {"sig": "COLUMNSTATISTICS()", "summary": "엔진이 기록한 열 통계 테이블을 반환(엔지니어링 진단용)."},
    "selectedmeasure": {
        "sig": "SELECTEDMEASURE()",
        "summary": "**계산 그룹**에서 현재 적용되는 측정값을 나타낸다. 계산 항목의 식 안에서만 의미가 있다.",
    },
    "selectedmeasurename": {"sig": "SELECTEDMEASURENAME()", "summary": "현재 선택된 측정값의 이름(문자열)."},
}
