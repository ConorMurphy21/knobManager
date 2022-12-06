
//
// TODO: explain where this is auto-generated from
//
#include "config.h"

#include <boost/program_options/parsers.hpp>
#include <boost/program_options/options_description.hpp>

namespace po = boost::program_options;
po::variables_map FLAG_STORE;

void parse_args(int argc, char** argv) {
    po::options_description desc;
    desc.add_options()
    ("module1.test", po::value<uint64_t>()->default_value(5))
    ("module1.words", po::value<std::string>()->default_value("hello"))
    ("module1.hello", po::value<bool>()->default_value(true))
    ("module1.test2", po::value<uint32_t>()->default_value(6))
    ;
    po::store(po::parse_command_line(argc, argv, desc), FLAG_STORE);
    po::notify(FLAG_STORE);

    po::store(po::parse_config_file("config.ini", desc), FLAG_STORE);
    po::notify(FLAG_STORE);
}
    