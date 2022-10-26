#include <iostream>
#include <string>
#include "Gate.hpp"
#include "Nombre.hpp"
#include <vector>

int main(){
    Gate x(false);
    Gate y(false);
    Gate Cin(false);
    Nombre Nombre1("00010");
    Nombre Nombre2("001");
    std::cout << Nombre1.addition(Nombre2)<<std::endl;
    /*               TESTS               */        
    /*std::vector<bool> tab = x.circuit_additionneur(y, Cin);
    for (bool i : tab) {
        std::cout << std::to_string(i) << std::endl;
    }*/
    //x.logic_and(y).afficher();
    //std::cout << std::to_string(x.logic_not().booleen);

    return 0;
}