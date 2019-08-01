#include <iostream>
#include <armadillo>
#include <string>

using namespace std;
using namespace arma;


int main(){
    fmat C;
    C.load("../extractedFeatures/features.csv", csv_ascii);
    ifstream ifs("../features/path.txt");
    std::string s;
    std::getline(ifs, s);
    std::cout << s << std::endl;
    C.save(s, csv_ascii);
    
    
//     C.save("vamosverC.csv", csv_ascii);
//     A.save("vamosverA.csv", csv_ascii);
//     

}


