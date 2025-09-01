#include "lou_lib.h"

void stack_init(Stack* s, size_t initialCapacity) {
    s->data = malloc(initialCapacity);
    if (s->data == NULL) {
        fprintf(stderr, "stack_init: malloc failed\n");
        exit(1);
    }

    s->capacity = initialCapacity;
    s->top = 0;
}

void stack_pushU64(Stack *s, uint64_t val) {
    if (s->top + sizeof(uint64_t) >= s->capacity) {
        s->capacity *= 2;
        s->data = realloc(s->data, s->capacity);
        if (s->data == NULL) {
            fprintf(stderr, "stack_pushU64: realloc failed\n");
            exit(1);
        }
    }

    memcpy(s->data + s->top, &val, sizeof(uint64_t));
    s->top += sizeof(uint64_t);
}

uint64_t stack_popU64(Stack *s) {
    if (s->top < sizeof(uint64_t)) {
        stack_free(s);
        fprintf(stderr, "stack_popU64: stack underflow\n");
        exit(1);
    }
    
    uint64_t val;

    s->top -= sizeof(uint64_t);
    memcpy(&val, s->data + s->top, sizeof(uint64_t));

    return val;
}

void stack_free(Stack* s) {
    free(s->data);
    s->capacity = 0;
    s->top = 0;
}