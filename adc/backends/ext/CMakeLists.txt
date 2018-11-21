cmake_minimum_required(VERSION 3.12)
project(ext C)

set(CMAKE_C_STANDARD 11)

find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})

add_library(ext SHARED spi_rpi.c)
