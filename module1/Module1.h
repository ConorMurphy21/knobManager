//
// Created by conor on 2022-11-28.
//
#pragma once

#include <iostream>
#include <utility>
#include "config.h"

namespace noname{
namespace module1 {
class Module1 {
public:
    config_t config;

    Module1(config_t config) :
        config(std::move(config))
    {}

    Module1() :
        config(config_t())
    {}

    void print_config(){
      std::cout << config.test << std::endl;
      std::cout << config.words << std::endl;
      std::cout << config.test2 << std::endl;
      std::cout << config.hello << std::endl;
    }
};

}
}
