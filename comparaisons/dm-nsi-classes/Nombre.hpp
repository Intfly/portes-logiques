#include <string>
class Nombre{
	public:
		std::string nombre;

		Nombre(std::string val){
			nombre = val;
		}
		
		std::string addition(Nombre Nombre2);
};

