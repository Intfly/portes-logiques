#include "Gate.hpp"
#include <iostream>
#include <string>
#include <vector>


void Gate::afficher() {
    std::cout << "valeur booleenne: " + std::to_string(this->booleen);
}

Gate Gate::logic_not() {
    if (this->booleen) {
        return Gate(false);
    }
    return Gate(true);
}

Gate Gate::logic_nand(Gate Q) {
    if (this->booleen) {
        if (Q.booleen) {
            return Gate(false);
        }
    }
    return Gate(true);
}

Gate Gate::logic_nor(Gate Q) {
    if (this->logic_not().booleen) {
        if (Q.logic_not().booleen) {
            return Gate(true);
        }
    }
    return Gate(false);
}

Gate Gate::logic_and(Gate Q) {
    Gate A = this->logic_nor(*this);
    Gate B = Q.logic_nor(Q);
    return A.logic_nor(B);
}

Gate Gate::logic_or(Gate Q) {
    Gate A = this->logic_nand(*this);
    Gate B = Q.logic_nand(Q);
    return A.logic_nand(B);
}

Gate Gate::logic_xor(Gate Q) {
    Gate A = this->logic_and(Q.logic_not());
    Gate B = Q.logic_and(this->logic_not());
    return A.logic_or(B);
}

Gate Gate::logic_xnor(Gate Q) {
    return this->logic_xor(Q).logic_not();
}

std::vector<bool> Gate::circuit_additionneur(Gate Q, Gate Cin) {
    Gate E1 = this->logic_xor(Q);
    bool S = E1.logic_xor(Cin).booleen;
    Gate E2 = E1.logic_and(Cin);
    Gate E3 = this->logic_and(Q);
    bool Cout = E2.logic_or(E3).booleen;
    return {Cout,S};
}