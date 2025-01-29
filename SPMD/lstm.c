#include <stdio.h>
#include <stdlib.h>
#include <alloc.h>
#include "tensor.h"
double __mram_noinit forget_weight[HIDDEN_SIZE * CHUNK_SIZE];
double __mram_noinit forget_bias[HIDDEN_SIZE];

double __mram_noinit input_weight[HIDDEN_SIZE * CHUNK_SIZE];
double __mram_noinit input_bias[HIDDEN_SIZE];

double __mram_noinit cell_weight[HIDDEN_SIZE * CHUNK_SIZE];
double __mram_noinit cell_bias[HIDDEN_SIZE];

double __mram_noinit output_weight[HIDDEN_SIZE * CHUNK_SIZE];
double __mram_noinit output_bias[HIDDEN_SIZE];

double __mram_noinit input_res[HIDDEN_SIZE];
double __mram_noinit forget_res[HIDDEN_SIZE];
double __mram_noinit output_res[HIDDEN_SIZE];
double __mram_noinit cell_res[HIDDEN_SIZE];

#define INPUT_STR_SIZE (1 << 10)

char __mram_noinit query[INPUT_STR_SIZE];
uint32_t __mram_noinit downloaded;
__host volatile uint64_t output;
__host volatile uint64_t ready = 0;

double input[CHUNK_SIZE];

double hidden[HIDDEN_SIZE];
double cell[HIDDEN_SIZE];
double tmp[HIDDEN_SIZE];

// Approximation of exp(x)
float exp_approx(float x) {
    float result = 1.0f + x + (x * x) / 2.0f + (x * x * x) / 6.0f;
    return result > 100.0f ? 100.0f : result; // Prevent overflow
}

// Approximation of sigmoid(x) = 1 / (1 + exp(-x))
float sigmoid(float x) {
    return 1.0f / (1.0f + exp_approx(-x));
}

// Approximation of tanh(x)
float tanh_approx(float x) {
    float x2 = x * x;
    return x * (27.0f + x2) / (27.0f + 9.0f * x2);
}

void lstm_forward(Tensor_ptr forget_weight_t, Vec forget_bias_v, Tensor_ptr input_weight_t, Vec input_bias_v, Tensor_ptr cell_weight_t, Vec cell_bias_v, Tensor_ptr output_weight_t, Vec output_bias_v) {
    gemv(input_weight_t, input, tmp);
    vec_add(input_bias_v, tmp, hidden);
    for (int i = 0; i < HIDDEN_SIZE; i++) {
        hidden[i] = sigmoid(hidden[i]);
    }
    Vec vi = create_vec_init(input_res, hidden, HIDDEN_SIZE);
    gemv(forget_weight_t, input, tmp);
    vec_add(forget_bias_v, tmp, hidden);
    for (int i = 0; i < HIDDEN_SIZE; i++) {
        hidden[i] = sigmoid(hidden[i]);
    }
    Vec vf = create_vec_init(forget_res, hidden, HIDDEN_SIZE);
    gemv(output_weight_t, input, tmp);
    vec_add(output_bias_v, tmp, hidden);
    for (int i = 0; i < HIDDEN_SIZE; i++) {
        hidden[i] = sigmoid(hidden[i]);
    }
    Vec vo = create_vec_init(output_res, hidden, HIDDEN_SIZE);
    gemv(cell_weight_t, input, tmp);
    vec_add(cell_bias_v, tmp, hidden);
    for (int i = 0; i < HIDDEN_SIZE; i++) {
        tmp[i] = tanh_approx(hidden[i]);
    }
    v_mul(vf, cell, cell);
    v_mul(vi, tmp, tmp);
    for (int i = 0; i< HIDDEN_SIZE; i++) {
        cell[i] += tmp[i];
    }
    for (int i = 0; i < HIDDEN_SIZE; i++) {
        tmp[i] = tanh_approx(cell[i]);
    }
    v_mul(vo, tmp, hidden);
}


int main() {
    mem_reset();
    ready = 1;

    // while (!downloaded) {
    //     printf("Waiting for download\n");
    // }

    __dma_aligned char local_cache[INPUT_STR_SIZE];
    mram_read(query, local_cache, INPUT_STR_SIZE);
    output = 0;
    for (int i = 0; i < 8; i++) {
        output += local_cache[i];
    }
    
    // Create tensors and vectors for LSTM gates
    // Tensor_ptr forget_weight_t = create_tensor(forget_weight, CHUNK_SIZE, HIDDEN_SIZE);
    // Vec forget_bias_v = create_vec(forget_bias, CHUNK_SIZE);

    // Tensor_ptr input_weight_t = create_tensor(input_weight, CHUNK_SIZE, HIDDEN_SIZE);
    // Vec input_bias_v = create_vec(input_bias, CHUNK_SIZE);

    // Tensor_ptr cell_weight_t = create_tensor(cell_weight, CHUNK_SIZE, HIDDEN_SIZE);
    // Vec cell_bias_v = create_vec(cell_bias, CHUNK_SIZE);

    // Tensor_ptr output_weight_t = create_tensor(output_weight, CHUNK_SIZE, HIDDEN_SIZE);
    // Vec output_bias_v = create_vec(output_bias, CHUNK_SIZE);
    // lstm_forward(forget_weight_t, forget_bias_v, input_weight_t, input_bias_v, cell_weight_t, cell_bias_v, output_weight_t, output_bias_v);
    return 0;
}

