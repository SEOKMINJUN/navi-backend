# Navi

## 프로젝트 소개
Navi 프로젝트의 백엔드 입니다.

## 기술 스택
- **Backend**
  - Django

## 시작하기

### 필수 요구사항
- Python 3.8 이상

### 백엔드 설정
1. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. 의존성 설치
```bash
pip install -r requirements.txt
```

3. 데이터베이스 마이그레이션
```bash
python manage.py migrate
```

4. 서버 실행
```bash
python manage.py runserver
```

## API 문서
API 문서는 [API_DOCUMENT.md](API_DOCUMENT.md)에서 확인할 수 있습니다.

## 테스트
```bash
python manage.py test
```

## 배포
1. 백엔드 배포
```bash
python manage.py collectstatic
python manage.py migrate
gunicorn config.wsgi:application
```