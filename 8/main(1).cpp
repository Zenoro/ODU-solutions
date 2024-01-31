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

vector <double> mulvm(vector <double>& vec, map<long long, map<long long, double>> x_rev, long long num_cells, map<long long, set<long long>> trans_rev)
{
    vector <double> res(num_cells, 0);
    for (long long m=1; m<=num_cells; m++) //выбор столбца матрицы (строки в обратной)
    {
        if (x_rev.count(m)==0)
        {
            res.push_back(0);
            continue;
        }
        double sum=0;
        for (set<long long>::iterator itc=trans_rev[m].begin(); itc!=trans_rev[m].end();itc++)//элементы вектора
        {
            sum+=vec[*itc]*x_rev[m][*itc];
        }
        res[m]=sum;
    }
    return res;
}

double scpr(vector <double>& v1, vector <double>& v2, long long num_cells)
{
    double res=0;
    for (long long i=1; i<=num_cells; i++)
    {
        res+=v1[i]*v2[i];
    }
    return res;
}

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

    double u=double(v);
    long long num_cells=(L/u)*(H/u);
    //cout<<num_cells<<endl;
    long long comps=0;
    map<long long, long long> global_colors; //Глобальный массив #если 2, то ячейка возвратная, если 0 - точно не возвратная
    map<long long, set<long long>> trans;
    map<long long, set<long long>> trans_rev;
    for (int it=1; it<=100; it++) //Итерации
    {
        //cout<<"===========ITERATION"<<it<<endl;
        comps=0;
        trans.clear();
        trans_rev.clear();
        map<long long, long long> global_colors_new; //Глобальный массив #если 2, то ячейка возвратная, если 0 - точно не возвратная
        for (long long cell=1; cell<=num_cells; cell++)//Перебор ячеек для построения симв образа
        {
            if (global_colors.count(cell)==1)
            {
                if (global_colors[cell]==0) continue;
            }
            double xc_0=x0+((cell-1)%int(L/u))*u;
            double yc_0=y0-floor((cell-1)/(L/u))*u;
            double du=double(u)/11;
            for (double i=du; i<u; i+=du)
            {
                for (double j=du; j<u; j+=du)
                {
                    double x_new=j_x(xc_0+i,yc_0-j,a);
                    double y_new=j_y(xc_0+i,yc_0-j,b);
                    long long new_cell=0;
                    if ((x_new<=x0) || (x_new>=x0+L)) continue;
                    if ((y_new>=y0) || (y_new<=y0-H)) continue;
                    if (((x_new-x0)/u==int((x_new-x0)/u)) || ((y_new-y0)/u==int((y_new-y0)/u))) continue; //попали на границу
                    else new_cell=L/u*floor((y0-y_new)/u)+ceil((x_new-x0)/u);
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
    //Инициализация матрицы мер
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
    /*for (int i=1; i<=num_cells; i++)
    {
        cout<<i<<" : ";
        for (set<long long>::iterator iter=trans_rev[i].begin(); iter!=trans_rev[i].end(); iter++)
        {
            cout<<*iter;
            cout<<" ";
        }
        cout<<endl;
    }*/
        //Начало алгоритма максимальной энтропии
    vector <double> r(num_cells+1, 1);
    for (long long i=0;i<MAXITER; i++) //Вычисление левого собственного вектора
    {
        r=mulvm(r,x_rev, num_cells, trans_rev);
        double vl=sqrt(scpr(r,r,num_cells));
        for (long long j=1;j<=num_cells; j++)
        {
            r[j]=r[j]/vl;
        }
    }
    vector <double> prom=mulvm(r,x_rev, num_cells, trans_rev);
    double maxlambda = scpr(r, prom, num_cells)/scpr(r,r,num_cells); //Макс собств значение
    cout<<"lambda_max = "<<maxlambda<<endl;
    map<long long, map<long long, double>> P_rev;
    for (long long i=1; i<=num_cells; i++)
    {
        if (x_rev.count(i)==0) continue;
        for (set<long long>::iterator itc=trans_rev[i].begin(); itc!=trans_rev[i].end();itc++)
        {
            P_rev[*itc][i]=x_rev[i][*itc]*r[*itc]/(maxlambda*r[i]);
        }
    }
    vector <double> m=r;
    double summ=0;
    for (long long i=0;i<MAXITER; i++)
    {
        summ=0;
        m=mulvm(m,P_rev, num_cells, trans);
        double vl=sqrt(scpr(m,m,num_cells));
        for (long long j=1;j<=num_cells; j++)
        {
            m[j]=m[j]/vl;
            summ+=m[j];
        }
    }
    for (long long j=1;j<=num_cells; j++)
    {
        m[j]=m[j]/summ;
    }
    map<long long, map<long long, double>> M;
    for (long long i=1; i<=num_cells; i++)
    {
        if (P_rev.count(i)==0) continue;
        for (set<long long>::iterator itc=trans[i].begin(); itc!=trans[i].end();itc++)
        {
            M[*itc][i]=P_rev[i][*itc]*m[*itc];
        }
    }
    time_t sec=time(NULL)-start;
    long long counter=0;
    ofstream fout;
    remove("res.txt");
    fout.open("res.txt");
    double sum1=0;
    double sum2=0;
    for (long long i=1; i<=num_cells; i++)
    {
        if (global_colors.count(i)==1)
        {
            if (global_colors[i]==2)
            {
                counter+=1;
                double mera=0;
                for (set<long long>::iterator itc=trans_rev[i].begin(); itc!=trans_rev[i].end(); itc++)
                {
                    if (global_colors.count(*itc)==0) continue;
                    if (global_colors[*itc]==0) continue;
                    mera+=M[i][*itc];
                    if (M[i][*itc]!=0) sum1+=M[i][*itc]*log(M[i][*itc]);
                    else sum1+=0;
                }
                if (mera!=0) sum2+=mera*log(mera);
                else sum2+=0;
                double xc_0=x0+((i-1)%int(L/u))*u;
                double yc_0=y0-floor((i-1)/(L/u))*u;
                fout<<xc_0<<" "<<yc_0<<" "<<mera<<endl;
            }
        }
    }
    fout<<u<<" "<<counter<<" "<<num_cells<<" "<<comps<<" "<<sec<<" "<<log(maxlambda) <<" "<<(-sum1+sum2);
    fout.close();
    cout<<"d = "<<u<<endl;
    cout<<"cells: "<<counter<<"/"<<num_cells<<endl;
    cout<<"components: "<<comps<<endl;
    cout<<"time all: "<<int(sec/60)<<" min "<<sec%60<<" sec"<<endl;
    cout<<"time cr: "<<int(cr/60)<<" min "<<cr%60<<" sec"<<endl;
    cout<<"log(lambda) "<<log(maxlambda)<<endl;
    cout<<"entropy "<<-sum1+sum2<<endl;
    // system("python draw.py");
    return 0;
}
