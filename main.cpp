#include "config/config.h"
#include "module1/Module1.h"


int main(int argc, char **argv) {

  noname::config::parse_args(argc, argv);
  noname::config::print_config();
  noname::module1::Module1 mod;
  mod.print_config();
  return 0;
}