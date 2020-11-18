/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <pyclustering/definitions.hpp>


namespace pyclustering {

namespace clst {


using silhouette_score_sequence = std::vector<double>;


/*!

@class    silhouette_ksearch_data silhouette_ksearch_data.hpp pyclustering/cluster/silhouette_ksearch_data.hpp

@brief    Defines result of silhouette K-search algorithm.

*/
class silhouette_ksearch_data {
private:
    std::size_t m_amount = 0;
    double      m_score  = 0;
    silhouette_score_sequence m_scores = { };

public:
    /*!
    
    @brief  Return optimal amount of clusters.

    @return Optimal amount of clusters.
    
    */
    const std::size_t get_amount() const;

    /*!

    @brief  Set optimal amount of clusters (this method is used by Silhouette K-search algorithm).

    @param[in] p_amount: optimal amount of clusters.

    */
    void set_amount(const std::size_t p_amount);

    /*!
    
    @brief  Returns optimal amount of clusters that has been found during the analysis.

    @return Optimal amount of clusters that has been found during the analysis.

    */
    const double get_score() const;

    /*!

    @brief  Set optimal amount of clusters that has been found during the analysis (this method is used by Silhouette K-search algorithm).

    @param[in] p_score: optimal amount of clusters that has been found during the analysis.

    */
    void set_score(const double p_score);

    /*!
    
    @brief  Returns constant reference to silhouette score for each K value (amount of clusters).

    @return Constant reference to silhouette score for each K value (amount of clusters).
    
    */
    const silhouette_score_sequence & scores() const;

    /*!

    @brief  Returns reference to silhouette score for each K value (amount of clusters).

    @return Reference to silhouette score for each K value (amount of clusters).

    */
    silhouette_score_sequence & scores();

public:
    /*!

    @brief    Compares Silhouette K-search results.

    @param[in] p_other: another Silhouette K-search result that is used for comparison.

    @return  Returns true if both objects are the same.

    */
    bool operator==(const silhouette_ksearch_data & p_other) const;
};


}

}