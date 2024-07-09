//
// Created by Outro on 2023/10/21.
//

#ifndef WALLPAPER3D_APP_SRC_MAIN_CPP_COMMON_TIMER_HPP_
#define WALLPAPER3D_APP_SRC_MAIN_CPP_COMMON_TIMER_HPP_
#include <chrono>
#include <ctime>

enum class TimeUnit { SECOND = 0, MILLISECOND, MICORSECOND, NANOSECOND };

class Time {
public:
  Time() = delete;
  static uint64_t GetCurrentTime(TimeUnit unit);
  static void Sleep(TimeUnit unit, uint64_t time);
};

class RealTimer {
public:
  RealTimer() = default;
  void Start();
  void Stop();
  int64_t GetDuration(TimeUnit unit) const;

private:
  std::chrono::time_point<std::chrono::steady_clock> start_;
  std::chrono::time_point<std::chrono::steady_clock> end_;
};

class CpuTimer {
public:
  CpuTimer() = default;
  void Start();
  void Stop();
  long double GetDuration(TimeUnit unit) const;

private:
  std::clock_t start_;
  std::clock_t end_;
};

#endif // WALLPAPER3D_APP_SRC_MAIN_CPP_COMMON_TIMER_HPP_
