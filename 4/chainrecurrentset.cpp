#include <map>
#include <vector>
#include <iostream>
#include <set>
#include <cmath>
#include <fstream>
#include <chrono>
#include "symbolicimage_2.hpp"
//#include "symbolicimage.cpp"

// const long long DEPTH = 0;

using namespace std;

map<long long, set<long long>> graph, tgraph;
map<long long, long long> p;
vector<long long> used;
vector<long long> color, order;
set<long long> components_parts, component;

void dfs1 (long long v) {
	used[v] = true;
	for (auto node : graph[v])
	{
		if (!used[node])
			dfs1(node);
	}
	order.push_back(v);
}

void dfs2 (long long v) {
	used[v] = true;
	component.insert(v);
	for (auto node : tgraph[v])
	{
		if (!used[node])
			dfs2(node);
	}
}

double fy_2d (double x, double y, double t, double k, double alpha, double beta, double B, double h) {
	return -k * y + alpha * x + beta * x * x * x + B * cos(h * t);
}

double fx_2d (double y) {
	return y;
}

pair<double, double> duffing_func(double x1, double y1, double alpha, double beta, double omega, double k, double B) {
	long long num_iters = 30;
	// double k = 0.25;
	// double alpha = -1.0;
	// double beta = 1.0;
	// double omega = 1.0;
	// double B = 0.3;
	double x = x1;
	double y = y1;
	double k1, k2, k3, k4;
	double q1, q2, q3, q4;
	double d = 2 * M_PI / num_iters;
	double t = 0;
	for (long long i = 0; i < num_iters; i++) {
		k1 = fy_2d(x, y, t, k, alpha, beta, B, omega);
		q1 = fx_2d(y);
	
		k2 = fy_2d(x + d * q1 / 2.0, y + d * k1 / 2.0, t + d / 2.0, k, alpha, beta, B, omega);
		q2 = fx_2d(y + d * k1 / 2.0);
	
		k3 = fy_2d(x + d * q2 / 2.0, y + d * k2 / 2.0, t + d / 2.0, k, alpha, beta, B, omega);
		q3 = fx_2d(y + d * k2 / 2.0);
	
		k4 = fy_2d(x + d * q3, y + d * k3, t + d, k, alpha, beta, B, omega);
		q4 = fx_2d(y + d * k3);
	
		y += d * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0;
		x += d * (q1 + 2.0 * q2 + 2.0 * q3 + q4) / 6.0;
		t += d;
	}
	return make_pair(x, y);
}

int main(int argc, char** argv)
{
	auto begin = std::chrono::steady_clock::now();
	double u_l = atof(argv[1]);
	double u_r = atof(argv[2]);
	double h_b = atof(argv[3]);
	double h_t = atof(argv[4]);
	double d_x = atof(argv[5]);
	double DEPTH = atof(argv[6]);
	double alpha = atof(argv[7]);
	double beta = atof(argv[8]);
	double omega = atof(argv[9]);
	double k = atof(argv[10]);
	double B = atof(argv[11]);
	double d_y = d_x;
	long long N = 4;
	d_x /= pow(2, DEPTH);
	d_y /= pow(2, DEPTH);
	
	pair<double, double> (*ptFunc)(double, double, double, double, double, double, double) = NULL;
	ptFunc = &duffing_func;
	pair<map<long long, set<long long>>, map<long long, set<long long>>> graphs = CalcSymbolicImage(u_l, u_r, h_b, h_t, d_x, d_y, N, ptFunc, alpha, beta, omega, k, B);
	graph = graphs.first;
	tgraph = graphs.second;

	component.clear();
		
	long long n = (long long)(((u_r - u_l) / d_x)*((h_t - h_b) / d_y));
			
	used.assign(n + 1, false);
	for (long long i = 1; i <= n; i++)
		if (!used[i])
			dfs1(i);
	used.assign(n + 1, false);
	long long num_comps = 0;
	long long num_notonesize_comps = 0;
	for (long long i = 1; i <= n; i++)
	{
		long long v = order[n - i];
		if (!used[v])
		{
			dfs2(v);
			num_comps++;
			if (component.size() > 1)
			{
				num_notonesize_comps++;
				for (auto node : component)
				{
					components_parts.insert(node);
				}
			}
			component.clear();
		}
	}
	
	auto end = std::chrono::steady_clock::now();
	auto elapsed_ms = std::chrono::duration_cast<std::chrono::milliseconds>(end - begin);
	cout << DEPTH << " iterations" << endl;
	cout << "The time: " << elapsed_ms.count() << " ms" << endl;

	ofstream out;
    out.open("res.txt");
	if (out.is_open())
	{
		double l_x = u_r - u_l;
		double l_y = h_t - h_b;
		long long c_x = (long long)(l_x / d_x);
		long long c_y = (long long)(l_y / d_y);
		out << d_x << " " << d_y << endl;
		for (auto comp : components_parts)
		{
			long long row = roundUp((double)comp / (double)c_x);
			long long column = comp - (row - 1) * c_x;
			double x_tl = d_x * (column - 1) + u_l;
			double y_tl = (c_y - row + 1) * d_y + h_b;
			out << x_tl << " " << y_tl << endl;
		}
	}
	out.close();

	ofstream out_buf;
	out_buf.open("sys.out");
	out_buf << elapsed_ms.count() << " " << num_comps + num_notonesize_comps << endl;
	out_buf.close();

	cout << "num_comps: " << num_comps << " num_not_one_size_comps: " << num_notonesize_comps << endl;
}
