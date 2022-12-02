
//
// TODO: explain where this is auto-generated from
//

#pragma once
#include <cstdint>
#include <boost/program_options/variables_map.hpp>

namespace po = boost::program_options;
extern po::variables_map FLAG_STORE;

namespace module1 {
    typedef struct config_t{
        const uint64_t test;
        const std::string words;
        const bool hello;
        const uint32_t test2;

        config_t()
        : test(FLAG_STORE["module1.test"].as<uint64_t>())
        , words(FLAG_STORE["module1.words"].as<std::string>())
        , hello(FLAG_STORE["module1.hello"].as<bool>())
        , test2(FLAG_STORE["module1.test2"].as<uint32_t>())
        {}
        
        config_t(uint64_t test, std::string words, bool hello, uint32_t test2)
        : test(test)
        , words(std::move(words))
        , hello(hello)
        , test2(test2)
        {}
    } config_t;
}
    