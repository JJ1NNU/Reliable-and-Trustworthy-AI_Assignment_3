# 1. 베이스 이미지 설정 (Ubuntu 24.04)
FROM ubuntu:24.04

# 2. 환경 변수 설정
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH="/app/Marabou:${PYTHONPATH}"

# 3. 필수 시스템 패키지 및 Python 3.11 설치
RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    cmake \
    git \
    libpython3.11-dev \
    python3.11 \
    python3.11-venv \
    python3-pip \
    && add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get update && apt-get install -y python3.11-dev

# 4. 작업 디렉토리 설정
WORKDIR /app

# 5. Marabou 소스 코드 다운로드 및 빌드
RUN git clone https://github.com/NeuralNetworkVerification/Marabou.git \
    && cd Marabou \
    && mkdir build && cd build \
    && cmake .. -DBUILD_PYTHON=ON -DPYTHON_EXECUTABLE=/usr/bin/python3.11 \
    && make -j$(nproc) \
    && cp maraboupy/MarabouCore*.so ../maraboupy/

# 6. 파이썬 패키지 설치
COPY requirements.txt .
RUN python3.11 -m pip install --no-cache-dir -r requirements.txt --break-system-packages

# 7. 과제 파일 복사
COPY test.py .
COPY models/ ./models/

# 8. 실행 명령
CMD ["python3.11", "test.py"]