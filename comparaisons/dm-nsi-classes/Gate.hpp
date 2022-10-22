#include <vector>
class Gate {   
    private:
        bool booleen;
    public:
        Gate(bool v_b) {
            booleen = v_b;
        }
    
        void afficher();
        Gate logic_not();
        Gate logic_nand(Gate Q);
        Gate logic_nor(Gate Q);
        Gate logic_and(Gate Q);
        Gate logic_or(Gate Q);
        Gate logic_xor(Gate Q);
        Gate logic_xnor(Gate Q);
        std::vector<bool> circuit_additionneur(Gate Q, Gate Cin);
};