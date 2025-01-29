dev: lstm.c tensor.c tensor.h
	dpu-upmem-dpurte-clang -O2 lstm.c tensor.c -o dev
host: host.cpp
	g++ --std=c++11 host.cpp -o host `dpu-pkg-config --cflags --libs dpu` -g

docker:
	docker run -it --rm -v .:/app -w /app johnramsden/upmem bash

clean:
	rm -f dev host
