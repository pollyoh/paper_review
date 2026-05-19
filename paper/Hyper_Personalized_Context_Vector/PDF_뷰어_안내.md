# PDF가 에디터에서 깨져 보일 때

Cursor·VS Code는 **탭에서 PDF를 텍스트처럼 열 수** 있습니다. 이 경우 `%PDF` 바이너리와 압축 스트림이 줄 단위로 보여 **파일이 손상된 것처럼** 느껴지지만, **파일 자체는 정상인 경우가 많습니다**.

## 권장 보기 방법 (macOS)

1. **미리보기(Preview)**: Finder에서 해당 `.pdf`를 더블클릭하거나, 터미널에서  
   `open "/Users/pollyoh/Documents/GitHub/paper_study/paper/Hyper_Personalized_Context_Vector/2502.11528.pdf"`
2. **브라우저**: 주소창에 `file:///.../2502.11528.pdf` 를 붙여 넣거나, [arXiv abs](https://arxiv.org/abs/2502.11528)에서 **View PDF** 클릭.
3. **HTML 실험판**(검색·복사에 유리): 예) `https://arxiv.org/html/2502.11528v2`

## 무결성 확인

같은 폴더의 `SHA256SUMS`는 **최신 arXiv 개정판**으로 다시 받은 PDF의 해시입니다. 검증:

```bash
cd paper/Hyper_Personalized_Context_Vector
shasum -a 256 -c SHA256SUMS
```

## 본 폴더에 반영된 arXiv 개정(2026-04-27 재수신)

| 파일 | 고정 버전 |
|------|-----------|
| 2304.11406.pdf | v4 |
| 2310.08560.pdf | v2 |
| 2310.18608.pdf | v3 |
| 2402.13598.pdf | v2 |
| 2412.13432.pdf | v3 |
| 2502.11528.pdf | v2 |
| 2503.17003.pdf | v4 |
| 2507.21509.pdf | v3 |
| 2508.03935.pdf | v1 |
| 2601.05171.pdf | v2 |
