#ifndef TENSOR_H
#define TENSOR_H
#include <stdint.h>
#include <mram.h>
#define INPUT_SIZE 27
#define HIDDEN_SIZE 128
#define CHUNK_SIZE INPUT_SIZE + HIDDEN_SIZE

__dma_aligned double chunk[CHUNK_SIZE];
typedef struct _Tensor {
    uint64_t width, height;
    __mram_ptr double * mram;
} Tensor_ptr;


Tensor_ptr create_tensor(__mram_ptr double*, uint64_t, uint64_t);
void gemv(Tensor_ptr, double * input, double * output);

typedef struct _Vec {
    uint64_t length;
    __mram_ptr double * mram;
} Vec;

Vec create_vec(__mram_ptr double *, uint64_t);
Vec create_vec_init(__mram_ptr double *, double *, uint64_t);
void vec_add(Vec, double * in, double *out);
void v_mul(Vec, double* in, double* out);
void vs_mul(Vec, double, double* out);
#endif
