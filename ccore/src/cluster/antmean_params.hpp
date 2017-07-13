/**
*
* Copyright (C) 2014-2017    Aleksey Kukushkin (pyclustering@yandex.ru)
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

#include <memory>
#include <tuple>
#include <cassert>

#include <type_traits>

#include "tsp/params_container.hpp"

namespace ant
{

// mapped to python interface
typedef struct s_ant_clustering_params {
    double                  ro;
    double                  pheramone_init;
    unsigned int            iterations;
    unsigned int            count_ants;
} s_ant_clustering_params;


enum class params_name_clustering : std::size_t
{
    RO                                // [double]
    , PHERAMONE_INIT                // [double]

    , ITERATIONS                    // [unsigned]
    , COUNT_ANTS                    // [unsigned]

    , LAST_ELEM // should be always last
                // using to check all params are set
};



/***********************************************************************************************
* ant_colony_TSP_params_initializer
*                          - contains type 'params_t' is used to create container for parameters
*  ! NOT CREATABLE !
*
*  Interface:
*       param_type      -   type of param (ex: param_type<Q> = Q_t ...)
*       base_param_type -   type of param value (ex: base_param_type<Q> = double)
*
*       static get [const/non-const]  - methods to get a parameter from container
*       static init_params                     - methods to initialize container
***********************************************************************************************/
//class ant_colony_TSP_params_initializer : public ant_colony_params_initializer_base
class ant_colony_clustering_params_initializer
{
public:
    using params_name = params_name_clustering;

    ////////////////////
    // all parameters should be declared below
    //
    CREATE_PARAM_WITH(RO_t, double);
    CREATE_PARAM_WITH(Pheramone_init_t, double);

    CREATE_PARAM_WITH(Iterations_t, unsigned);
    CREATE_PARAM_WITH(Count_ants_t, unsigned);
    //
    ////////////////////

private:

    template<params_name name>
    struct cast_name
    {
        static const std::size_t val = static_cast<std::size_t>(name);
    };

    using params_container = params_n::params_container<RO_t, Pheramone_init_t, Iterations_t, Count_ants_t>;


public:
    //
    // MAIN type for parameter's container
    //
    using params_t = params_container::type;

    //
    // All parameters should be presented
    //
    static_assert(std::tuple_size<params_t>::value == static_cast<std::size_t>(params_name::LAST_ELEM)
        , "ant_colony_params_initializer should have all params in tuple");

    ////////////////////
    // Check : all params in tuple must be mapped to paramsName in enum
    //
    #define STATIC_ASSERT_TUPLE_TYPES(params_name, className)                             \
        static_assert(params_container::get_elem_type<cast_name<params_name>::val, className>::res::value                   \
                , "paramName(className) param has error placement in tuple");

    STATIC_ASSERT_TUPLE_TYPES(params_name_clustering::RO, RO_t);
    STATIC_ASSERT_TUPLE_TYPES(params_name_clustering::PHERAMONE_INIT, Pheramone_init_t);
    STATIC_ASSERT_TUPLE_TYPES(params_name_clustering::ITERATIONS, Iterations_t);
    STATIC_ASSERT_TUPLE_TYPES(params_name_clustering::COUNT_ANTS, Count_ants_t);

    #undef STATIC_ASSERT_TUPLE_TYPES
    //
    ////////////////////


    ////////////////////
    // overloaded to get param type by name
    //
    template <params_name name>
    using param_type = params_container::param_type<cast_name<name>::val>;

    template <params_name name>
    using base_param_type = params_container::base_param_type<cast_name<name>::val>;
    //
    ////////////////////


    ////////////////////
    //  Functions 'get' for const and non-const return value
    //
#ifdef __CPP_14_ENABLED__
    template<params_name name>
    static decltype(auto) get()
    {
        return base_get<params_t, cast_name<name>::val>(params)
    }

    template<params_name name>
    static decltype(auto) get()
    {
        return base_get<params_t, cast_name<name>::val>(params)
    }

#else
    template<params_name name>
    static auto get(const params_t& params) -> const param_type<name>&
    {
        return params_container::get<cast_name<name>::val>(params);
    }

    template<params_name name>
    static auto get(params_t& params) -> param_type<name>&
    {
        return params_container::get<cast_name<name>::val>(params);
    }
#endif
    //
    ////////////////////

    //
    // Init function
    //
    template<typename... Args>
    static void init_params(params_t& params, Args&&... args)
    {
        params_container::init_params<Args...>(params, std::forward(args)...);
    }
};




/***********************************************************************************************
* ant_clustering_params
*                          - contains all params are used in the algorithm ant clustering with means
* Do not able to create object params
*
* example:
*
***********************************************************************************************/
class ant_clustering_params
{
public:

    // delete constructor
    ant_clustering_params(const ant_clustering_params&) = delete;
    // delete move constructor
    ant_clustering_params(const ant_clustering_params&&) = delete;

    // but it's able to assignment for objects
    ant_clustering_params& operator= (const ant_clustering_params& other) = default;

    ant_clustering_params& operator= (ant_clustering_params&& other) = default;


    using AP = ant_colony_clustering_params_initializer;

    // fabric functions to produce shared ptr to algorithm's params
#ifdef __CPP_14_ENABLED__
    static decltype(auto)
#else
    static std::shared_ptr<ant_clustering_params>
#endif
        make_param(      AP::RO_t&& ro_init
                    , AP::Pheramone_init_t&& ph_init
                    , AP::Iterations_t&& iter_init
                    , AP::Count_ants_t&& count_ants_initi
                )
    {
        // ant_colony_params has a private constructor so make_shared is unavailable
        return std::shared_ptr<ant_clustering_params>
            (new ant_clustering_params(ro_init, ph_init, iter_init, count_ants_initi));
    }

#ifdef __CPP_14_ENABLED__
    static decltype(auto)
#else
    static std::shared_ptr<ant_clustering_params>
#endif
        make_param()
    {
        return std::shared_ptr<ant_clustering_params>(new ant_clustering_params());
    }

    // return a value for a requested param
    template<params_name_clustering name>
#ifdef __CPP_14_ENABLED__
    decltype(auto)
#else
    const AP::param_type<name>&
#endif
        get() const
    {
        return AP::get<name>(params);
    }

    template<AP::params_name name>
    void set(AP::base_param_type<name> value)
    {
        AP::get<name>(params) = AP::param_type<name>(value);
    }

private:
    // constructors in private to create only by the fabric function 'make_param'
    // to prevent creating much copies of the same object
    // all actions are able with pointer returned by the fabric function

    ant_clustering_params(      AP::RO_t& ro_init
                            , AP::Pheramone_init_t& ph_init
                            , AP::Iterations_t& iter_init
                            , AP::Count_ants_t& count_ants_initi
        )
        : params{ ro_init, ph_init, iter_init, count_ants_initi }
    {}


    ant_clustering_params()
        : params{ AP::RO_t(0.9), AP::Pheramone_init_t(0.1),  AP::Iterations_t(10), AP::Count_ants_t(5) }
    {}

private:

    AP::params_t params;

};











}
