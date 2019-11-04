cmake_minimum_required(VERSION 3.8)
project(Server)

set(CMAKE_CXX_STANDARD 11)
include_directories(header)
set(SOURCE_FILES
    header/AdhocServer.h
    header/CommandList.h
    src/tcp_command.c
        src/control.c)

add_executable(Server ${SOURCE_FILES})