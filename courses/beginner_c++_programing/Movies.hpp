# ifndef _MOVIES_HPP
# define _MOVIES_HPP

# include <string>
# include <vector>
# include "Movie.hpp"

using std::string;
using std::vector;

class Movies {
    vector<Movie> movieList;
     public:
        void addMovie(string name, string rating, unsigned int watched);
        void incrWatched(string name); 
        void display() const;
};
# endif