#ifndef LOULIB_H
#define LOULIB_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <inttypes.h>

typedef struct {
    uint8_t* data;
    size_t capacity;
    size_t top;
} Stack;

void     stack_init(Stack* s, size_t initialCapacity);
void     stack_pushU64(Stack *s, uint64_t val);
uint64_t stack_popU64(Stack *s);
void     stack_free(Stack* s);

#endif