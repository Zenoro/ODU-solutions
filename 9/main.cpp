#include <math.h>
#include <iostream>
#include <ctime>
#include <map>
#include <set>
#include <vector>
#include <deque>
#include <fstream>

#define v 2 //Размер клетки исходного разбиения

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

double func_osn(double x, double y)
{
    return x*x + y*y;
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

int searchtree(map<long long, vector<long long>> Tree, long long i2, long long i1, map <long long, long long> &newcycle)
{
    if (i2==i1) return 1;
    int res=0;
    for (vector<long long>::iterator itv=Tree[i2].begin();itv!=Tree[i2].end(); itv++)
    {
        res=searchtree(Tree, *itv, i1, newcycle);
        if (res==1)
        {
            newcycle[i2]=*itv;
            return 1;
        }
    }
    return 0;
}

int main(int argc, char** argv)
{
    // wnd.lpszClassName = "class";
    // wnd.lpfnWndProc = DefWindowProcA;
    // wnd.hCursor = LoadCursor(0, IDC_ARROW);
    // RegisterClassA(&wnd);

    time_t start = time(NULL);

    double x0 = atof(argv[1]);
    double y0 = atof(argv[2]);
    double L = atof(argv[3]);
    double H = atof(argv[4]);
    double a = atof(argv[5]);
    double b = atof(argv[6]);
    int iterations = atoi(argv[7]);

    double u = double(v);
    long long num_cells = (L/u) * (H/u);
    long long comps = 0;
    map<long long, long long> global_colors; //Глобальный массив #если 2, то ячейка возвратная, если 0 - точно не возвратная
    ofstream fout("res.txt");
    for (int it = 1; it <= 100; it++) //ИТЕРАЦИИ
    {
        //cout<<"===========ITERATION"<<it<<endl;
        comps = 0;
        map<long long, set<long long>> trans;
        map<long long, set<long long>> trans_rev;
        map<long long, long long> global_colors_new; //Глобальный массив #если 2, то ячейка возвратная, если 0 - точно не возвратная
        map<long long, double> C; //Оснащение графа
        for (long long cell=1; cell<=num_cells; cell++)//Перебор ячеек для построения симв образа
        {
            if (global_colors.count(cell) == 1)
            {
                if (global_colors[cell] == 0) continue;
            }
            double xc_0 = x0 + ((cell-1)%int(L/u)) * u;
            double yc_0 = y0 - floor((cell-1)/(L/u)) * u;
            C[cell] = func_osn(xc_0+u/2,yc_0-u/2);
            //cout<<"osn "<<cell<<"="<<C[cell]<<" coords "<<xc_0+u/2<<" "<<yc_0-u/2<<endl;
            double du = double(u)/11;
            for (double i=du; i<u; i+=du)
            {
                for (double j=du; j<u; j+=du)
                {
                    double x_new = j_x(xc_0 + i, yc_0 - j, a);
                    double y_new = j_y(xc_0 + i, yc_0 - j, b);
                    long long new_cell = 0;
                    if ((x_new <= x0) or (x_new >= x0 + L)) continue;
                    if ((y_new >= y0) or (y_new <= y0 - H)) continue;
                    if (((x_new - x0)/u == int((x_new - x0 )/u)) or 
                    ((y_new - y0)/u == int((y_new - y0)/u))) continue; //попали на границу
                    else new_cell = L / u * floor((y0-y_new)/u) + ceil((x_new-x0)/u);
                    if (new_cell != 0)
                    {
                            trans[cell].insert(new_cell);
                            trans_rev[new_cell].insert(cell);
                    }
                }
            }
        }
        //cout<<"Simv obraz +"<<endl;
        for (long long i = 1; i <= num_cells; i++)
        {
            //cout<<i<<": ";
            //for (set<long long>::iterator itc=trans[i].begin(); itc!=trans[i].end(); itc++ ) cout<<*itc<<" ";
            //cout<<endl;
        }
        g = trans;
        gr = trans_rev;
        long long n = num_cells;
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
                if (component.size() == 1)
                {
                    long long cll=component.at(0);
                    for (set<long long>::iterator itc=trans[cll].begin(); itc!=trans[cll].end(); itc++ )
                    {
                        if (*itc==cll)
                        {
                            flag = 1;
                            break;
                        }
                    }
                }
                if ((component.size()>1) or flag==1)
                {
                    comps++;
                    for (vector<long long>::iterator itc = component.begin(); itc!=component.end(); itc++)
                    {
                        global_colors[*itc]=2;
                    }
                    if (it==iterations)
                    {
                        //Алгоритм Романовского
                        //Поиск начального цикла
                        map<long long, long long> Nz; //N*
                        vector<long long> Mz=component; //M*
                        map<long long, long long> Stv; //Степени вершин
                        for (vector<long long>::iterator itv = component.begin(); itv!=component.end(); itv++) //Подсчет дуг
                        {
                            if (Stv.count(*itv)==0) Stv[*itv]=0;
                            long long to=0;
                            for (vector<long long>::iterator its = component.begin(); its!=component.end(); its++)
                            {
                                if (trans[*itv].count(*its)>0)
                                {
                                    Nz[*itv]=*its;
                                    to=*its;
                                    break;
                                }
                            }
                            for (vector<long long>::iterator itmz=Mz.begin();itmz!=Mz.end(); itmz++) //Удаление из M* с ненул степ
                            {
                                if (*itmz==to)
                                {
                                    Mz.erase(itmz);
                                    break;
                                }
                            }
                            if (Stv.count(to)==0) Stv[to]=0;
                            Stv[to]+=1;
                        }
                        while (Mz.size()!=0)
                        {
                            long long i1=Mz[0];
                            long long i2=Nz[i1];
                            Mz.erase(Mz.begin());
                            Nz.erase(i1);
                            Stv[i2]-=1;
                            if (Stv[i2]==0) Mz.push_back(i2);
                        }
                        //Выбираем лучший цикл
                        map<long long, long long> curcycle;
                        map<long long, long long> initmaxcycle;
                        map<long long, long long> initmincycle;
                        double bestmaxscore=0;
                        double bestminscore=0;
                        int flag=0;
                        for (map<long long, long long>::iterator itm=Nz.begin(); itm!=Nz.end();itm++)
                        {
                            long long start_cell=itm->first;
                            long long cur_cell=itm->second;
                            //cout<<start_cell<<" "<<cur_cell<<endl;
                            long long csize=1;
                            double sumosn=C[start_cell];
                            curcycle.clear();
                            curcycle[start_cell]=cur_cell;
                            while (cur_cell!=start_cell)
                            {
                                csize+=1;
                                sumosn+=C[cur_cell];
                                curcycle[cur_cell]=Nz[cur_cell];
                                cur_cell=Nz[cur_cell];
                            }
                            if ((flag==0) or ((sumosn/csize)<bestminscore))
                            {
                                bestminscore=(sumosn/csize);
                                initmincycle.clear();
                                initmincycle=curcycle;
                            }
                            if ((flag==0) or ((sumosn/csize)>bestmaxscore))
                            {
                                bestmaxscore=(sumosn/csize);
                                initmaxcycle.clear();
                                initmaxcycle=curcycle;
                            }
                            curcycle.clear();
                            if (flag==0) flag=1;
                        }
                        //Найден начальный цикл
                        //initmaxcycle - начальный цикл максимума
                        //initmincycle - начальный цикл минимума

                        //Промеж вывод
                        //cout<<"maxcycle"<<endl;
                        //cout<<bestmaxscore<<endl;
                        for (map<long long, long long>::iterator itm=initmaxcycle.begin(); itm!=initmaxcycle.end();itm++)
                        {
                            long long start_cell=itm->first;
                            long long cur_cell=itm->second;
                            //cout<<start_cell<<" "<<cur_cell<<endl;
                        }
                        //cout<<"mincycle"<<endl;
                        //cout<<bestminscore<<endl;
                        for (map<long long, long long>::iterator itm=initmincycle.begin(); itm!=initmincycle.end();itm++)
                        {
                            long long start_cell=itm->first;
                            long long cur_cell=itm->second;
                            //cout<<start_cell<<" "<<cur_cell<<endl;
                        }
                        //Теперь сам алгоритм Романовского (для минимума)
                        while(true)
                        {
                            //cout<<"global cycle"<<endl;
                            map<long long, double> V;
                            set<long long> M0;
                            deque<long long> M1;
                            set<long long> M2;
                            for (vector<long long>::iterator itv = component.begin(); itv!=component.end(); itv++) //Заполнение M2
                            {
                                M2.insert(*itv);
                            }
                            map<long long, vector<long long>> Tree;
                            long long startver=(initmincycle.begin())->first;
                            long long curver=startver;
                            V[startver]=0;
                            M1.push_back(startver);
                            M2.erase(startver);
                            //**Подсчет z=bestminscore на цикле
                            long long cur_cell=initmincycle[startver];
                            long long csize=1;
                            double sumosn=C[startver];
                            while (cur_cell!=startver)
                            {
                                csize+=1;
                                sumosn+=C[cur_cell];
                                cur_cell=initmincycle[cur_cell];
                            }
                            bestminscore=(sumosn/csize);
                            //**
                            while(true)
                            {
                                long long newcurver=initmincycle[curver];
                                if (newcurver==curver) break;
                                if (newcurver==startver) break;
                                Tree[curver].push_back(newcurver);
                                M1.push_back(newcurver);
                                M2.erase(newcurver);
                                V[newcurver]=C[curver]-bestminscore+V[curver];
                                curver=newcurver;
                            }
                            initmincycle.erase(curver);
                            int flagg=0;
                            while (M1.size()!=0)//Главный цикл алгоритма
                            {
                                long long i1=M1[0];
                                M1.erase(M1.begin());
                                M0.insert(i1);
                                for (set<long long>::iterator i2=trans[i1].begin(); i2!=trans[i1].end(); i2++)
                                {
                                    if (*i2==startver) continue;
                                    double w=V[i1]+C[i1]-bestminscore;
                                    //cout<<"w from "<<i1<<" to "<<*i2<<" "<<w<<endl;
                                    if (M2.count(*i2)>0)
                                    {
                                        V[*i2]=w;
                                        Tree[i1].push_back(*i2);
                                        M2.erase(*i2);
                                        M1.push_back(*i2);
                                        //cout<<"M1 push back "<<*i2<<endl;
                                    }
                                    else if (w<V[*i2])
                                    {
                                        map<long long, long long> newcycle;
                                        int flag=searchtree(Tree, *i2, i1, newcycle);
                                        if (flag==1)
                                        {
                                            newcycle[i1]=*i2;
                                            flagg=1;
                                            initmincycle=newcycle;
                                            break;
                                        }
                                        else
                                        {
                                            for (map<long long, vector<long long>>::iterator imv=Tree.begin(); imv!=Tree.end(); imv++)
                                            {
                                                int fl=0;
                                                for (vector<long long>::iterator icc=(imv->second).begin(); icc!=(imv->second).end(); icc++)
                                                {
                                                    if ((*icc)==(*i2))
                                                    {
                                                        fl=1;
                                                        (imv->second).erase(icc);
                                                        if (M0.count(*i2)>0)
                                                        {
                                                            M0.erase(*i2);
                                                            M1.push_front(*i2);
                                                        }
                                                        break;
                                                    }
                                                }
                                                if (fl==1) break;
                                            }
                                        }
                                    }
                                }
                                //cout<<endl;
                                if (flagg==1) break;
                            }
                            if (flagg==1) continue;
                            break;

                        }
                        //Для максимума
                        while(true)
                        {
                            //cout<<"global cycle"<<endl;
                            map<long long, double> V;
                            set<long long> M0;
                            deque<long long> M1;
                            set<long long> M2;
                            for (vector<long long>::iterator itv = component.begin(); itv!=component.end(); itv++) //Заполнение M2
                            {
                                M2.insert(*itv);
                            }
                            map<long long, vector<long long>> Tree;
                            long long startver=(initmaxcycle.begin())->first;
                            long long curver=startver;
                            V[startver]=0;
                            M1.push_back(startver);
                            M2.erase(startver);
                            //**Подсчет z=bestmaxscore на цикле
                            long long cur_cell=initmaxcycle[startver];
                            long long csize=1;
                            double sumosn=C[startver];
                            while (cur_cell!=startver)
                            {
                                csize+=1;
                                sumosn+=C[cur_cell];
                                cur_cell=initmaxcycle[cur_cell];
                            }
                            bestmaxscore=(sumosn/csize);
                            //**
                            while(true)
                            {
                                long long newcurver=initmaxcycle[curver];
                                if (newcurver==curver) break;
                                if (newcurver==startver) break;
                                Tree[curver].push_back(newcurver);
                                M1.push_back(newcurver);
                                M2.erase(newcurver);
                                V[newcurver]=C[curver]-bestmaxscore+V[curver];
                                curver=newcurver;
                            }
                            initmaxcycle.erase(curver);
                            int flagg=0;
                            while (M1.size()!=0)//Главный цикл алгоритма
                            {
                                long long i1=M1[0];
                                M1.erase(M1.begin());
                                M0.insert(i1);
                                for (set<long long>::iterator i2=trans[i1].begin(); i2!=trans[i1].end(); i2++)
                                {
                                    if (*i2==startver) continue;
                                    double w=V[i1]+C[i1]-bestmaxscore;
                                    //cout<<"w from "<<i1<<" to "<<*i2<<" "<<w<<endl;
                                    if (M2.count(*i2)>0)
                                    {
                                        V[*i2]=w;
                                        Tree[i1].push_back(*i2);
                                        M2.erase(*i2);
                                        M1.push_back(*i2);
                                        //cout<<"M1 push back "<<*i2<<endl;
                                    }
                                    else if (w>V[*i2])
                                    {
                                        map<long long, long long> newcycle;
                                        int flag=searchtree(Tree, *i2, i1, newcycle);
                                        if (flag==1)
                                        {
                                            newcycle[i1]=*i2;
                                            flagg=1;
                                            initmaxcycle=newcycle;
                                            break;
                                        }
                                        else
                                        {
                                            for (map<long long, vector<long long>>::iterator imv=Tree.begin(); imv!=Tree.end(); imv++)
                                            {
                                                int fl=0;
                                                for (vector<long long>::iterator icc=(imv->second).begin(); icc!=(imv->second).end(); icc++)
                                                {
                                                    if ((*icc)==(*i2))
                                                    {
                                                        fl=1;
                                                        (imv->second).erase(icc);
                                                        if (M0.count(*i2)>0)
                                                        {
                                                            M0.erase(*i2);
                                                            M1.push_front(*i2);
                                                        }
                                                        break;
                                                    }
                                                }
                                                if (fl==1) break;
                                            }
                                        }
                                    }
                                }
                                //cout<<endl;
                                if (flagg==1) break;
                            }
                            if (flagg==1) continue;
                            break;

                        }
                        cout<<"component "<<comps<<" ["<<bestminscore<<" ; "<<bestmaxscore<<"]"<<endl;
                        fout<<"component "<<comps<<" ["<<bestminscore<<" ; "<<bestmaxscore<<"]"<<endl;
                        //Конец алгоритма Романовского
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
    time_t sec=time(NULL)-start;
    //рисование
    // hwnd = CreateWindow("class", "window", WS_OVERLAPPEDWINDOW, 20, 20, 800, 600, 0, 0, 0, 0);
    // dc = GetDC(hwnd);
    // ShowWindow(hwnd, SW_SHOWNORMAL);

    //делаем белый фон
    // SelectObject(dc, CreateSolidBrush(RGB(255,255,255)));
    // Rectangle(dc,0,0,800,600);
    // SelectObject(dc, CreateSolidBrush(RGB(0,0,0)));
    long long counter=0;
    for (long long i=1; i<=num_cells; i++)
    {
        if (global_colors.count(i)==1)
        {
            if (global_colors[i]==2)
            {
                counter++;
                // double xc_0=x0+((i-1)%int(L/u))*u;
                // double yc_0=y0-floor((i-1)/(L/u))*u;
                // Rectangle(dc, 320+(xc_0*scale), 240-(yc_0*scale), 320+((xc_0+u)*scale), 240-((yc_0-u)*scale));
                // SetPixel(dc, 320+(xc_0*scale), 240-(yc_0*scale), RGB(0,0,0));
            }
        }
    }
    // ofstream fd("res.txt");
    fout << u << " " << counter << " " << num_cells << " " << comps << " " << sec;
    // fd.close();
    fout.close();
    cout<<"u = "<<u<<endl;
    cout<<"cells: "<<counter<<"/"<<num_cells<<endl;
    cout<<"components: "<<comps<<endl;
    cout<<"time: "<<int(sec/60)<<" min "<<sec%60<<" sec"<<endl;
    // while(GetMessage(&msg,0,0,0)){
        // DispatchMessage(&msg);
    // }
    return 0;
}

