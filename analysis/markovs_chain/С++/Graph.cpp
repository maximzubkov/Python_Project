#include "Graph.h"
#include <iostream>
#include <vector>
#include <fstream>
#include <cstdint>
#include <string>
#include <sstream>
#include <chrono>
using namespace std;


Graph::Graph(std::string dir){
    // Открывает файл graph.txt, преобразует данные из него в матрицу инцедентности
    std::ifstream in;
    in.open(dir);
    if (!in.is_open()){
        std::cout << "invalid file";
        exit(0);
    }
    std::string line;
    std::string tmp_str;
    std::vector <double> tmp_vect;
    std::vector < std::vector <double> > res;
    std::string::size_type sz;   
    graph_size_ = 0;
    while(std::getline(in, line)){
        std::istringstream ist(line);
        while (ist >> tmp_str){
            tmp_vect.push_back(std::stod(tmp_str, &sz));
        }
        graph_matrix_.push_back(tmp_vect);
        graph_size_++;
        tmp_vect.clear();
    }
    in.close();
    std::cout << "Graph object being created with max nodes size:" << graph_size_ << "\n\n";
}


Graph::Graph(size_t n_vertex, std::vector< std::vector<double> >& matrix) : graph_size_(n_vertex), graph_matrix_(matrix) {
    // Конструктор класса, преобразующй
    std::cout << "Graph object being created with max nodes size:" << n_vertex << "\n\n";
}

std::ostream& operator << (std::ostream &ostr, const Graph &graph)
{
    auto matrix = graph.getMatrix();
    ostr << "graph size:" << graph.size() << "\n";
    ostr << "     ";
    for (int i = 0; i < graph.size(); i++){
        if (i >= 10){
            ostr << i << " ";
        } else {
            ostr << i << "  ";
        }
    }
    ostr << "\n\n";
    for (int i = 0; i < graph.size(); i++){
        if (i >= 10){
            ostr << i << "   ";
        } else {
            ostr << i << "    ";
        }
        for (int j = 0; j < graph.size(); j++){
            ostr << matrix[i][j] << "  ";
        }
        ostr << "\n";
    }
    ostr << "\n";
    return ostr;
}


void Graph::printNodeList(void) const{
    // Выводит все ребра графа в формате (u, v)
    for(int i = 0; i < graph_size_; i++){
        for(int j = 0; j < graph_size_; j++){
            if (graph_matrix_[i][j] == 1){
                std::cout << "(" << i << "," << j << ")";
            }
        }
    }
}

void Graph::addVertex(std::vector <double> v){
    graph_size_++;
    graph_matrix_.push_back(v);
    for (int i = 0; i < this->size(); i++){
       graph_matrix_[this->size() - 1][i] = v[i]; 
    }
}


// void Graph::removeVertex(const size_t vert){
//     graph_bit_code_.erase(graph_bit_code_.begin() + vert);
//     graph_size_--;
//     uint64_t tmp = (1ULL << (this->size() - vert + 1)) - 1ULL;
//     for (int i = 0; i < graph_size_; i++){
//         graph_bit_code_[i] = ((graph_bit_code_[i] >> (this->size() - vert + 1)) << (this->size() - vert)) + (graph_bit_code_[i] & tmp);
//     }
// }


size_t Graph::size() const {
    return graph_size_;
}


std::vector < std::vector <double> > Graph::getMatrix() const{
    return graph_matrix_;
}








