#include "Nombre.hpp"
#include "Gate.hpp"
#include <iostream>
#include<string>
#include<vector>
#include <chrono>

std::string Nombre::addition(Nombre Nombre2){
	std::string N1 = "0" + this->nombre;
	std::string N2 = "0" + Nombre2.nombre;
	std::vector<bool> inter = { 0,0 };
	std::string resultat = "";
	if (N1.length() > N2.length()) {
		int longueurMax = N1.length();
		std::string zeroConcatenation = "";
		for (int i = 0; i < (longueurMax - N2.length()); i++) {
			zeroConcatenation = zeroConcatenation + "0";
		}
		N2 = zeroConcatenation + N2;
		
	}
	else {
		int longueurMax = N2.length();
		std::string zeroConcatenation = "";
		for (int i = 0; i < (longueurMax - N1.length()); i++) {
			zeroConcatenation = zeroConcatenation + "0";
		}
		N1 = zeroConcatenation + N1;
	}
	for (int i = 0; i < N1.length(); i++) {
		std::string N1S(1,N1[N1.length() - i - 1]);
		std::string N2S(1,N2[N2.length() - i - 1]);
		Gate P = Gate(bool(stoi(N1S)));
		Gate Q = Gate(bool(stoi(N2S)));
		Gate Cin = Gate(bool(inter[0]));
		inter = P.circuit_additionneur(Q, Cin);
		resultat = std::to_string(int(inter[1])) + resultat;
	}
	return resultat;
}


long Nombre::stats(Nombre Nombre2, int iterations) {
	auto dbt = std::chrono::high_resolution_clock::now();//j'ai du mettre le chrono en dehors de la boucle sinon les opérations sont réalisées trop rapidement et ne sont pas comptabilisées
	for (int i = 0; i < iterations; i++) {
		this->addition(Nombre2);
	}
	auto fin1 = std::chrono::high_resolution_clock().now();
	for (int i = 0; i < iterations; i++) {
	}
	auto fin2 = std::chrono::high_resolution_clock().now();
	std::chrono::duration<double, std::milli> fin = (fin1 - dbt)-(fin2-fin1);//(temps de la loop + de l'opération) - (temps de la loop) = temps de l'opération
	return fin.count();
}