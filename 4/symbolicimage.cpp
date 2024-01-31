#include <iostream>
#include <set>
#include <map>
#include <iterator>
#include <utility>

using namespace std;

int roundUp(double src)
{
    if (src == (int)src)
        return (int)src;
    else return ((int)src + 1);
}

pair<double, double> func(double x, double y) {
	int** m = new int * [2];
	m[0] = new int[2];
	m[1] = new int[2];
	m[0][0] = 1;
	m[0][1] = -2;
	m[1][0] = 4;
	m[1][1] = -3;
	//int m[2][2] = { {1,-2}, {4,-3} };
	double x1 = m[0][0] * x + m[0][1] * y;
    double y1 = m[1][0] * x + m[1][1] * y;
	return make_pair(x1, y1);
}

map<int, set<int>> CalcSymbolicImage(double a, double b, double c, double d, double h, int N, pair<double, double> (*ptFunc)(double, double)) {
	double len_x = b - a;
    double len_y = d - c;
    int l_x = (int)(len_x / h);
    int l_y = (int)(len_y / h);
    int h_rand = 1000 * h;
    map<int, set<int>> graph;
    for (int i = 1; i <= l_x*l_y; i++)
    {
		set<int> newset;
		graph[i] = newset;
        int row = roundUp((double)i / (double)l_x) - 1;
        int column = i - row * l_x - 1;
        double x_tl = h * column + a;
        double y_tl = (l_y - row) * h + c;
        for (int j = 0; j < N; j++)
        {
            double x = x_tl + (double)(rand() % (h_rand - 1) + 1) / 1000.0;
            double y = y_tl - (double)(rand() % (h_rand - 1) + 1) / 1000.0;            
            pair<double, double> p = ptFunc(x, y);			
            double x1 = p.first;
			double y1 = p.second;
            int row1 = l_y - roundUp((y1 + len_y/2) / h);
            int column1 = (int)((x1 + len_x/2) / h);
            if (0 <= row1 && row1 < l_y && 0 <= column1 && column1 < l_x)
            {
                int num = l_x * row1 + column1 + 1;
                graph[i].insert(num);
            }
        }
    }
	return graph;
}

/*int main()
{
	double a = -2.0;
	double b = 2.0;
	double c = -2.0;
	double d = 2.0;
	int N = 100;
	double h = 0.5;
	double len_x = b - a;
    double len_y = d - c;
	int l_x = (int)(len_x / h);
    int l_y = (int)(len_y / h);
	pair<double, double> (*ptFunc)(double, double) = NULL;
	ptFunc = &func;
	map<int, set<int>> graph = CalcSymbolicImage(a, b, c, d, h, N, ptFunc);
    for (int i = 1; i <= l_x * l_y; i++)
	{
		cout << i << ": ";
        copy(graph[i].begin(), graph[i].end(), ostream_iterator<int>(cout, " "));
        cout << endl;
	}
    return 0;
}*/