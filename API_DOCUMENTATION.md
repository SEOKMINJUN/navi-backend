# API 문서

## 개요
이 API는 대학생을 위한 일정 관리 및 커뮤니티 서비스를 제공합니다.

## 인증
모든 API 요청은 JWT 토큰을 Authorization 헤더에 포함시켜야 합니다.
```
Authorization: Bearer <your_jwt_token>
```

## 1. 계정 관리 API

### 1.1 회원가입
- **URL**: `/api/signup/`
- **Method**: `POST`
- **요청 본문**:
```json
{
    "username": "사용자아이디",
    "password": "비밀번호",
    "email": "이메일",
    "student_id": "학번",
    "nickname": "닉네임"
}
```
- **응답**: 201 Created
```json
{
    "message": "회원가입 성공"
}
```

### 1.2 로그인
- **URL**: `/api/login/`
- **Method**: `POST`
- **요청 본문**:
```json
{
    "username": "사용자아이디",
    "password": "비밀번호"
}
```
- **응답**: 200 OK
```json
{
    "access": "액세스토큰",
    "refresh": "리프레시토큰"
}
```

### 1.3 토큰 갱신
- **URL**: `/api/token/refresh/`
- **Method**: `POST`
- **요청 본문**:
```json
{
    "refresh": "리프레시토큰"
}
```
- **응답**: 200 OK
```json
{
    "access": "새로운액세스토큰"
}
```

### 1.4 비밀번호 재설정
- **URL**: `/api/reset-password/`
- **Method**: `POST`
- **인증**: 필요 (JWT 토큰)
- **권한**: 관리자 또는 본인

#### 관리자 요청
- **요청 본문**:
```json
{
    "username": "사용자아이디",
    "new_password": "새비밀번호"
}
```

#### 일반 사용자 요청
- **요청 본문**:
```json
{
    "current_password": "현재비밀번호",
    "new_password": "새비밀번호"
}
```

- **응답**: 200 OK
```json
{
    "message": "비밀번호가 성공적으로 변경되었습니다."
}
```

## 2. 체크리스트 API

### 2.1 체크리스트 목록 조회
- **URL**: `/api/checklist/`
- **Method**: `GET`
- **응답**: 200 OK
```json
[
    {
        "item_name": "할 일 1",
        "status": false
    }
]
```

### 2.2 체크리스트 항목 생성
- **URL**: `/api/checklist/`
- **Method**: `POST`
- **요청 본문**:
```json
{
    "item_name": "새로운 할 일",
    "status": false
}
```
- **응답**: 200 OK
```json
{
    "item_name": "새로운 할 일",
    "status": false
}
```

### 2.3 체크리스트 항목 수정
- **URL**: `/api/checklist/<id>/`
- **Method**: `PATCH`
- **요청 본문**:
```json
{
    "status": true
}
```
- **응답**: 200 OK
```json
{
    "item_name": "새로운 할 일",
    "status": true
}
```

### 2.4 체크리스트 항목 삭제
- **URL**: `/api/checklist/<id>/`
- **Method**: `DELETE`
- **응답**: 204 No Content

## 3. 일정 관리 API

### 3.1 일정 목록 조회
- **URL**: `/api/schedule/`
- **Method**: `GET`
- **응답**: 200 OK
```json
[
    {
        "id": 1,
        "title": "일정 1",
        "description": "일정 세부 내용",
        "start_time": "2024-03-20T10:00:00Z",
        "end_time": "2024-03-20T12:00:00Z"
    }
]
```

### 3.2 일정 생성
- **URL**: `/api/schedule/`
- **Method**: `POST`
- **요청 본문**:
```json
{
    "title": "일정 2",
    "description": "일정 세부 내용",
    "start_time": "2024-03-20T10:00:00Z",
    "end_time": "2024-03-20T12:00:00Z"
}
```
- **응답**: 201 Created

### 3.3 일정 수정
- **URL**: `/api/schedule/<id>/`
- **Method**: `PUT`/`PATCH`
- **요청 본문**:
```json
{
    "title": "수정된 일정",
    "description": "수정된 설명"
}
```
- **응답**: 200 OK

### 3.4 일정 삭제
- **URL**: `/api/schedule/<id>/`
- **Method**: `DELETE`
- **응답**: 204 No Content

## 4. 커뮤니티 API

### 4.1 게시판 관리
#### 4.1.1 게시판 목록 조회
- **URL**: `/api/community/boards/`
- **Method**: `GET`
- **응답**: 200 OK
```json
[
    {
        "id": 1,
        "name": "공지사항",
        "description": "공지사항 게시판"
    }
]
```

#### 4.1.2 게시판 생성 (관리자만)
- **URL**: `/api/community/boards/`
- **Method**: `POST`
- **요청 본문**:
```json
{
    "name": "새 게시판",
    "description": "새 게시판 설명"
}
```
- **응답**: 201 Created

### 4.2 게시글 관리
#### 4.2.1 게시글 목록 조회
- **URL**: `/api/community/posts/`
- **Method**: `GET`
- **쿼리 파라미터**:
  - `board`: 게시판 ID (선택)
  - `search`: 검색어 (선택)
  - `ordering`: 정렬 기준 (created_at, updated_at, view_count)
- **응답**: 200 OK
```json
[
    {
        "id": 1,
        "title": "게시글 제목",
        "author_username": "작성자",
        "created_at": "2024-03-20T10:00:00Z",
        "view_count": 10,
        "comment_count": 5
    }
]
```

#### 4.2.2 게시글 작성
- **URL**: `/api/community/posts/`
- **Method**: `POST`
- **요청 본문**:
```json
{
    "title": "게시글 제목",
    "content": "게시글 내용",
    "board": 1
}
```
- **응답**: 201 Created

#### 4.2.3 게시글 상세 조회
- **URL**: `/api/community/posts/<id>/`
- **Method**: `GET`
- **응답**: 200 OK
```json
{
    "id": 1,
    "title": "게시글 제목",
    "content": "게시글 내용",
    "board": 1,
    "board_name": "공지사항",
    "author_username": "작성자",
    "created_at": "2024-03-20T10:00:00Z",
    "view_count": 10,
    "comments": [
        {
            "id": 1,
            "content": "댓글 내용",
            "author_username": "댓글작성자",
            "created_at": "2024-03-20T10:30:00Z",
            "replies": []
        }
    ]
}
```

### 4.3 댓글 관리
#### 4.3.1 댓글 작성
- **URL**: `/api/community/posts/<post_id>/add_comment/`
- **Method**: `POST`
- **요청 본문**:
```json
{
    "content": "댓글 내용"
}
```
- **응답**: 201 Created

#### 4.3.2 답글 작성
- **URL**: `/api/community/comments/<comment_id>/reply/`
- **Method**: `POST`
- **요청 본문**:
```json
{
    "content": "답글 내용"
}
```
- **응답**: 201 Created

## 에러 응답

### 400 Bad Request
잘못된 요청 형식이나 데이터
```json
{
    "field_name": ["에러 메시지"]
}
```

### 401 Unauthorized
인증되지 않은 요청
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
권한이 없는 요청
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
존재하지 않는 리소스
```json
{
    "detail": "Not found."
}
```

## 제약사항
1. 모든 API는 인증이 필요합니다 (회원가입, 로그인 제외).
2. 게시판 생성은 관리자만 가능합니다.
3. 게시글과 댓글은 작성자만 수정/삭제할 수 있습니다.
4. 체크리스트 항목은 사용자당 동일한 이름을 가진 항목이 하나만 존재할 수 있습니다.
5. 일정은 사용자 본인의 것만 조회/수정/삭제할 수 있습니다 (관리자 제외). 