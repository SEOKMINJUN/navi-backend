# Navi API 문서

## 목차
1. [계정 관리 API](#계정-관리-api)
2. [체크리스트 API](#체크리스트-api)
3. [일정 관리 API](#일정-관리-api)
4. [커뮤니티 API](#커뮤니티-api)

## 계정 관리 API

### 회원가입
- **URL**: `/api/signup/`
- **Method**: `POST`
- **인증**: 불필요
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string",
    "email": "string",
    "student_id": "string",
    "nickname": "string"
  }
  ```

### 로그인
- **URL**: `/api/login/`
- **Method**: `POST`
- **인증**: 불필요
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

### 토큰 갱신
- **URL**: `/api/token/refresh/`
- **Method**: `POST`
- **인증**: 불필요
- **Request Body**:
  ```json
  {
    "refresh": "string"
  }
  ```

### 비밀번호 초기화 요청
- **URL**: `/api/password-reset-request/`
- **Method**: `POST`
- **인증**: 불필요
- **Request Body**:
  ```json
  {
    "email": "string"
  }
  ```
- **Response**:
  - 성공 (200):
    ```json
    {
      "message": "임시 비밀번호가 이메일로 전송되었습니다.",
      "temp_password": "string"
    }
    ```
  - 실패:
    - 이메일 누락 (400):
      ```json
      {
        "error": "이메일을 입력해주세요."
      }
      ```
    - 사용자 없음 (404):
      ```json
      {
        "error": "해당 이메일로 등록된 사용자가 없습니다."
      }
      ```
    - 이메일 전송 실패 (500):
      ```json
      {
        "error": "이메일 전송에 실패했습니다.",
        "temp_password": "string"
      }
      ```

### 비밀번호 재설정 (일반 사용자)
- **URL**: `/api/reset-password/`
- **Method**: `POST`
- **인증**: 필요
- **Request Body**:
  ```json
  {
    "current_password": "string",
    "new_password": "string"
  }
  ```

### 비밀번호 재설정 (관리자)
- **URL**: `/api/reset-password/`
- **Method**: `POST`
- **인증**: 관리자 필요
- **Request Body**:
  ```json
  {
    "username": "string",
    "new_password": "string"
  }
  ```

## 체크리스트 API

### 체크리스트 목록 조회
- **URL**: `/api/checklist/`
- **Method**: `GET`
- **인증**: 필요

### 체크리스트 항목 생성
- **URL**: `/api/checklist/`
- **Method**: `POST`
- **인증**: 필요
- **Request Body**:
  ```json
  {
    "item_name": "string",
    "status": boolean
  }
  ```

## 일정 관리 API

### 일정 목록 조회
- **URL**: `/api/schedule/`
- **Method**: `GET`
- **인증**: 필요

### 일정 생성
- **URL**: `/api/schedule/`
- **Method**: `POST`
- **인증**: 필요
- **Request Body**:
  ```json
  {
    "title": "string",
    "description": "string",
    "start_time": "datetime",
    "end_time": "datetime"
  }
  ```

## 커뮤니티 API

### 게시판 관리

#### 게시판 목록 조회
- **URL**: `/api/community/boards/`
- **Method**: `GET`
- **인증**: 필요

#### 게시판 생성 (관리자)
- **URL**: `/api/community/boards/`
- **Method**: `POST`
- **인증**: 관리자 필요
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string"
  }
  ```

#### 게시판 수정 (관리자)
- **URL**: `/api/community/boards/{board_id}/`
- **Method**: `PUT`
- **인증**: 관리자 필요
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string"
  }
  ```

#### 게시판 삭제 (관리자)
- **URL**: `/api/community/boards/{board_id}/`
- **Method**: `DELETE`
- **인증**: 관리자 필요

### 게시글 관리

#### 게시글 목록 조회
- **URL**: `/api/community/posts/`
- **Method**: `GET`
- **인증**: 필요

#### 게시글 작성
- **URL**: `/api/community/posts/`
- **Method**: `POST`
- **인증**: 필요
- **Request Body**:
  ```json
  {
    "title": "string",
    "content": "string",
    "board": "integer"
  }
  ```

#### 게시글 상세 조회
- **URL**: `/api/community/posts/{post_id}/`
- **Method**: `GET`
- **인증**: 필요

#### 게시글 수정
- **URL**: `/api/community/posts/{post_id}/`
- **Method**: `PUT`
- **인증**: 작성자 필요
- **Request Body**:
  ```json
  {
    "title": "string",
    "content": "string",
    "board": "integer"
  }
  ```

#### 게시글 삭제
- **URL**: `/api/community/posts/{post_id}/`
- **Method**: `DELETE`
- **인증**: 작성자 필요

### 댓글 관리

#### 댓글 작성
- **URL**: `/api/community/posts/{post_id}/add_comment/`
- **Method**: `POST`
- **인증**: 필요
- **Request Body**:
  ```json
  {
    "content": "string"
  }
  ```

#### 댓글 목록 조회
- **URL**: `/api/community/comments/?post={post_id}`
- **Method**: `GET`
- **인증**: 필요

#### 댓글 수정
- **URL**: `/api/community/comments/{comment_id}/`
- **Method**: `PUT`
- **인증**: 작성자 필요
- **Request Body**:
  ```json
  {
    "content": "string"
  }
  ```

#### 댓글 삭제
- **URL**: `/api/community/comments/{comment_id}/`
- **Method**: `DELETE`
- **인증**: 작성자 필요

#### 대댓글 작성
- **URL**: `/api/community/comments/{comment_id}/reply/`
- **Method**: `POST`
- **인증**: 필요
- **Request Body**:
  ```json
  {
    "content": "string"
  }
  ```

## 인증
대부분의 API는 JWT 토큰 인증이 필요합니다. 인증이 필요한 API 요청 시 다음과 같이 헤더에 토큰을 포함해야 합니다:
```
Authorization: Bearer <access_token>
```

## 에러 응답
API는 다음과 같은 HTTP 상태 코드를 반환할 수 있습니다:
- 200: 성공
- 201: 생성 성공
- 400: 잘못된 요청
- 401: 인증 실패
- 403: 권한 없음
- 404: 리소스를 찾을 수 없음
- 500: 서버 내부 오류 