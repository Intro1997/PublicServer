//
// Created by Outro on 2023/10/21.
//

#include "TimeTools.hpp"
#include <thread>
#include <typeinfo>

template <typename T1, typename T2>
static T1 ConvertTimeToType(T2 duration, TimeUnit unit) {
  switch (unit) {
  case TimeUnit::SECOND: {
    return std::chrono::duration_cast<std::chrono::seconds>(duration).count();
  }
  case TimeUnit::MILLISECOND: {
    return std::chrono::duration_cast<std::chrono::milliseconds>(duration)
        .count();
  }
  case TimeUnit::MICORSECOND: {
    return std::chrono::duration_cast<std::chrono::microseconds>(duration)
        .count();
  }
  case TimeUnit::NANOSECOND: {
    return std::chrono::duration_cast<std::chrono::nanoseconds>(duration)
        .count();
  }
  }
  return (T1)0;
}

// Time
uint64_t Time::GetCurrentTime(TimeUnit unit) {
  return ConvertTimeToType<uint64_t, std::chrono::system_clock::duration>(
      std::chrono::system_clock::now().time_since_epoch(), unit);
}

static void Sleep(TimeUnit unit, unsigned long long time) {
  switch (unit) {
  case TimeUnit::SECOND: {
    std::this_thread::sleep_for(std::chrono_literals::operator""s(time));
    break;
  }
  case TimeUnit::MILLISECOND: {
    std::this_thread::sleep_for(std::chrono_literals::operator""ms(time));
    break;
  }
  case TimeUnit::MICORSECOND: {
    std::this_thread::sleep_for(std::chrono_literals::operator""us(time));
    break;
  }
  case TimeUnit::NANOSECOND: {
    std::this_thread::sleep_for(std::chrono_literals::operator""ns(time));
    break;
  }
  }
}
// RealTimer
void RealTimer::Start() { start_ = std::chrono::high_resolution_clock::now(); }

void RealTimer::Stop() { end_ = std::chrono::high_resolution_clock::now(); }

int64_t RealTimer::GetDuration(TimeUnit unit) const {
  return ConvertTimeToType<int64_t, std::chrono::duration<float>>(end_ - start_,
                                                                  unit);
}

// CpuTimer
void CpuTimer::Start() { start_ = std::clock(); }

void CpuTimer::Stop() { end_ = std::clock(); }

long double CpuTimer::GetDuration(TimeUnit unit) const {
  std::clock_t duration_sec = (end_ - start_) / CLOCKS_PER_SEC;
  switch (unit) {
  case TimeUnit::SECOND: {
    return (long double)duration_sec;
  }
  case TimeUnit::MILLISECOND: {
    return (long double)(duration_sec * 1e3);
  }
  case TimeUnit::MICORSECOND: {
    return (long double)(duration_sec * 1e6);
  }
  case TimeUnit::NANOSECOND: {
    return (long double)(duration_sec * 1e9);
  }
  }
  return 0.0;
}