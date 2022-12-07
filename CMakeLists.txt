cmake_minimum_required(VERSION 3.22)
project(config)

set(CMAKE_CXX_STANDARD 20)

find_package( Boost 1.40 COMPONENTS program_options REQUIRED )
include_directories( ${Boost_INCLUDE_DIR} )

add_executable(config main.cpp config/config.cpp)

find_package( PythonInterp 3.9 REQUIRED )

target_link_libraries(config LINK_PUBLIC ${Boost_LIBRARIES} )

add_custom_target(
        generate_config ALL
        COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/config/config.py ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_BINARY_DIR}
        COMMENT "Generating config"
)

add_dependencies(config generate_config)


