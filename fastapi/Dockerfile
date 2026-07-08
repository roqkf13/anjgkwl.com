# 1. Python 3.13 가벼운 버전으로 시작
FROM python:3.13-slim

# 2. 컨테이너 내부에서 작업할 폴더 지정
WORKDIR /app

# 2-1. opencv-python(YOLO/ultralytics 의존성)이 필요로 하는 공유 라이브러리 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 libxcb1 libxext6 libsm6 libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# 3. 라이브러리 목록 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# 4. 나머지 백엔드 소스 코드 전부 복사
COPY . .

# 5. FastAPI나 Flask 같은 백엔드 앱 실행 (상황에 맞게 포트나 명령어를 수정하세요)
# 예시는 Uvicorn으로 main.py의 app을 실행하는 명령어입니다.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
