/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    pyclustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pyclustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

*/


#include <gtest/gtest.h>

#include "samples.hpp"

#include <pyclustering/container/kdtree.hpp>
#include <pyclustering/container/kdtree_searcher.hpp>

#include <pyclustering/utils/metric.hpp>

#include <algorithm>
#include <numeric>


using namespace pyclustering;
using namespace pyclustering::container;
using namespace pyclustering::utils::metric;


class utest_kdtree : public ::testing::Test {
protected:
    virtual void SetUp() { }

    virtual void TearDown() { }

protected:
    virtual void InitTestObject(const dataset & points) {
        tree = kdtree();
        for (auto & point : points) {
            tree.insert(point);
        }
    }

    virtual void TemplateTestBalancedFind(const dataset & p_data) {
        std::vector<void *> payload;
        for (std::size_t i = 0; i < p_data.size(); i++) {
            payload.push_back((void *)i);
        }

        tree = kdtree(p_data, payload);

        ASSERT_NE(nullptr, tree.get_root());
        ASSERT_EQ(p_data.size(), tree.get_size());

        for (std::size_t i = 0; i < p_data.size(); i++) {
            kdnode::ptr node = tree.find_node(p_data[i], payload[i]);

            ASSERT_NE(nullptr, node);
            ASSERT_EQ(p_data[i], node->get_data());
            ASSERT_EQ(payload[i], node->get_payload());
        }
    }

    virtual void TemplateTestBalancedSearch(const dataset & p_data, const double p_radius_search = 10.0) {
        std::vector<void *> payload;
        for (std::size_t i = 0; i < p_data.size(); i++) {
            payload.push_back((void *) i);
        }

        tree = kdtree(p_data, payload);

        ASSERT_NE(nullptr, tree.get_root());
        ASSERT_EQ(p_data.size(), tree.get_size());

        for (std::size_t i = 0; i < p_data.size(); i++) {
            searcher = kdtree_searcher(p_data[i], tree.get_root(), p_radius_search);
            
            FindNearestNode(p_data, i);         /* Find the nearest node */
            FindNearestNeighbors(p_data, i);    /* Find the nearest neighbors */

            /* Find nearest using user-specific rule to store result */
            std::vector<std::size_t> index_points;
            kdtree_searcher::rule_store rule = [&i, &index_points](const kdnode::ptr node, const double distance)
            {
                if (i != (std::size_t) node->get_payload()) {
                    index_points.push_back((std::size_t) node->get_payload());
                }
            };

            searcher.find_nearest(rule);

            ASSERT_EQ(tree.get_size() - 1, index_points.size());
            ASSERT_TRUE(std::find(index_points.begin(), index_points.end(), i) == index_points.end());
        }
    }

    virtual void TemplateTestInsertSearchRemove(const dataset & p_data, const double radius_search = 10.0) {
        tree = kdtree();

        ASSERT_EQ(nullptr, tree.get_root());

        for (std::size_t index = 0; index < p_data.size(); index++) {
            ASSERT_EQ(tree.get_size(), index);

            tree.insert(p_data[index], (void *) index);
            ASSERT_EQ(tree.get_size(), index + 1);

            searcher = kdtree_searcher(p_data[index], tree.get_root(), radius_search);

            /* Find the nearest node */
            FindNearestNode(p_data, index);

            /* Find the nearest neighbors */
            FindNearestNeighbors(p_data, index);

            /* Find nearest using user-specific rule to store result */
            std::vector<std::size_t> index_points;
            kdtree_searcher::rule_store rule = [&index, &index_points](const kdnode::ptr node, const double distance) 
                { 
                    if (index != (std::size_t) node->get_payload()) {
                        index_points.push_back((std::size_t) node->get_payload());
                    }
                };

            searcher.find_nearest(rule);

            ASSERT_EQ(tree.get_size() - 1, index_points.size());
            ASSERT_TRUE(std::find(index_points.begin(), index_points.end(), index) == index_points.end());
        }

        for (std::size_t index = 0; index < p_data.size(); index++) {
            ASSERT_EQ(tree.get_size(), p_data.size() - index);

            tree.remove(p_data[index]);
            ASSERT_EQ(tree.get_size(), p_data.size() - index - 1);
        }

        ASSERT_EQ(tree.get_size(), 0U);
        ASSERT_EQ(tree.get_root(), nullptr);
    }

    virtual void TemplateInsertFindRemoveByCoordinatesAndPayload(const dataset & p_data, const std::vector<std::size_t> & p_payloads) {
        tree = kdtree();

        std::vector<kdnode::ptr> nodes = { };
        for (std::size_t i = 0; i < p_data.size(); i++) {
            nodes.push_back( tree.insert(p_data[i], (void *) &(p_payloads[i])) );
        }

        for (auto & node : nodes) {
            kdnode::ptr found_node = tree.find_node(node->get_data(), node->get_payload());
            ASSERT_EQ(node, found_node);
        }

        for (std::size_t i = 0; i < nodes.size(); i++) {
            tree.remove(nodes[i]->get_data(), nodes[i]->get_payload());

            kdnode::ptr found_node = tree.find_node(nodes[i]->get_data(), nodes[i]->get_payload());
            ASSERT_EQ(nullptr, found_node);

            for (std::size_t j = i + 1; j < nodes.size(); j++) {
                found_node = tree.find_node(nodes[j]->get_data(), nodes[j]->get_payload());
                ASSERT_EQ(nodes[j], found_node);
            }
        }
    }

private:
    void FindNearestNode(const dataset & p_data, const std::size_t p_index) {
        kdnode::ptr nearest_node = searcher.find_nearest_node();

        ASSERT_EQ(nearest_node->get_data(), p_data[p_index]);
        ASSERT_EQ((std::size_t) nearest_node->get_payload(), p_index);
    }

    void FindNearestNeighbors(const dataset & p_data, const std::size_t p_index) {
        std::vector<double> nearest_distances;
        std::vector<kdnode::ptr> nearest_nodes;
        searcher.find_nearest_nodes(nearest_distances, nearest_nodes);

        ASSERT_EQ(tree.get_size(), nearest_distances.size());
        ASSERT_EQ(tree.get_size(), nearest_nodes.size());

        for (auto & found_kdnode : nearest_nodes) {
            ASSERT_NE(nullptr, found_kdnode);
        }
    }

protected:
    kdtree_searcher     searcher;
    kdtree              tree;
};


TEST_F(utest_kdtree, creation_without_payload) {
    std::vector< std::vector<double> > test_sample_point_vector = { {4, 3}, {3, 4}, {5, 8}, {3, 3}, {3, 9}, {6, 4}, {5, 9} };

    InitTestObject(test_sample_point_vector);

    std::vector<kdnode::ptr> children;
    tree.get_root()->get_children(children);

    ASSERT_NE(nullptr, children[0]);
    ASSERT_NE(nullptr, children[1]);

    for (auto & point : test_sample_point_vector) {
        kdnode::ptr node = tree.find_node(point);

        ASSERT_NE(nullptr, node);
        ASSERT_EQ(nullptr, node->get_payload());
        ASSERT_EQ(point, node->get_data());
    }
}


TEST_F(utest_kdtree, parent_node) {
    std::vector< std::vector<double> > test_sample_point_vector = { {4, 3}, {3, 4}, {5, 8}, {3, 3}, {3, 9}, {6, 4}, {5, 9} };

    InitTestObject(test_sample_point_vector);

    kdnode::ptr node = tree.find_node(test_sample_point_vector[0]);
    ASSERT_EQ(nullptr, node->get_parent());

    node = tree.find_node(test_sample_point_vector[1]);
    ASSERT_EQ(test_sample_point_vector[0], node->get_parent()->get_data());

    node = tree.find_node(test_sample_point_vector[2]);
    ASSERT_EQ(test_sample_point_vector[0], node->get_parent()->get_data());

    node = tree.find_node(test_sample_point_vector[5]);
    ASSERT_EQ(test_sample_point_vector[2], node->get_parent()->get_data());

    node = tree.find_node(test_sample_point_vector[3]);
    ASSERT_EQ(test_sample_point_vector[1], node->get_parent()->get_data());

    node = tree.find_node(test_sample_point_vector[6]);
    ASSERT_EQ(test_sample_point_vector[2], node->get_parent()->get_data());

    node = tree.find_node(test_sample_point_vector[4]);
    ASSERT_EQ(test_sample_point_vector[1], node->get_parent()->get_data());
}


TEST_F(utest_kdtree, insert_remove_node) {
    std::vector< char > test_sample_payload = { 'q', 'w', 'e', 'r', 't', 'y', 'u' };
    std::vector< std::vector<double> > test_sample_point_vector = { {4, 3}, {3, 4}, {5, 8}, {3, 3}, {3, 9}, {6, 4}, {5, 9} };

    for (std::size_t index = 0; index < test_sample_point_vector.size(); index++) {
        std::vector<double> & point = test_sample_point_vector[index];
        char * payload = (char *) &(test_sample_payload[index]);

        ASSERT_EQ(tree.get_size(), index);
        tree.insert(point, payload);
        ASSERT_EQ(tree.get_size(), index + 1);

        kdnode::ptr node = tree.find_node(point);
        ASSERT_NE(nullptr, node.get());
        ASSERT_EQ(point, node->get_data());
        ASSERT_EQ(payload, node->get_payload());
    }


    for (std::size_t index = 0; index < test_sample_point_vector.size(); index++) {
        std::vector<double> & point = test_sample_point_vector[index];
        tree.remove(point);

        kdnode::ptr node = tree.find_node(test_sample_point_vector[index]);
        ASSERT_EQ(nullptr, node.get());

        for (std::size_t next_index = index + 1; next_index < test_sample_point_vector.size(); next_index++) {
            node = tree.find_node(test_sample_point_vector[next_index]);
            std::vector<double> point = test_sample_point_vector[next_index];

            ASSERT_EQ(point, node->get_data());
            ASSERT_EQ(&test_sample_payload[next_index], node->get_payload());
        }
    }

    ASSERT_EQ(tree.get_size(), static_cast<std::size_t>(0));
}


TEST_F(utest_kdtree, find_without_insertion) {
    std::vector< std::vector<double> > test_sample_point_vector = { {4, 3}, {3, 4}, {5, 8}, {3, 3}, {3, 9}, {6, 4}, {5, 9} };

    for (unsigned int index = 0; index < test_sample_point_vector.size(); index++) {
        std::vector<double> & point = test_sample_point_vector[index];

        kdnode::ptr node = tree.find_node(point);
        ASSERT_EQ(nullptr, node.get());
    }
}


TEST_F(utest_kdtree, remove_long_branch) {
    std::vector< std::vector<double> > test_sample_point_vector = { {5, 5}, {6, 5}, {6, 6}, {7, 6}, {7, 7} };

    InitTestObject(test_sample_point_vector);

    for (auto & point : test_sample_point_vector) {
        tree.remove(point);

        kdnode::ptr node = tree.find_node(point);
        ASSERT_EQ(nullptr, node);
    }
}


TEST_F(utest_kdtree, insert_search_remove_simple_01) {
    auto sample = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    TemplateTestInsertSearchRemove(*sample);
}


TEST_F(utest_kdtree, insert_search_simple_01) {
    auto sample = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    TemplateTestBalancedSearch(*sample);
}


TEST_F(utest_kdtree, insert_search_remove_simple_02) {
    auto sample = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02);
    TemplateTestInsertSearchRemove(*sample);
}


TEST_F(utest_kdtree, insert_search_simple_02) {
    auto sample = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02);
    TemplateTestBalancedSearch(*sample);
}


TEST_F(utest_kdtree, insert_search_remove_simple_03) {
    auto sample = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03);
    TemplateTestInsertSearchRemove(*sample);
}


TEST_F(utest_kdtree, insert_search_simple_03) {
    auto sample = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03);
    TemplateTestBalancedSearch(*sample);
}


TEST_F(utest_kdtree, insert_search_remove_simple_04) {
    auto sample = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04);
    TemplateTestInsertSearchRemove(*sample);
}


TEST_F(utest_kdtree, insert_search_simple_04) {
    auto sample = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04);
    TemplateTestBalancedSearch(*sample);
}


TEST_F(utest_kdtree, insert_search_remove_simple_05) {
    auto sample = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05);
    TemplateTestInsertSearchRemove(*sample);
}


TEST_F(utest_kdtree, insert_search_simple_05) {
    auto sample = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05);
    TemplateTestBalancedSearch(*sample);
}


TEST_F(utest_kdtree, insert_search_remove_simple_06) {
    auto sample = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_06);
    TemplateTestInsertSearchRemove(*sample);
}


TEST_F(utest_kdtree, insert_search_simple_06) {
    auto sample = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_06);
    TemplateTestBalancedSearch(*sample);
}


TEST_F(utest_kdtree, insert_search_remove_simple_07) {
    auto sample = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07);
    TemplateTestInsertSearchRemove(*sample);
}


TEST_F(utest_kdtree, insert_search_simple_07) {
    auto sample = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07);
    TemplateTestBalancedSearch(*sample);
}


TEST_F(utest_kdtree, insert_search_remove_simple_08) {
    auto sample = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_08);
    const double search_radius = farthest_distance(*sample, distance_metric_factory<point>::euclidean());
    TemplateTestInsertSearchRemove(*sample, search_radius);
}


TEST_F(utest_kdtree, insert_search_simple_08) {
    auto sample = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_08);
    const double search_radius = farthest_distance(*sample, distance_metric_factory<point>::euclidean());
    TemplateTestBalancedSearch(*sample, search_radius);
}


TEST_F(utest_kdtree, insert_search_remove_simple_10) {
    auto sample = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_10);
    const double search_radius = farthest_distance(*sample, distance_metric_factory<point>::euclidean());
    TemplateTestInsertSearchRemove(*sample, search_radius);
}


TEST_F(utest_kdtree, insert_search_simple_10) {
    auto sample = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_10);
    const double search_radius = farthest_distance(*sample, distance_metric_factory<point>::euclidean());
    TemplateTestBalancedSearch(*sample, search_radius);
}



TEST_F(utest_kdtree, insert_search_remove_hepta) {
    auto sample = fcps_sample_factory::create_sample(FCPS_SAMPLE::HEPTA);
    double search_radius = farthest_distance(*sample, distance_metric_factory<point>::euclidean());
    search_radius += search_radius * 0.0000001;
    TemplateTestInsertSearchRemove(*sample, search_radius);
}


#ifndef VALGRIND_ANALYSIS_SHOCK

TEST_F(utest_kdtree, insert_search_remove_lsun) {
    auto sample = fcps_sample_factory::create_sample(FCPS_SAMPLE::LSUN);
    const double search_radius = farthest_distance(*sample, distance_metric_factory<point>::euclidean());
    TemplateTestInsertSearchRemove(*sample, search_radius);
}


TEST_F(utest_kdtree, insert_search_remove_tetra) {
    auto sample = fcps_sample_factory::create_sample(FCPS_SAMPLE::TETRA);
    double search_radius = farthest_distance(*sample, distance_metric_factory<point>::euclidean());
    search_radius += search_radius * 0.0000001;
    TemplateTestInsertSearchRemove(*sample, search_radius);
}


TEST_F(utest_kdtree, insert_search_remove_two_diamonds) {
    auto sample = fcps_sample_factory::create_sample(FCPS_SAMPLE::TWO_DIAMONDS);
    const double search_radius = farthest_distance(*sample, distance_metric_factory<point>::euclidean());
    TemplateTestInsertSearchRemove(*sample, search_radius);
}

#endif


TEST_F(utest_kdtree, insert_search_remove_with_payload_identical_data_1) {
    dataset data = { {0.1}, {0.1}, {0.1}, {0.1}, {0.2}, {0.2} };
    std::vector<std::size_t> payloads = { 0, 1, 2, 3, 4, 5 };

    TemplateInsertFindRemoveByCoordinatesAndPayload(data, payloads);
}


TEST_F(utest_kdtree, insert_search_remove_with_payload_identical_data_2) {
    dataset data = { {0.1}, {0.1}, {0.1}, {0.1}, {0.1}, {0.1} };
    std::vector<std::size_t> payloads = { 0, 1, 2, 3, 4, 5 };

    TemplateInsertFindRemoveByCoordinatesAndPayload(data, payloads);
}

TEST_F(utest_kdtree, insert_search_remove_with_payload_identical_data_3) {
    dataset data = { {0.1}, {0.1}, {0.1}, {0.1}, {0.2}, {0.2} };
    std::vector<std::size_t> payloads = { 0, 1, 2, 3, 4, 5 };

    TemplateInsertFindRemoveByCoordinatesAndPayload(data, payloads);
}


TEST_F(utest_kdtree, insert_search_remove_with_payload_identical_data_4) {
    dataset data = { {1.2}, {1.2}, {1.3}, {1.3}, {1.4}, {1.4} };
    std::vector<std::size_t> payloads = { 0, 1, 2, 3, 4, 5 };

    TemplateInsertFindRemoveByCoordinatesAndPayload(data, payloads);
}


TEST_F(utest_kdtree, insert_search_remove_with_payload_identical_data_5) {
    dataset data = { {75, 75}, {75, 75}, {75, 75}, {75, 75}, {75, 75}, {75, 75}, {75, 75}, {75, 75} };
    std::vector<std::size_t> payloads = { 0, 1, 2, 3, 4, 5, 6, 7 };

    TemplateInsertFindRemoveByCoordinatesAndPayload(data, payloads);
}


TEST_F(utest_kdtree, insert_search_remove_with_payload_identical_simple_09) {
    auto data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09);
    std::vector<std::size_t> payloads(data->size());
    std::iota(payloads.begin(), payloads.end(), 0);

    TemplateInsertFindRemoveByCoordinatesAndPayload(*data, payloads);
}


TEST_F(utest_kdtree, insert_search_remove_with_payload_identical_simple_11) {
    auto data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_11);
    std::vector<std::size_t> payloads(data->size());
    std::iota(payloads.begin(), payloads.end(), 0);

    TemplateInsertFindRemoveByCoordinatesAndPayload(*data, payloads);
}


TEST_F(utest_kdtree, insert_search_remove_with_payload_identical_simple_12) {
    auto data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_12);
    std::vector<std::size_t> payloads(data->size());
    std::iota(payloads.begin(), payloads.end(), 0);

    TemplateInsertFindRemoveByCoordinatesAndPayload(*data, payloads);
}


TEST_F(utest_kdtree, balanced_tree_find_simple_01) {
    auto data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    TemplateTestBalancedFind(*data);
}


TEST_F(utest_kdtree, balanced_tree_find_simple_02) {
    auto data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02);
    TemplateTestBalancedFind(*data);
}


TEST_F(utest_kdtree, balanced_tree_find_simple_03) {
    auto data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03);
    TemplateTestBalancedFind(*data);
}


TEST_F(utest_kdtree, balanced_tree_find_simple_04) {
    auto data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04);
    TemplateTestBalancedFind(*data);
}


TEST_F(utest_kdtree, balanced_tree_find_simple_05) {
    auto data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05);
    TemplateTestBalancedFind(*data);
}


TEST_F(utest_kdtree, balanced_tree_find_simple_06) {
    auto data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_06);
    TemplateTestBalancedFind(*data);
}


TEST_F(utest_kdtree, balanced_tree_find_simple_07) {
    auto data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07);
    TemplateTestBalancedFind(*data);
}


TEST_F(utest_kdtree, balanced_tree_find_simple_08) {
    auto data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_08);
    TemplateTestBalancedFind(*data);
}


TEST_F(utest_kdtree, balanced_tree_find_simple_09) {
    auto data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09);
    TemplateTestBalancedFind(*data);
}


TEST_F(utest_kdtree, balanced_tree_find_simple_10) {
    auto data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_10);
    TemplateTestBalancedFind(*data);
}


TEST_F(utest_kdtree, balanced_tree_find_simple_11) {
    auto data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_11);
    TemplateTestBalancedFind(*data);
}


TEST_F(utest_kdtree, balanced_tree_find_simple_12) {
    auto data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_12);
    TemplateTestBalancedFind(*data);
}
