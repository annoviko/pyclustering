#ifndef _KMEDIANS_H_
#define _KMEDIANS_H_

#include <vector>

typedef std::vector<double>         point;
typedef std::vector<unsigned int>   cluster;

class kmedians {
private:
    double                  m_tolerance;
    std::vector<point>      m_medians;
    std::vector<cluster>    m_clusters;

    std::vector<point> *    m_ptr_data; /* used only during processing */

public:
    kmedians(void);

    kmedians(const std::vector<point> & initial_medians, const double tolerance);

    ~kmedians(void);

public:
    void initialize(const std::vector<point> & initial_medians, const double tolerance);

    void process(const std::vector<point> & data);

public:
    inline void get_clusters(std::vector<cluster> & output_clusters) const {
        output_clusters.clear();
        output_clusters.resize(m_clusters.size());

        std::copy(m_clusters.begin(), m_clusters.end(), output_clusters.begin());
    }

    inline void get_medians(std::vector<point> & output_medians) const {
        output_medians.clear();
        output_medians.resize(m_medians.size());

        std::copy(m_medians.begin(), m_medians.end(), output_medians.begin());
    }

private:
    void update_clusters(void);
    
    double update_medians(void);
};

#endif