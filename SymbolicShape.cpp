#include <iostream>
#include <string.h>
#include <cmath>
#include <algorithm>
#include <vector>
#include <iterator>
using namespace std;

// representation coefficients
double a = 1.4;
double b = 0.3;

// X-representation
double xfunc (double x, double y)
{
    return (1+y-a*x*x);
}
//Y-representation
double yfunc (double x, double y)
{
    return (b*x);
}

//Cell-finder function
int cell(double xr, double yr, double x_left,double y_top,double x_right,double y_down,double h, int n)
{
        if(xr<x_left || xr>x_right || yr>y_top || yr<y_down) return 0;
        int nomer = floor((fabs(y_top-yr))/h)*n + (ceil ((fabs(x_left-xr))/h));
        if (xr==x_left) nomer++;
        if (yr==y_down) nomer-=n;
        return nomer;
}

int main (int argc, char** argv)
{
    double x0 = -1.5;   //x left
    double x1 = 1.5;    //x right
    double y0 = -1.5;   //y down
    double y1 = 1.5;    //y up
    double h =0.5;      //step
    int pt = 10;       // squrt of point number

    int k = 0;
    int counter = 1;
    double xrez, yrez, cellrez ;
    double xtemp = x0;
    double ytemp = y1;
    double xcikl = x0;
    double ycikl = y1;
    vector<int> cell_list;
    double leng = abs(x1 - x0) / h;
    while (ycikl > y0){
        while (xcikl < x1){
            for (int i=0;i<pt;i++) {
                for (int j=0;j<pt;j++){
                    xrez = xfunc(xtemp, ytemp);
                    yrez = yfunc(xtemp, ytemp);
                    xtemp += 1.0/pt*h;
                    cellrez = cell(xrez, yrez, x0,y1,x1,y0,h,leng);
                    if ((find(begin(cell_list), end(cell_list), cellrez) == end(cell_list)) && (cellrez != 0))
                        cell_list.push_back(cellrez);
                }
                xtemp = xcikl;
                ytemp -= 1.0/pt*h;
            }
            xcikl += h;
            xtemp = xcikl;
            ytemp = ycikl;
            sort(begin(cell_list), end(cell_list));
            cout<<counter<<": [";
            for (int jf=0;jf<cell_list.size();jf++)
                cout<<cell_list[jf]<<" ";
            cout<<"]\n";
            ++counter;
            cell_list.clear();
        }
    ycikl -= h;
    xcikl = x0;
    xtemp = xcikl;
    ytemp = ycikl;
    }
        return 0;
}
//by Zenoro