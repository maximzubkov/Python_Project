#pragma once
#include <vector>


class Graph{
    public:
        Graph(std::size_t n_vertex, std::vector< std::vector<double> >& matrix);
        Graph(std::string dir);
        void addVertex(std::vector <double> v);
        void removeVertex(const size_t vert);
        void printMatrix(void) const;
        void printNodeList(void) const;
        size_t size() const;
        std::vector < std::vector <double> > getMatrix() const;
        friend std::ostream& operator << (std::ostream &ostr, const Graph &graph);
    private:
        std::size_t graph_size_;
        std::vector < std::vector <double> > graph_matrix_;
};

