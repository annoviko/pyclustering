/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2019
* @copyright GNU Public License
*
* GNU_PUBLIC_LICENSE
*   pyclustering is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   pyclustering is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
*/

#pragma once


#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/cluster/elbow.hpp>
#include <pyclustering/cluster/kmeans_plus_plus.hpp>
#include <pyclustering/cluster/random_center_initializer.hpp>

#include <pyclustering/definitions.hpp>


/**
 *
 * @brief   Elbow result is returned by pyclustering_package that consist sub-packages and this enumerator provides
 *           named indexes for sub-packages.
 *
 */
enum elbow_package_indexer {
    ELBOW_PACKAGE_AMOUNT = 0,
    ELBOW_PACKAGE_WCE,
    ELBOW_PACKAGE_SIZE
};


/**
 *
 * @brief   Performs data analysis using Elbow method using center initializer that is specified by template.
 * @details Caller should destroy returned result by 'free_pyclustering_package'.
 *
 * @param[in] p_sample: input data for clustering.
 * @param[in] p_kmin: minimum amount of clusters that should be considered.
 * @param[in] p_kmax: maximum amount of clusters that should be considered.
 *
 * @return  Returns Elbow's analysis results as a pyclustering package [ [ amount of clusters ], [ within cluster errors (wce) ] ].
 *
 */
template <class type_initializer>
pyclustering_package * elbow_method(const pyclustering_package * const p_sample,
                                    const std::size_t p_kmin,
                                    const std::size_t p_kmax)
{
    pyclustering::dataset input_dataset;
    p_sample->extract(input_dataset);

    pyclustering::clst::elbow_data result;
    pyclustering::clst::elbow<type_initializer> solver(p_kmin, p_kmax);
    solver.process(input_dataset, result);

    pyclustering_package * package = new pyclustering_package(pyclustering_data_t::PYCLUSTERING_TYPE_LIST);
    package->size = ELBOW_PACKAGE_SIZE;
    package->data = new pyclustering_package * [ELBOW_PACKAGE_SIZE];

    std::vector<std::size_t> amount_cluters = { result.get_amount() };
    ((pyclustering_package **) package->data)[ELBOW_PACKAGE_AMOUNT] = create_package(&amount_cluters);
    ((pyclustering_package **) package->data)[ELBOW_PACKAGE_WCE] = create_package(&result.get_wce());

    return package;
}


/**
 *
 * @brief   Performs data analysis using Elbow method with K-Means++ center initialization to found out proper amount of clusters.
 * @details Caller should destroy returned result by 'free_pyclustering_package'.
 *
 * @param[in] p_sample: input data for clustering.
 * @param[in] p_kmin: minimum amount of clusters that should be considered.
 * @param[in] p_kmax: maximum amount of clusters that should be considered.
 *
 * @return  Returns Elbow's analysis results as a pyclustering package [ [ amount of clusters ], [ within cluster errors (wce) ] ].
 *
 */
extern "C" DECLARATION pyclustering_package * elbow_method_ikpp(const pyclustering_package * const p_sample, 
                                                                const std::size_t p_kmin, 
                                                                const std::size_t p_kmax);


/**
 *
 * @brief   Performs data analysis using Elbow method with random center initialization to found out proper amount of clusters.
 * @details Caller should destroy returned result by 'free_pyclustering_package'.
 *
 * @param[in] p_sample: input data for clustering.
 * @param[in] p_kmin: minimum amount of clusters that should be considered.
 * @param[in] p_kmax: maximum amount of clusters that should be considered.
 *
 * @return  Returns Elbow's analysis results as a pyclustering package [ [ amount of clusters ], [ within cluster errors (wce) ] ].
 *
 */
extern "C" DECLARATION pyclustering_package * elbow_method_irnd(const pyclustering_package * const p_sample, 
                                                                const std::size_t p_kmin, 
                                                                const std::size_t p_kmax);
