#include <iostream>
#include <string>
 
using namespace std;
 
int main() {
 
    //暗号を入力
    cout << "Code : ";
 
    string s;
    getline(cin, s);
 
    //フラグに必ず含まれるアルファベットを入力
    cout << endl << "KeyWord : ";
 
    string key;
    getline(cin,key);

    int count;
 
    for (int a = 0;a < 26;a++){
        //一つずつずらす
        for (int i = 0;i < s.length();i++){
            if (s[i] >= 'a' && s[i] < 'z') s[i]++;
            else if (s[i] >= 'A' && s[i] < 'Z') s[i]++;
            else if (s[i] == 'z') s[i] = 'a';
            else if (s[i] == 'Z') s[i] = 'A';
            else ;
        }
        
        //キーが含まれていたらbreak
        if (s.find(key) != std::string::npos){
            count = a;
            break;   
        }
    }
 
    //答えを出力
    cout << endl << count;
    cout << endl << s << endl;
 
    return 0;
 
}