# Skillsets

Codex에서 사용하는 스킬 모음입니다.

## 덕테이프 포스터

현재 버전: **1.0.0** · [스킬 다운로드](https://github.com/hotjinnasim-code/Skillsets/releases/download/ducttape-poster-v1.0.0/ducttape-poster-1.0.0.zip)

[덕테이프 포스터](skills/ducttape-poster/SKILL.md)는 문구와 디자인 조건을 받아 서로 다른 스타일의 포스터 다섯 장을 제작합니다. 사용자 지정 수량·스타일·비율을 우선하며, 한 장 수정은 해당 이미지에만 적용합니다.

스타일 설계·텍스트 위계·본문 흐름·레퍼런스 아이디어와 이미지 제작 지침은 스킬 안에 있습니다. 제작을 마친 첫 완료 답변에 각 이미지와 원본 다운로드 링크·픽셀 크기를 함께 전달합니다.

## 설치와 사용

`skills/ducttape-poster` 폴더를 `~/.codex/skills/ducttape-poster`로 복사하고 `$ducttape-poster` 또는 `덕테이프 포스터`를 호출합니다. 넣을 문구와 목적·매체·디자인 조건을 적습니다. 제목만 있는 요청과 글자 없는 요청도 처리합니다.

## 구성과 검증

스킬 폴더에는 지침, 재사용할 레퍼런스, 제작·전달 보조 도구와 회귀 테스트만 있습니다. 테스트는 저장소 루트에서 실행합니다. 구성 스케치 테스트에는 Pillow와 테스트에 지정된 시스템 글꼴이 필요합니다.

```sh
python3 -B -m unittest discover -s skills/ducttape-poster/tests -v
```

이전 평가·시안·초안의 원기록은 [정리 전 Git 이력](https://github.com/hotjinnasim-code/Skillsets/tree/b2d7d512f2d952474079144d5141a2a082ecdb37/evals/ducttape-poster)에서 확인할 수 있습니다.
