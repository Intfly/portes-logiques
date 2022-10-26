#include "Nombre.hpp"
#include "Gate.hpp"
#include <iostream>
#include<string>
#include<vector>
#include <chrono>

std::string Nombre::addition(Nombre Nombre2){
	std::string N1 = "0" + this->nombre;
	std::string N2 = "0" + Nombre2.nombre;
	std::vector<int> inter = { 0,0 };
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
		//std::cout << std::to_string(longueurMax - N1.length());
		for (int i = 0; i < (longueurMax - N1.length()); i++) {
			zeroConcatenation = zeroConcatenation + "0";
		}
		N1 = zeroConcatenation + N1;
	}
	//std::string x(1, N1[N1.length() - 0 - 1]);
	//std::cout <<N1<<"    "<< N1.length()<<"    " << (N1[N1.length()-0-1])  << std::endl;// c'est un char et je dois le convertir en bool sauf que ça marche pas.
	//std::cout<<bool(stoi(x)) << "   " << bool(N1[N1.length() - 0 - 1]) << "   " << bool(N2[N2.length() - 0 - 1]) << std::endl;
	for (int i = 0; i < N1.length(); i++) {
		std::cout << "ok3"<<std::endl;
		std::string N1S(1,N1[N1.length() - i - 1]);
		std::string N2S(1,N2[N2.length() - i - 1]);
		Gate P = Gate(bool(stoi(N1S)));
		Gate Q = Gate(bool(stoi(N2S)));
		Gate Cin = Gate(bool(inter[0]));
		std::cout << bool(stoi(N1S))<<std::endl;
		std::vector<bool> inter = P.circuit_additionneur(Q, Cin);
		resultat = std::to_string(int(inter[1])) + resultat;
	}
	return resultat;
}


std::vector<int> Nombre::stats(Nombre Nombre1, int iterations) {
	std::vector<int> t1 = {};
	std::vector<int> t2 = {};
	for (int i = 0; i < iterations; i++) {
		auto t1 = std::chronohigh_resolution_clock::now();
	}
}