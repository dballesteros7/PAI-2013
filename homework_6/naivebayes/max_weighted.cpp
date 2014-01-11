#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/prim_minimum_spanning_tree.hpp>

using namespace std;
using namespace boost;

typedef adjacency_list<vecS, vecS, undirectedS, no_property, property<edge_weight_t, double> > Graph;

int main(){
    Graph attr(5);
    add_edge(0,1,1.0 - 0.0641806290585, attr);
    add_edge(0,2,1.0 - 0.00936032569784, attr);
    add_edge(0,3,1.0 - 0.00357871586073, attr);
    add_edge(0,4,1.0 - 0.00406511002778, attr);
    add_edge(1,2,1.0 - 0.0441214494379, attr);
    add_edge(1,3,1.0 - 0.0586995687713, attr);
    add_edge(1,4,1.0 - 0.0175128427163, attr);
    add_edge(2,3,1.0 - 0.00854369704422, attr);
    add_edge(2,4,1.0 - 0.000334181052829, attr);
    add_edge(3,4,1.0 - 0.0935996320429, attr);
    vector<int> p(5);
    prim_minimum_spanning_tree(attr,&p[0]);
    for(int i = 0; i < 5; ++i){
        cout << p[i] << "\n";
    }
}
