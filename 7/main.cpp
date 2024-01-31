#include <math.h>
#include <iostream>
#include <ctime>
#include <map>
#include <set>
#include <cstdio>
#include <vector>
#include <fstream>

//#define x0 -2
//#define y0 2

//#define L 4 //wtf chel oblast1 delaet kak dlinnu
//#define H 4
#define v 2
//#define a 0.3
//#define b 0.2

//#define scale 200
//#define iterations 8//10
#define MAXITER 20

using namespace std;

map<long long,set<long long>> g;
map<long long,set<long long>> gr;
vector<char> used;
vector<long long> order, component;

double j_x(double x, double y, double a)
{
    return x*x-y*y+a;
}

double j_y(double x, double y, double b)
{
    return 2*x*y+b;
}

void dfs1 (long long v1) {
	used[v1] = true;
	for (set<long long>::iterator i=g[v1].begin(); i!=g[v1].end(); ++i)
		if (!used[ *i ])
			dfs1 (*i);
	order.push_back (v1);
}

void dfs2 (long long v1) {
	used[v1] = true;
	component.push_back (v1);
	for (set<long long>::iterator i=gr[v1].begin(); i!=gr[v1].end(); ++i)
		if (!used[ *i ])
			dfs2 (*i);
}

int main(int argc, char** argv)
{
    time_t start=time(NULL);

    int x0 = atoi(argv[1]);
    int y0 = atoi(argv[2]);
    int L = atoi(argv[3]);
    int H = atoi(argv[4]);
    double a = atof(argv[5]);
    double b = atof(argv[6]);
    int iterations = atoi(argv[7]);

    //======================================================================

    double u=double(v);
    long long num_cells=(L/u)*(H/u);
    //cout<<num_cells<<endl;
    long long comps=0;
    map<long long, long long> global_colors;
    map<long long, set<long long>> trans;
    map<long long, set<long long>> trans_rev;
    for (int it=1; it<=100; it++)
    {
        //cout<<"===========ITERATION"<<it<<endl;
        comps=0;
        trans.clear();
        trans_rev.clear();
        map<long long, long long> global_colors_new;
        for (long long cell=1; cell<=num_cells; cell++) {
            if (global_colors.count(cell)==1) {
                if (global_colors[cell]==0)
                    continue;
            }
            double xc_0=x0+((cell-1)%int(L/u))*u;
            double yc_0=y0-floor((cell-1)/(L/u))*u;
            double du=double(u)/11;
            for (double i=du; i<u; i+=du)
            {
                for (double j=du; j<u; j+=du)
                {
                    double x_new=j_x(xc_0+i,yc_0-j, a);
                    double y_new=j_y(xc_0+i,yc_0-j, b);
                    long long new_cell=0;
                    if ((x_new<=x0) || (x_new>=x0+L))
                        continue;
                    if ((y_new>=y0) || (y_new<=y0-H))
                        continue;
                    if (((x_new-x0)/u==int((x_new-x0)/u)) || ((y_new-y0)/u==int((y_new-y0)/u))) 
                        continue;
                    else 
                        new_cell=L/u*floor((y0-y_new)/u)+ceil((x_new-x0)/u);
                    if (new_cell!=0)
                    {
                        trans[cell].insert(new_cell);
                        trans_rev[new_cell].insert(cell);
                    }
                }
            }
        }
        //cout<<"Simv obraz +"<<endl;
        g=trans;
        gr=trans_rev;
        long long n=num_cells;
        used.assign (n+1, false);
        for (long long i=1; i<=n; ++i)
            if (!used[i])
                dfs1 (i);
        used.assign (n+1, false);
        for (long long i=1; i<=n; ++i) {
            long long v1 = order[n-i];
            if (!used[v1]) {
                dfs2 (v1);
                int flag=0;
                if (component.size()==1)
                {
                    long long cll=component.at(0);
                    for (set<long long>::iterator itc=trans[cll].begin(); itc!=trans[cll].end(); itc++ )
                    {
                        if (*itc==cll)
                        {
                            flag=1;
                            break;
                        }
                    }
                }
                if ((component.size()>1) || flag==1)
                {
                    comps++;
                    for (vector<long long>::iterator itc = component.begin(); itc!=component.end(); itc++)
                    {
                        global_colors[*itc]=2;
                    }
                }
                component.clear();
            }
        }
        for (long long i=1; i<=num_cells; i++)
        {
            if (global_colors.count(i)==0)
            {
                global_colors_new[int((i-1)/(L/u))*(L/u)*4+2*((i-1)%int(L/u))+1]=0;
                global_colors_new[int((i-1)/(L/u))*(L/u)*4+2*((i-1)%int(L/u))+2]=0;
                global_colors_new[int((i-1)/(L/u))*(L/u)*4+(2*L/u)+2*((i-1)%int(L/u))+1]=0;
                global_colors_new[int((i-1)/(L/u))*(L/u)*4+(2*L/u)+2*((i-1)%int(L/u))+2]=0;
            }
            if (global_colors.count(i)==1)
            {
                if (global_colors[i]==0)
                {
                    global_colors_new[int((i-1)/(L/u))*(L/u)*4+2*((i-1)%int(L/u))+1]=0;
                    global_colors_new[int((i-1)/(L/u))*(L/u)*4+2*((i-1)%int(L/u))+2]=0;
                    global_colors_new[int((i-1)/(L/u))*(L/u)*4+(2*L/u)+2*((i-1)%int(L/u))+1]=0;
                    global_colors_new[int((i-1)/(L/u))*(L/u)*4+(2*L/u)+2*((i-1)%int(L/u))+2]=0;
                    continue;
                }
            }
        }
        if (it==iterations) break;
        u=u/2;
        global_colors=global_colors_new;
        used.clear();
        order.clear();
        num_cells*=4;
    }
    time_t cr=time(NULL)-start;
    map<long long, map<long long, double>> x;
    map<long long, map<long long, double>> x_rev;
    for (int i=1; i<=num_cells;i++)
    {
        if (global_colors.count(i)==0)
        {
            trans.erase(i);
            trans_rev.erase(i);
            continue;
        }
        if (global_colors[i]==0)
        {
            trans.erase(i);
            trans_rev.erase(i);
            continue;
        }
        for (set<long long>::iterator its=trans[i].begin(); its!=trans[i].end(); its++)
        {
            if (global_colors.count(*its)==0)
            {
                trans[i].erase(*its);
                continue;
            }
            if (global_colors[*its]==0)
            {
                trans[i].erase(*its);
                continue;
            }
            x[i][*its]=1;
        }
        for (set<long long>::iterator its=trans_rev[i].begin(); its!=trans_rev[i].end(); its++)
        {
            if (global_colors.count(*its)==0)
            {
                trans_rev[i].erase(*its);
                continue;
            }
            if (global_colors[*its]==0)
            {
                trans_rev[i].erase(*its);
                continue;
            }
            x_rev[i][*its]=1;
        }
    }
    map<long long, map<long long, double>> x2=x;
    map<long long, map<long long, double>> x2_rev=x_rev;
    for (int j=0; j<MAXITER; j++)
    {
        double sum=0;
        double sum_=0;
        for (int i=1; i<=num_cells;i++) {
            if (trans.count(i)==0) continue;
            for (set<long long>::iterator its=trans[i].begin(); its!=trans[i].end(); its++)
            {
                sum+=x[i][*its];
            }
        }
        for (int i=1; i<=num_cells;i++) {
            if (trans.count(i)==0) continue;
            for (set<long long>::iterator its=trans[i].begin(); its!=trans[i].end(); its++)
            {
                sum_+=x2[i][*its];
            }
        }
        for (int i=1; i<=num_cells;i++) {
            if (trans.count(i)==0) continue;
            for (set<long long>::iterator its=trans[i].begin(); its!=trans[i].end(); its++)
            {
                x[i][*its]=x[i][*its]/sum;
                x_rev[*its][i]=x_rev[*its][i]/sum;
            }
        }
        for (int i=1; i<=num_cells;i++) {
            if (trans.count(i)==0) continue;
            for (set<long long>::iterator its=trans[i].begin(); its!=trans[i].end(); its++)
            {
                x2[i][*its]=x2[i][*its]/sum_;
                x2_rev[*its][i]=x2_rev[*its][i]/sum_;
            }
        }
        map<long long, map<long long, double>> x_new;
        map<long long, map<long long, double>> x_new_rev;
        map<long long, map<long long, double>> x2_new;
        map<long long, map<long long, double>> x2_new_rev;
        for (int i=1; i<=num_cells;i++) {
            if (trans.count(i)==0) continue;
            double sum1=0;
            double sum2=0;
            for (set<long long>::iterator k=trans_rev[i].begin(); k!=trans_rev[i].end(); k++)
            {
                if (*k==i) continue;
                sum1+=x_rev[i][*k];
            }
            for (set<long long>::iterator l=trans[i].begin(); l!=trans[i].end(); l++)
            {
                if (*l==i) continue;
                sum2+=x[i][*l];
            }
            double sm=sqrt(sum1/sum2);
            for (set<long long>::iterator its=trans[i].begin(); its!=trans[i].end(); its++)
            {
                if (i==*its)
                {
                    x_new[i][i]=x[i][i];
                    x_new_rev[i][i]=x_rev[i][i];
                }
                else
                {
                    x_new[i][*its]=x[i][*its]*sm;
                    x_new_rev[*its][i]=x_rev[*its][i]*sm;
                }
            }
        }
        for (int i=1; i<=num_cells;i++) {
            if (trans.count(i)==0) continue;
            double sum1=0;
            double sum2=0;
            for (set<long long>::iterator l=trans[i].begin(); l!=trans[i].end(); l++)
            {
                if (*l==i) continue;
                sum1+=x2[i][*l];
            }
            for (set<long long>::iterator m=trans_rev[i].begin(); m!=trans_rev[i].end(); m++)
            {
                if (*m==i) continue;
                sum2+=x2_rev[i][*m];
            }
            double sm=sqrt(sum1/sum2);
            for (set<long long>::iterator its=trans_rev[i].begin(); its!=trans_rev[i].end(); its++)
            {
                if (i==*its)
                {
                    x2_new[i][i]=x2[i][i];
                    x2_new_rev[i][i]=x2_rev[i][i];
                }
                else
                {
                    x2_new[*its][i]=x[*its][i]*sm;
                    x2_new_rev[i][*its]=x_rev[i][*its]*sm;
                }
            }
        }
        x=x_new;
        x_rev=x_new_rev;
        x2=x2_new;
        x2_rev=x2_new_rev;
    }
    time_t sec=time(NULL)-start;

    ofstream fout;
    remove("res.txt");
    fout.open("res.txt");
    long long counter=0;
    for (long long i=1; i<=num_cells; i++)
    {
        if (global_colors.count(i)==1)
        {
            if (global_colors[i]==2)
            {
                counter+=1;
                double mera=0;
                double mera2=0;
                for (set<long long>::iterator itc=trans[i].begin(); itc!=trans[i].end(); itc++)
                {
                    if (global_colors.count(*itc)==0) continue;
                    if (global_colors[*itc]==0) continue;
                    mera+=x[i][*itc];
                    mera2+=x2[i][*itc];
                }
                double xc_0=x0+((i-1)%int(L/u))*u;
                double yc_0=y0-floor((i-1)/(L/u))*u;
                cout<<mera<<" "<<mera2<<endl;
                fout<<xc_0<<" "<<yc_0<<" "<<mera<<endl;
            }
        }
    }
    fout<<u<<" "<<counter<<" "<<num_cells<<" "<<comps<<" "<<sec;
    fout.close();
    cout<<"cells: "<<counter<<"/"<<num_cells<<endl;
    cout<<"components: "<<comps<<endl;
    cout<<"time all: "<<int(sec/60)<<" min "<<sec%60<<" sec"<<endl;
    cout<<"time cr: "<<int(cr/60)<<" min "<<cr%60<<" sec"<<endl;
    //system("python draw.py");
    return 0;
}

