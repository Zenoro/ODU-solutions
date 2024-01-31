#include <iostream>
#include <set>
#include <map>
#include <iterator>
#include <utility>

using namespace std;

long long roundUp(double src)
{
    if (src == (long long)src)
        return (long long)src;
    else return ((long long)src + 1);
}

pair<double, double> func(double x, double y) {
	long long** m = new long long * [2];
	m[0] = new long long[2];
	m[1] = new long long[2];
	m[0][0] = 1;
	m[0][1] = -2;
	m[1][0] = 4;
	m[1][1] = -3;
	//int m[2][2] = { {1,-2}, {4,-3} };
	double x1 = m[0][0] * x + m[0][1] * y;
    double y1 = m[1][0] * x + m[1][1] * y;
	return make_pair(x1, y1);
}

pair<map<long long, set<long long>>, map<long long, set<long long>>> CalcSymbolicImage(double u_l, double u_r, double h_b, double h_t, double d_x, double d_y, long long N, pair<double, double> (*ptFunc)(double, double, double, double, double, double, double), double alpha, double beta, double gamma, double k, double B) {
	double l_x = u_r - u_l;
    double l_y = h_t - h_b;
    long long c_x = (int)(l_x / d_x);
    long long c_y = (int)(l_y / d_y);
    long long d_x_rand = 1000 * d_x;
	long long d_y_rand = 1000 * d_y;
    map<long long, set<long long>> graph, tgraph;
    for (long long i = 1; i <= c_x * c_y; i++)
    {
        long long row = roundUp((double)i / (double)c_x);
        long long column = i - (row - 1) * c_x;
        double x_tl = d_x * (column - 1) + u_l;
        double y_tl = (c_y - row + 1) * d_y + h_b;
        for (long long j = 1; j <= N; j++)
        {
			for (long long z = 1; z <= N; z++)
			{
				/*double x = x_tl + (double)(rand() % (d_x_rand - 1) + 1) / 1000.0;
				double y = y_tl - (double)(rand() % (d_y_rand - 1) + 1) / 1000.0;*/
				double x = x_tl + d_x * j / (sqrt(N) + 1);
				double y = y_tl - d_y * z / (sqrt(N) + 1);
				pair<double, double> p = ptFunc(x, y, alpha, beta, gamma, k, B);			
				double x1 = p.first;
				double y1 = p.second;
				double x_im = x1 - u_l;
				double y_im = h_t - y1;
				long long row1;
				long long column1;
				if (y_im == l_y)
					row1 = c_y;
				else
					row1 = (long long)((double)y_im / (double)d_y) + 1;
				if (x_im == l_x)
					column1 = c_x;
				else
					column1 = (long long)((double)x_im / (double)d_x) + 1;
				//cout << x1 << " " << y1 << endl;
				if (0 < row1 && row1 <= c_y && 0 < column1 && column1 <= c_x) {
					long long num = c_x * (row1 - 1) + column1;
					graph[i].insert(num);
					if (tgraph.find(num) != tgraph.end())
						tgraph[num].insert(i);
					else
					{
						set<long long> s;
						tgraph[num] = s;
						tgraph[num].insert(i);
					}
				}
			}
        }       
    }
	return make_pair(graph, tgraph);
}

/*int main()
{
	double u_l = -2.0;
	double u_r = 2.0;
	double h_b = -2.0;
	double h_t = 2.0;
	double d_x = 0.5;
	double d_y = 0.5;
	int N = 100;
	double l_x = u_r - u_l;
    double l_y = h_t - h_b;
    int c_x = (int)(l_x / d_x);
    int c_y = (int)(l_y / d_y);
	pair<double, double> (*ptFunc)(double, double) = NULL;
	ptFunc = &func;
	pair<map<int, set<int>>, map<int, set<int>>> graphs = CalcSymbolicImage(u_l, u_r, h_b, h_t, d_x, d_y, N, ptFunc);
	map<int, set<int>> graph = graphs.first;
	map<int, set<int>> tgraph = graphs.second;
    for (int i = 1; i <= c_x * c_y; i++)
	{
		cout << i << ": ";
        copy(graph[i].begin(), graph[i].end(), ostream_iterator<int>(cout, " "));
        cout << endl;
	}
    return 0;
}*/