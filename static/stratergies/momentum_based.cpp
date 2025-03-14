#include <iterator>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
using namespace std;
struct Data{
    string date;
    double close;
};
void writeOrderStats(const vector<pair<string, string>> &orders) {
    ofstream file("order_statistics.csv");
    file << "Date,Action,Price,Position\n";
    for (const auto &order : orders) {
        file << order.first << "," << order.second << "\n";
    }
    file.close();
}
void writeCashflow(const vector<double> &cashflow) {
    ofstream file("daily_cashflow.csv");
    file << "Cashflow\n";
    for (const auto &flow : cashflow) {
        file << flow << "\n";
    }
    file.close();
}
class Momentum_Stratergy{
    public:
    void strat(vector<Data> data,int n,int x){
    int position = 0;
    vector<double> cashflow;
    vector<pair<string, string>> orders;
    for (int i = n; i < data.size(); ++i) {
        bool increasing = false, decreasing = false;
        for (int j = i - n; j < i - 1; ++j) {
            if (data[j].close >= data[j + 1].close) {
                decreasing = true;
            }
            if (data[j].close <= data[j + 1].close) {
                increasing = true;
            }
        }
        if (increasing && position < x) {
            // Buy 1 share
            position++;
            cashflow.push_back(-data[i].close);
            orders.push_back({data[i].date, "BUY," + to_string(data[i].close) + "," + to_string(position)});
        } else if (decreasing && position > -x) {
            // Sell 1 share
            position--;
            cashflow.push_back(data[i].close);
            orders.push_back({data[i].date, "SELL," + to_string(data[i].close) + "," + to_string(position)});
        }
    }
    writeCashflow(cashflow);
    writeOrderStats(orders);
        }
};
int main(){
    vector<Data> data;
    fstream file;
    file.open("stock_data.csv",ios::in);
    vector<string> row;
    string s,line,word;
    getline(file,line);
    while (getline(file, line))
    {
        row.clear();
        stringstream s(line);
        while (getline(s, word, ','))
        {
            row.push_back(word);
        }
        data.push_back({row[0],stod(row[7])});
    }
    Momentum_Stratergy strat;
   strat.strat(data,5,2);
    
}