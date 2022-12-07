/*
 * Copyright (C) 2022 Data-Intensive Systems Lab, Simon Fraser University.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// THIS FILE IS AUTO-GENERATED BY config/config.py BASED OFF THE CONTENTS OF config/config.ini
// ANY CHANGES TO THIS FILE WILL NOT PERSIST
// TO ADD A CONFIG FLAG ADD A NEW FLAG TO config/config.ini

#pragma once

#include <boost/program_options/variables_map.hpp>

namespace po = boost::program_options;
extern po::variables_map FLAG_STORE;

void parse_args(int argc, char** argv);
