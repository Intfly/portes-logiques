#include <string>
#include <vector>
class Nombre{
	public:
		std::string nombre;

		Nombre(std::string val){
			nombre = val;
		}
		
		std::string addition(Nombre Nombre2);
		std::vector<int> stats(Nombre Nombre2, int iterations);
};

