/*
 * params_container.hpp
 *
 *  Created on: Apr 6, 2016
 *      Author: alex
 */

#pragma once


//
// Each parameter should take a one argument
// and forward it to base class
//
#define CREATE_PARAM_WITH(name, type)    \
            class name : public params_n::Base_t<type>                \
            {                                               \
            public:                                         \
                explicit name(type init)                    \
                :Base_t(init)                               \
                {}                                          \
            };




namespace params_n{


/*****************************
*   Base class for all params
*****************************/
template<typename T>
class Base_t
{
public:
    using type = T;

    explicit Base_t(T init)
        :value{ init }
    {}

    T get() const { return value; }

private:
    T value;
};//end class Base_t



/***********************************************************************************************
* params_container
*                          - provides ONLY types to create container with parameters
*  ! NOT CREATABLE !
*
***********************************************************************************************/
template<typename... TParams>
class params_container
{
public:
    // do not able to create the object
    params_container() = delete;


    //
    //      MAIN TYPE for parameters
    //
    using type = std::tuple<TParams...>;


    // template class to represent types for each parameter
    template<std::size_t name>
    using param_type = typename std::tuple_element<name, type>::type;

    template <std::size_t name>
    using base_param_type = typename param_type<name>::type;

    //
    //  Functions 'get' for const and non-const return value
    //
#ifdef __CPP_14_ENABLED__
    template<std::size_t name>
    static decltype(auto) get(const type& params)
    {
        return std::get<name>(params);
    }

    template<std::size_t name>
    static decltype(auto) get(type& params)
    {
        return std::get<name>(params);
    }

#else
    template<std::size_t name>
    static auto get(const type& params) -> const param_type<name>&
    {
        return std::get<name>(params);
    }

    template<std::size_t name>
    static auto get(type& params) -> param_type<name>&
    {
        return std::get<name>(params);
    }
#endif


    //
    // Function to init tuple
    //
    template<typename... Args>
    static void init_params(type& params, Args&&... args)
    {
        params = std::make_tuple(std::forward(args)...);
    }

    template<std::size_t paramName, typename tupleElem>
    struct get_elem_type
    {
        using res = std::is_same<typename std::tuple_element<paramName, type>::type, tupleElem>;
    };
};


}// namespace params_n
