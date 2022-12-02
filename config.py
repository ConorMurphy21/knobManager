import configparser
import dataclasses
import os
import sys


@dataclasses.dataclass
class Flag:
    module: str
    name: str
    val: str
    cpp_type: str


py_types = [
    # (type, test)
    (int, int),
    (float, float),
    (bool, lambda x: x.lower() == 'true' or x.lower() == 'false'),
    (str, str),
]

cpp_types = [
    'bool',
    'std::string',
    'double',
    'uint64_t',
    'uint32_t',
    'int64_t',
    'int32_t',
]

py_to_cpp = {
    bool: 'bool',
    str: 'std::string',
    float: 'double',
}


def get_cpp_type(key: str, val: str):
    # if explicitly defined in name
    for ct in cpp_types:
        if ct in key:
            return ct

    # otherwise guess
    py_type = None
    for (pt, test) in py_types:
        try:
            if test(val):
                py_type = pt
                break
        except ValueError:
            pass

    if py_type == int:
        if int(val) < 0:
            return 'int32_t'
        else:
            return 'uint64_t'
    return py_to_cpp[py_type]


def strip_data_types(key: str):
    for ct in cpp_types:
        key = key.removeprefix(f'{ct} ')
    return key


def parse_config(config_file: str):
    cp = configparser.ConfigParser()
    cp.read(config_file)
    flags = []
    for module in cp.sections():
        for key in cp[module]:
            val = cp[module][key]
            cpp_type = get_cpp_type(key, val)
            name = strip_data_types(key)
            # wrap string in quotes if there are none
            if cpp_type == 'std::string' and val[0] != '"':
                val = f'"{val}"'
            flags.append(Flag(module, name, val, cpp_type))
    return cp.sections(), flags


def option_desc(flag: Flag):
    if flag.module == 'root':
        return f'("{flag.name}", po::value<{flag.cpp_type}>()->default_value({flag.val}))'
    return f'("{flag.module}.{flag.name}", po::value<{flag.cpp_type}>()->default_value({flag.val}))'


def main_config_str(flags: [Flag]):
    option_descs = '\n    '.join(option_desc(flag) for flag in flags)
    config_cpp = f'''
//
// TODO: explain where this is auto-generated from
//
#include "config.h"

#include <boost/program_options/parsers.hpp>
#include <boost/program_options/options_description.hpp>

namespace po = boost::program_options;
po::variables_map FLAG_STORE;

void parse_args(int argc, char** argv) {{
    po::options_description desc;
    desc.add_options()
    {option_descs}
    ;
    po::store(po::parse_command_line(argc, argv, desc), FLAG_STORE);
    po::notify(FLAG_STORE);

    po::store(po::parse_config_file("config.ini", desc), FLAG_STORE);
    po::notify(FLAG_STORE);
}}
    '''
    return config_cpp


def generate_main_config(path: str, flags: [Flag]):
    with open(os.path.join(path, 'config.cpp'), 'w') as file:
        file.write(main_config_str(flags))


def type_decl(flag: Flag):
    return f'const {flag.cpp_type} {flag.name};'


def default_decl(flag: Flag):
    return f'{flag.name}(FLAG_STORE["{flag.module}.{flag.name}"].as<{flag.cpp_type}>())'


def param_decl(flag: Flag):
    return f'{flag.cpp_type} {flag.name}'


def assigned_val(flag: Flag):
    if flag.cpp_type == 'std::string':
        return f'{flag.name}(std::move({flag.name}))'
    return f'{flag.name}({flag.name})'


def module_config_str(module: str, flags: [Flag]):
    type_decls = '\n        '.join(type_decl(flag) for flag in flags)
    default_vals = '\n        , '.join(default_decl(flag) for flag in flags)
    param_decls = ', '.join(param_decl(flag) for flag in flags)
    assigned_vals = '\n        , '.join(assigned_val(flag) for flag in flags)
    h_config = f'''
//
// TODO: explain where this is auto-generated from
//

#pragma once
#include <cstdint>
#include <boost/program_options/variables_map.hpp>

namespace po = boost::program_options;
extern po::variables_map FLAG_STORE;

namespace {module} {{
    typedef struct config_t{{
        {type_decls}

        config_t()
        : {default_vals}
        {{}}
        
        config_t({param_decls})
        : {assigned_vals}
        {{}}
    }} config_t;
}}
    '''
    return h_config


def generate_module_config(path: str, module: str, flags: [Flag]):
    module_path = os.path.join(path, module)
    with open(os.path.join(module_path, 'config.h'), 'w') as file:
        file.write(module_config_str(module, flags))


def config_update(path: str):
    return os.path.getmtime(os.path.join(path, 'config.ini')) > os.path.getmtime(os.path.join(path, 'config.cpp'))


def main():
    path = sys.argv[1]
    #if not config_update(path):
        #return
    modules, flags = parse_config(os.path.join(path, 'config.ini'))
    generate_main_config(path, flags)
    for module in modules:
        if module != 'root':
            generate_module_config(path, module, [flag for flag in flags if flag.module == module])


if __name__ == '__main__':
    main()
