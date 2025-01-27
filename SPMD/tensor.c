#include "tensor.h"
#include <mram.h>


Tensor_ptr create_tensor(__mram_ptr double* target, uint64_t width, uint64_t height) {
    Tensor_ptr tp;
    tp.width = width;
    tp.height = height;
    tp.mram = target;
    for (int row = 0; row < height; row++) {
        for (int col = 0; col < width; col++) {
            chunk[col] = col + row;
        }
        mram_write(chunk, tp.mram + row * width, width * sizeof(double));
    }

    return tp;
}

void gemv(Tensor_ptr mat, double * input, double * output) {
    for (int row = 0; row < mat.height; row ++) {
        mram_read(mat.mram + row * mat.width, chunk, mat.width * sizeof(double));
        output[row] = 0;
        for (int col = 0; col < mat.width; col++) {
            output[row] += chunk[col] * input[col];
        }

    }
}


Vec create_vec(__mram_ptr double * target, uint64_t length) {
    for (int i = 0; i < length; i++) {
        chunk[i] = i;
    }
    return create_vec_init(target, chunk, length);

}


Vec create_vec_init(__mram_ptr double * target, double * data, uint64_t length) {
    Vec v;
    v.length = length;
    v.mram = target;
    mram_write(chunk, v.mram, length * sizeof(double));
    return v;
}



void vec_add(Vec v, double * in, double *out) {
    mram_read(v.mram, out, v.length * sizeof(double));
    for (int i = 0; i < v.length; i++) {
        out[i] += in[i];
    }
}



void v_mul(Vec v, double * in, double * out) {
    mram_read(v.mram, chunk, v.length);
    for (int i = 0; i < v.length; i++) {
        out[i] += in[i] * chunk[i];
    }
}

void vs_mul(Vec v, double s, double *out) {
    mram_read(v.mram, chunk, v.length);
    for (int i = 0; i < v.length; i++) {
        out[i]= s * chunk[i];
    }
}
