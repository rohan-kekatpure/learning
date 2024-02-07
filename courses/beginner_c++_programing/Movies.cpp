# include<iostream>
# include<string>
# include<vector>
# include "Movies.hpp"

using std::cout;
using std::endl;

void Movies::addMovie(string name, string rating, unsigned int watched) {
    for (const auto &movie: movieList) {
        if (movie.getName() == name) {
            cout << "Movie '" << name << "' already present" << endl;
            return; 
        }
    }
    movieList.push_back(Movie(name, rating, watched));
}

void Movies::incrWatched(string name) {
    for (auto &movie: movieList) {
        if (movie.getName() == name) {
            movie.incrWatched();
            return;
        }
    }
    cout << "Movie '" << name << "' not found" << endl;
}

void Movies::display() const {
    for (auto m: movieList) {
        m.display();
    }
}