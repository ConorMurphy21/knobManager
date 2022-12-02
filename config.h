//
// Created by conor on 2022-11-28.
//
#pragma once

#include <boost/program_options/variables_map.hpp>

namespace po = boost::program_options;
extern po::variables_map FLAG_STORE;

void parse_args(int argc, char** argv);

