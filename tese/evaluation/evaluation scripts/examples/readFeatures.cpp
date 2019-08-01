#include <iostream>
#include <armadillo>
#include <string>

using namespace std;
using namespace arma;


int main(){
    fmat C;
    C.load("../extractedFeatures/features.csv", csv_ascii);
    std::cout << C.n_rows << C.n_cols << std::endl;
    
    vector<vector<float>> features;
    for (int i = 0; i < C.n_cols; i++)
    {
        vector <float> f;
        for (int j = 0; j < C.n_rows; j++)
        {
            f.push_back(C(j,i));
        }
        features.push_back(f);
    }
    
    
    
    double** arrFeatures = new double*[features.size()];	
    
    vector<vector<float>> featuresTest;

    for (int i = 0; i < features.size(); i++)
    {
        arrFeatures[i] = new double[features[0].size()];
        for (int j = 0; j < features[0].size(); j++)
            arrFeatures[i][j] = features[i][j];
        
    }
    
    
    for (int i = 0; i < features.size(); i++)
    {       
        vector<float> vec(arrFeatures[i], arrFeatures[i] + features[0].size());
        featuresTest.push_back(vec);
    }
    
    
    fmat A;
    for (int i = 0; i < featuresTest.size(); i++)
    {
        vector <float> f = featuresTest[i];
        fmat column(f);
        A.insert_cols(i, column);
    }
    
    std::cout << A.n_rows << A.n_cols << std::endl;
    
    std::cout << to_string(arrFeatures[10][10]) + to_string(111) << features[10][10] << featuresTest[10][10] << std::endl;
    
//     C.save("vamosverC.csv", csv_ascii);
//     A.save("vamosverA.csv", csv_ascii);
//     std::cout << A(12,50) << C(12,50) << std::endl;
//     

}


