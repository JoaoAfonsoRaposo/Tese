#include <iostream>
#include <armadillo>
#include <string>

using namespace std;
using namespace arma;


int main(){
    mat C;
    C.load("chromas.csv", csv_ascii);
    std::cout << C.n_rows << C.n_cols << std::endl;
    
    vector<vector<double>> chroma_features;
    for (int i = 0; i < C.n_cols; i++)
    {
        vector <double> f;
        for (int j = 0; j < C.n_rows; j++)
        {
            f.push_back(C(j,i));
        }
        chroma_features.push_back(f);
    }
}
