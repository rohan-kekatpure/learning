# ifndef _MOVIE_HPP
# define _MOVIE_HPP

# include <string>
# include <iostream>
using std::string;
using std::cout;
using std::endl;

class Movie {
    string name;
    string rating;
    unsigned int watched;

    public:
        Movie(string name, string rating, unsigned int watched)
            : name {name}, rating {rating}, watched {watched} {}
        
        string getName() const {return name;}        
        unsigned int getWatched() const {return watched;}
        void incrWatched() {watched++;}        
        void display() const {
            cout << "Movie(" << name << ", " << rating << ", " << watched << ")" << endl;
        };
};
# endif