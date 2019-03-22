#pragma once


#include <vector>


namespace ccore {

namespace clst {


using silhouette_sequence      = std::vector<double>;


class silhouette_data {
private:
    silhouette_sequence m_scores;

public:
   const silhouette_sequence & get_score(void) const { return m_scores; }

    silhouette_sequence & get_score(void) { return m_scores; }
};


}

}