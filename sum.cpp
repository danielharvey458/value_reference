#include "benchmark/benchmark.h"

#include <array>
#include <iostream>
#include <memory>
#include <vector>

#define BODY                \
   size_t r = 0;            \
   for (const auto &x : a)  \
   {                        \
     r += x;                \
   }                        \
   return r;

template <size_t N>
size_t __attribute__((noinline))
sum_reference(const std::array<size_t, N> &a)
{
  BODY
}

template <size_t N>
size_t __attribute__((noinline))
sum_value(const std::array<size_t, N> a)
{
  BODY
}

#define profile(fn)                                   \
template <size_t N>                                   \
void fn(benchmark::State &state)                      \
{                                                     \
  auto v = std::array<size_t, N> ();                  \
  v.fill(1);                                          \
  for (const auto _ : state)                          \
  {                                                   \
   benchmark::DoNotOptimize (sum_##fn (v));             \
  }                                                   \
}

profile (reference)
profile (value)

#define DISPATCH_ARGS(F, n)                                                     \
   F(n, 1);                                                                     \
   F(n, 2);                                                                     \
   F(n, 3);                                                                     \
   F(n, 4);                                                                     \
   F(n, 5);                                                                     \
   F(n, 6);                                                                     \
   F(n, 7);                                                                     \
   F(n, 8);                                                                     \
   F(n, 16);

DISPATCH_ARGS(BENCHMARK_TEMPLATE, value)
DISPATCH_ARGS(BENCHMARK_TEMPLATE, reference)

BENCHMARK_MAIN()
