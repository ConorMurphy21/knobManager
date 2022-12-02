#include "config.h"
#include "module1/Module1.h"

int main(int argc, char** argv) {

    parse_args(argc, argv);
    Module1 mod;
    mod.print_config();
    return 0;
}