#ifndef _KMEDIANS_H_
#define _KMEDIANS_H_

#include <vector>


typedef std::vector<double>         point;
typedef std::vector<unsigned int>   cluster;


class kmedians_result {
private:
    friend class kmedians;

private:
    std::vector<cluster>    m_clusters;
    std::vector<point>      m_medians;

public:
    kmedians_result(void) :
        m_clusters(0, cluster()),
        m_medians(0, point()) { }

    virtual ~kmedians_result(void) { }

    inline std::vector<cluster> & get_clusters(void) { return m_clusters; }

    inline std::vector<point> & get_medians(void) { return m_medians; }
};


class kmedians {
private:
    double                  m_tolerance;
    std::vector<point>      m_initial_medians;

    kmedians_result *       m_ptr_result;   /* temporary pointer to output result */
    std::vector<point> *    m_ptr_data;     /* used only during processing */

public:
    kmedians(void);

    kmedians(const std::vector<point> & initial_medians, const double tolerance);

    ~kmedians(void);

public:
    void initialize(const std::vector<point> & initial_medians, const double tolerance);

    void process(const std::vector<point> & data, kmedians_result & output_result);

private:
    void update_clusters(void);
    
    double update_medians(void);
};

#endif
