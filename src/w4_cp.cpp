#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef pair<int, int> pii;
typedef pair<ll, int> plli;

#define speed                         \
    ios_base::sync_with_stdio(false); \
    cin.tie(0), cout.tie(0)
#define all(v) v.begin(), v.end()
#define rall(v) v.rbegin(), v.rend()
#define sz(x) ((int)(x).size())
#define endll '\n'
#define yes cout << "YES" << endll
#define no cout << "NO" << endll
#define pb push_back

const int MX = 1e5 + 10;
const ll mod = 1e9 + 7; // 998244353
const ll INF = 1000000000000L; //0x7fffffff;

template <typename T, typename V>
ostream &operator<<(ostream &os, pair<T, V> pr)
{
    // os << "{" << pr.first << ", " << pr.second << "}";
    os << pr.first << " " << pr.second;
    return os;
}

template <template <class, class> class Container, typename T>
ostream &operator<<(ostream &os, const Container<T, allocator<T>> &container)
{
    os << "[ ";
    for (auto el : container)
        os << el << " ";
    os << "]";
    return os;
}

template <typename Tuple, size_t... Is>
void print_tuple_helper(const Tuple& tup, index_sequence<Is...>)
{
    ((cout << (Is == 0 ? "" : ", ") << get<Is>(tup)), ...);
}

template <typename... Ts>
void print_tuple(const tuple<Ts...>& tup)
{
    cout << "(";
    print_tuple_helper(tup, index_sequence_for<Ts...>{});
    cout << ")";
}


void solve()
{

}

int main()
{
#ifndef ONLINE_JUDGE
    freopen("input.txt", "r", stdin);
    freopen("output.txt", "w", stdout);
#endif // ONLINE_JUDGE
    speed;
    
    ll test = 1;
    cin >> test;
    while (test--)
        solve();

    return 0;
}

/**
 * Sweep Line Algorithm
 * 
 * N buses
 * N timelines
 * 
 * Timetable
 * bus1     arrival time        departure time
 * bus2
 * ...
 * busN     arrival time N      departure time 
 * 
 * Q1
 *  Can a 2-buses bus station handle the timetable?
 * Q2
 *  What is he minimum number of buses that the station should be able to handle in order for it to be able to handle the given timetable?
*/


/**
 * How many different grays you have in your image
 * Your new image should have 4 colors
 * In a way to minimize the distortion of the image
 * 
 * Dada una imagen en escala de grises mapeala a una imagen en escala de grises con solo 4 grises
 *      Definimos una lista de 4 colores igualmente espaciados tomando el pixel mas claro y el pixel mas oscuro
 *      Performar un algoritmo de clustering KMeans
 *      Asignarle a cada cluster un color
 *      El color de cada cluster sera definido por el mas cercano de la lista de 4 colores a el centroide del cluster
 * 
 *      Quantization
 *          Discretization of the space
 *          The connection with the clustering is not directed
*/

