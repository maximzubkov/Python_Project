#include "Graph.h" 
#include <iostream>



// /Users/MaximZubkov/Desktop/Programming/Python/Python_Project/analysis/markovs_chain/graph.txt это я для себя


int main(int argc, char * argv[]) {
    Graph graph(argv[1]);
    std::cout << graph;
    std::cout << "success";
    return 0;
}
