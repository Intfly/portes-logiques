#include "Nombre.hpp"
#include "Gate.hpp"
#include <iostream>
#include<string>
#include<vector>

std::string Nombre::addition(Nombre Nombre2){
	std::string N1 = "0" + this->nombre;
	std::string N2 = "0" + Nombre2.nombre;
	std::vector<int> inter = { 0,0 };
	std::string resultat = "";
	if (N1.length() > N2.length()) {
		int longueurMax = N2.length();
		std::string zeroConcatenation = "";
		std::cout << std::to_string(longueurMax - N2.length());
		for (int i = 0; i < (longueurMax - N1.length()); i++) {//la boucle est broken, longueurMax - N1.length() = 0 donc erreur
			zeroConcatenation = zeroConcatenation + "0";
		}
		N1 = zeroConcatenation + N1;
		
	}
	else {
		int longueurMax = N1.length();
		std::string zeroConcatenation = "";
		std::cout << std::to_string(longueurMax - N2.length());
		for (int i = 0; i < (longueurMax - N2.length()); i++) {//la boucle est broken, longueurMax - N1.length() = 0 donc erreur
			zeroConcatenation = zeroConcatenation + "0";
		}
		N2 = zeroConcatenation + N2;
		
	}
	std::cout << "ok2";
	for (int i = -1; i < N1.length();i++) {
		Gate P = Gate(int(N1[N1.length() - i - 1]));
		Gate Q = Gate(int(N2[N2.length() - i - 1]));
		Gate Cin = Gate(bool(int(inter[0])));
		std::vector<bool> inter = P.circuit_additionneur(Q, Cin);
		std::string resulat = std::to_string(int(inter[1])) + resulat;
	}
	return resultat;
}
