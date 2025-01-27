FROM johnramsden/upmem

COPY . /app
WORKDIR /app
RUN apt update && apt -y install cmake
RUN cmake .
