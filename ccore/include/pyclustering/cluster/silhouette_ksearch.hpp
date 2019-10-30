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


#include <pyclustering/cluster/silhouette.hpp>
#include <pyclustering/cluster/silhouette_ksearch_data.hpp>


namespace pyclustering {

namespace clst {


class silhouette_ksearch_allocator {
public:
    using ptr = std::shared_ptr<silhouette_ksearch_allocator>;

public:
    virtual ~silhouette_ksearch_allocator() = default;

public:
    virtual void allocate(const std::size_t p_amount, const dataset & p_data, cluster_sequence & p_clusters) = 0;
};


class kmeans_allocator : public silhouette_ksearch_allocator {
public:
    virtual void allocate(const std::size_t p_amount, const dataset & p_data, cluster_sequence & p_clusters) override;
};

class kmedians_allocator : public silhouette_ksearch_allocator {
public:
    virtual void allocate(const std::size_t p_amount, const dataset & p_data, cluster_sequence & p_clusters) override;
};

class kmedoids_allocator : public silhouette_ksearch_allocator {
public:
    virtual void allocate(const std::size_t p_amount, const dataset & p_data, cluster_sequence & p_clusters) override;
};


class silhouette_ksearch {
private:
    std::size_t m_kmin;
    std::size_t m_kmax;
    silhouette_ksearch_allocator::ptr m_allocator = std::make_shared<kmeans_allocator>();

public:
    silhouette_ksearch() = default;

    silhouette_ksearch(const std::size_t p_kmin, const std::size_t p_kmax, const silhouette_ksearch_allocator::ptr & p_allocator = std::make_shared<kmeans_allocator>());

    silhouette_ksearch(const silhouette_ksearch & p_other) = default;

    silhouette_ksearch(silhouette_ksearch && p_other) = default;

    ~silhouette_ksearch() = default;

public:
    void process(const dataset & p_data, silhouette_ksearch_data & p_result);
};

}

}