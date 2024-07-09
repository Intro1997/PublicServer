#include "TimeTools.hpp"
#include <cmath>
#include <iostream>
#include <unordered_map>

void Assert(double expect, double val, const char *err_msg) {
  if (std::abs(expect - val) > (double)1e-9) {
    std::cerr << err_msg << std::endl;
    std::cerr << "expect : " << expect << ", get: " << val << std::endl;
    std::exit(-1);
  }
}

std::unordered_map<TimeUnit, std::string> time_name_map = {
    {TimeUnit::SECOND, "SECOND"},
    {TimeUnit::MILLISECOND, "MILLISECOND"},
    {TimeUnit::MICORSECOND, "MICORSECOND"},
    {TimeUnit::NANOSECOND, "NANOSECOND"}};

template <typename ChronoTimeType, TimeUnit TimeUnitType>
void DoTimeTest(const uint32_t &time_val) {
  double double_time(time_val);
  ChronoTimeType chrono_time(time_val);
  // clang-format off

  static const double kSecondsNanoseconds = 1e9;
  static const double kMillisecondsNanoseconds = 1e6;
  static const double kMicrosecondsNanoseconds = 1e3;
  static const double kNanosecondsNanoseconds = 1;

  double chrono_time_nanoseconds = std::chrono::duration_cast<std::chrono::nanoseconds>(chrono_time).count();

  double convert_seconds = chrono_time_nanoseconds / kSecondsNanoseconds;
  double convert_milliseconds = chrono_time_nanoseconds / kMillisecondsNanoseconds;
  double convert_microseconds = chrono_time_nanoseconds / kMicrosecondsNanoseconds;
  double convert_nanoseconds = chrono_time_nanoseconds / kNanosecondsNanoseconds;
  
  Assert(
    convert_seconds, Time::ConvertFromLeftTimeUnitToRight<TimeUnitType, TimeUnit::SECOND>(double_time), 
    (time_name_map[TimeUnitType] + " to SECOND failed.").c_str()
  );
  Assert(
    convert_milliseconds, Time::ConvertFromLeftTimeUnitToRight<TimeUnitType, TimeUnit::MILLISECOND>(double_time), 
    (time_name_map[TimeUnitType] + " to MILLISECOND failed.").c_str()
  );
  Assert(
    convert_microseconds, Time::ConvertFromLeftTimeUnitToRight<TimeUnitType, TimeUnit::MICORSECOND>(double_time), 
    (time_name_map[TimeUnitType] + " to MICORSECOND failed.").c_str()
  );
  Assert(
    convert_nanoseconds, Time::ConvertFromLeftTimeUnitToRight<TimeUnitType, TimeUnit::NANOSECOND>(double_time), 
    (time_name_map[TimeUnitType] + " to NANOSECOND failed.").c_str()
  );
  // clang-format on
}

void DoAllTimeTest() {
  DoTimeTest<std::chrono::seconds, TimeUnit::SECOND>(233);
  DoTimeTest<std::chrono::milliseconds, TimeUnit::MILLISECOND>(42);
  DoTimeTest<std::chrono::microseconds, TimeUnit::MICORSECOND>(233);
  DoTimeTest<std::chrono::nanoseconds, TimeUnit::NANOSECOND>(42);

  DoTimeTest<std::chrono::seconds, TimeUnit::SECOND>(-233);
  DoTimeTest<std::chrono::milliseconds, TimeUnit::MILLISECOND>(-42);
  DoTimeTest<std::chrono::microseconds, TimeUnit::MICORSECOND>(-233);
  DoTimeTest<std::chrono::nanoseconds, TimeUnit::NANOSECOND>(-42);

  // error test
  DoTimeTest<std::chrono::nanoseconds, TimeUnit::SECOND>(-42);
}

int main() {
  DoAllTimeTest();
  return 0;
}