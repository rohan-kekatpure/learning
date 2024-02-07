# include <iostream>
# include "Movies.hpp"

using std::cout;
using std::cin;
using std::endl;
using std::vector;
using std::string;


int main() {
    Movies movies;
    movies.addMovie("Gunda", "R", 2500);
    movies.addMovie("Loha", "R", 203);
    movies.display();

    movies.incrWatched("Gunda");
    movies.display();

    movies.incrWatched("foo");
    movies.addMovie("Gunda", "R", 20);
    return 0;
}

