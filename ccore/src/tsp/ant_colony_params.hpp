/**
*
* Copyright (C) 2014-2017    Kukushkin Aleksey (pyclustering@yandex.ru)
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

enum class params_name_TSP : std::size_t {
    Q,                  // [double]
    RO,                 // [double]
    ALPHA,              // [double]
    BETA,               // [double]
    GAMMA,              // [double]
    INITIAL_PHERAMONE,  // [double]

    ITERATIONS,         // [unsigned]
    COUNT_ANTS_IN_ITERATION, // [unsigned]

    LAST_ELEM,  // should be always last
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
class ant_colony_TSP_params_initializer
{

public:

    ////////////////////
    // all parameters should be declared below
    //
    CREATE_PARAM_WITH(Q_t    , double);
    CREATE_PARAM_WITH(Ro_t   , double);
    CREATE_PARAM_WITH(Alpha_t, double);
    CREATE_PARAM_WITH(Beta_t , double);
    CREATE_PARAM_WITH(Gamma_t, double);
    CREATE_PARAM_WITH(InitialPheramone_t, double);

    CREATE_PARAM_WITH(Iterations_t, unsigned);
    CREATE_PARAM_WITH(CountAntsInIteration_t, unsigned);
    //
    ////////////////////

private:

    template<params_name_TSP name>
    struct cast_name
    {
        static const std::size_t val = static_cast<std::size_t>(name);
    };

    using params_container = params_n::params_container<Q_t, Ro_t, Alpha_t, Beta_t, Gamma_t, InitialPheramone_t, Iterations_t, CountAntsInIteration_t>;


public:
    //
    // MAIN type for parameter's container
    //
    using params_t = params_container::type;

    //
    // All parameters should be presented
    //
    static_assert(std::tuple_size<params_t>::value == static_cast<std::size_t>(params_name_TSP::LAST_ELEM)
        , "ant_colony_params_initializer should have all params in tuple");

    ////////////////////
    // Check : all params in tuple must be mapped to paramsName in enum
    //
    #define STATIC_ASSERT_TUPLE_TYPES(params_name_TSP, className)                             \
        static_assert(params_container::get_elem_type<cast_name<params_name_TSP>::val, className>::res::value                   \
                , "paramName(className) param has error placement in tuple");

    STATIC_ASSERT_TUPLE_TYPES(params_name_TSP::Q, Q_t);
    STATIC_ASSERT_TUPLE_TYPES(params_name_TSP::RO, Ro_t);
    STATIC_ASSERT_TUPLE_TYPES(params_name_TSP::ALPHA, Alpha_t);
    STATIC_ASSERT_TUPLE_TYPES(params_name_TSP::BETA, Beta_t);
    STATIC_ASSERT_TUPLE_TYPES(params_name_TSP::GAMMA, Gamma_t);
    STATIC_ASSERT_TUPLE_TYPES(params_name_TSP::INITIAL_PHERAMONE, InitialPheramone_t);
    STATIC_ASSERT_TUPLE_TYPES(params_name_TSP::ITERATIONS, Iterations_t);
    STATIC_ASSERT_TUPLE_TYPES(params_name_TSP::COUNT_ANTS_IN_ITERATION, CountAntsInIteration_t);

    #undef STATIC_ASSERT_TUPLE_TYPES
    //
    ////////////////////


    ////////////////////
    // overloaded to get param type by name
    //
    template <params_name_TSP name>
    using param_type = params_container::param_type<cast_name<name>::val>;

    template <params_name_TSP name>
    using base_param_type = params_container::base_param_type<cast_name<name>::val>;
    //
    ////////////////////


    ////////////////////
    //  Functions 'get' for const and non-const return value
    //
#ifdef __CPP_14_ENABLED__
    template<params_name_TSP name>
    static decltype(auto) get()
    {
        return base_get<params_t, cast_name<name>::val>(params)
    }

    template<params_name_TSP name>
    static decltype(auto) get()
    {
        return base_get<params_t, cast_name<name>::val>(params)
    }

#else
    template<params_name_TSP name>
    static auto get(const params_t& params) -> const param_type<name>&
    {
        return params_container::get<cast_name<name>::val>(params);
    }

    template<params_name_TSP name>
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
* ant_colony_TSP_params
*                          - contains all params are used in the algorithm
* Do not able to create object params
*
* example:
*
***********************************************************************************************/
class ant_colony_TSP_params
{
public:

    // delete constructor
    ant_colony_TSP_params(const ant_colony_TSP_params&) = delete;
    // delete move constructor
    ant_colony_TSP_params(const ant_colony_TSP_params&&) = delete;

    // but it's able to assignment for objects
    ant_colony_TSP_params& operator= (const ant_colony_TSP_params& other) = default;

#ifdef __CPP_14_ENABLED__
    ant_colony_params& operator= (ant_colony_params&& other) = default;
#endif


    using AP = ant_colony_TSP_params_initializer;


    //-----------------------------------------
    //--
    //-- Can be used to enable make_shared<> for private constructor
    //--
    //template<class _Ty>
    //friend class std::_Ref_count_obj;
    //-----------------------------------------

    // fabric functions to produce shared ptr to algorithm's params

#ifdef __CPP_14_ENABLED__
    static decltype(auto)
#else
    static std::shared_ptr<ant_colony_TSP_params>
#endif
        make_param(AP::Q_t&& Q_init
        , AP::Ro_t&& ro_init
        , AP::Alpha_t&& alpha_init
        , AP::Beta_t&& beta_init
        , AP::Gamma_t&& gamma_init
        , AP::InitialPheramone_t&& initial_pheromone
        , AP::Iterations_t&& iterations
        , AP::CountAntsInIteration_t&& ants_in_iteration)
    {
        // ant_colony_params has a private constructor so make_shared is unavailable
        return std::shared_ptr<ant_colony_TSP_params>(new ant_colony_TSP_params(
            std::move(Q_init)
            , std::move(ro_init)
            , std::move(alpha_init)
            , std::move(beta_init)
            , std::move(gamma_init)
            , std::move(initial_pheromone)
            , std::move(iterations)
            , std::move(ants_in_iteration))
            );
    }

#ifdef __CPP_14_ENABLED__
    static decltype(auto)
#else
    static std::shared_ptr<ant_colony_TSP_params>
#endif
        make_param()
    {
        return std::shared_ptr<ant_colony_TSP_params>(new ant_colony_TSP_params());
    }

    // return a value for a requested param
    template<params_name_TSP name>
#ifdef __CPP_14_ENABLED__
    decltype(auto)
#else
    const AP::param_type<name>&
#endif
        get() const
    {
        return AP::get<name>(params);
    }

    template<params_name_TSP name>
    void set(AP::base_param_type<name> value)
    {
        AP::get<name>(params) = AP::param_type<name>(value);
    }

private:
    // constructors in private to create only by the fabric function 'make_param'
    // to prevent creating much copies of the same object
    // all actions are able with pointer returned by the fabric function
    ant_colony_TSP_params(AP::Q_t&& Q_init
        , AP::Ro_t&& ro_init
        , AP::Alpha_t&& alpha_init
        , AP::Beta_t&& beta_init
        , AP::Gamma_t&& gamma_init
        , AP::InitialPheramone_t&& initial_pheromone
        , AP::Iterations_t&& iterations
        , AP::CountAntsInIteration_t&& ants_in_iteration)
        : params{
                Q_init, ro_init, alpha_init, beta_init, gamma_init, initial_pheromone, iterations, ants_in_iteration
            }
    {}

    ant_colony_TSP_params()
        : params{
                AP::Q_t{ 0.5 }
                , AP::Ro_t{ 0.7 }
                , AP::Alpha_t{ 1.0 }
                , AP::Beta_t{ 1.0 }
                , AP::Gamma_t{ 2.0 }
                , AP::InitialPheramone_t{ 0.1 }
                , AP::Iterations_t{ 100 }
                , AP::CountAntsInIteration_t{ 50 }
            }
    {}

private:

    AP::params_t params;

};

}//namespace ant_colony
