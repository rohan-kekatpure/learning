# include<iostream>

class Foo
{
    private:
        int x, y;        
    public:
        int dist();        
        Foo(int x, int y);                
};

Foo::Foo(int a, int b) : x(a), y(b) {}

int Foo::dist(){
    int u, v;
    u = this->x;
    v = this->y;

    return u * u + v * v;
}

int main(int argc, char *argv[]){
    Foo f = Foo(1, 2);
    std::cout << f.dist() << std::endl;
}