/*
* ant_colony.h
*
*  Created on: Mar 21, 2016
*      Author: alex
*/

#pragma once

#include <memory>
#include <tuple>
#include <cassert>

#include <type_traits>

namespace ant_colony
{


/***********************************************************************************************
* AntColonyAlgorithmParamsInitialize
*                          - contains names and classes for all possible params in algorithm
*  ! NOT CREATABLE !
*
*  example below in class AntColonyAlgorithmParams
***********************************************************************************************/
class AntColonyAlgorithmParamsInitializer
{
public:

	// do not able to create the object
	AntColonyAlgorithmParamsInitializer() = delete;

	enum class paramsName
	{
		Q			// [double]
		, RO		// [double]
		, ALPHA		// [double]
		, BETA		// [double]
		, GAMMA		// [double]
		, INITIAL_PHERAMONE // [double]

		, ITERATIONS // [unsigned]
		, COUNT_ANTS_IN_ITERATION // [unsigned]

		, LAST_ELEM // should be always last
					// using to check what all params are set 
	};


	/*****************************
	*	Base class for all params
	*****************************/
	template<typename T>
	class Base_t
	{
	public:
		Base_t(T init)
			:value{ init }
		{}

		auto get() const { return value; }

	private:
		T value;
	};//end class Base_t


	//
	// All params should take one argument -> value
	// and forward it to base class
	//
	#define CREATE_CLASS_WITH_BASE_T_CONSTRACTOR(name, type)	\
				class name : public Base_t<type>				\
				{												\
				public:											\
					name(type init)								\
					:Base_t(init)								\
					{}											\
				};										

	//
	//Should be declared all params from 'enum class paramsName'
	//
	CREATE_CLASS_WITH_BASE_T_CONSTRACTOR(Q_t	, double);
	CREATE_CLASS_WITH_BASE_T_CONSTRACTOR(Ro_t	, double);
	CREATE_CLASS_WITH_BASE_T_CONSTRACTOR(Alpha_t, double);
	CREATE_CLASS_WITH_BASE_T_CONSTRACTOR(Beta_t , double);
	CREATE_CLASS_WITH_BASE_T_CONSTRACTOR(Gamma_t, double);
	CREATE_CLASS_WITH_BASE_T_CONSTRACTOR(InitialPheramone_t, double);

	CREATE_CLASS_WITH_BASE_T_CONSTRACTOR(Iterations_t, unsigned);
	CREATE_CLASS_WITH_BASE_T_CONSTRACTOR(CountAntsInIteration_t, unsigned);

	#undef CREATE_CLASS_WITH_BASE_T_CONSTRACTOR

	//
	//		MAIN TYPE for params
	// Type to using it in the algorithm 
	//
	using params_t = std::tuple<Q_t, Ro_t, Alpha_t, Beta_t, Gamma_t, InitialPheramone_t, Iterations_t, CountAntsInIteration_t>;


	//
	//	Functions get for const and non const return value
	//
	template<paramsName name>
	static decltype(auto) get(const params_t& params)
	{
		return std::get<static_cast<int>(name)>(params);
	}

	template<paramsName name>
	static decltype(auto) get(params_t& params)
	{
		return std::get<static_cast<int>(name)>(params);
	}


	//
	// Function to init tuple
	//
	template<typename... Args>
	static void init_params(const params_t& params, Args&&... args)
	{
		params = std::make_tuple(std::forward(args)...);
	}

private:
	// Tuple should contain all params elements
	static_assert(std::tuple_size<params_t>::value == static_cast<std::size_t>(paramsName::LAST_ELEM)
		, "AntColonyAlgorithmParamsInitializer should have all params in tuple");


	// Check : all params in tuple must be mapped to paramsName in enum
	template<paramsName paramName, typename tupleElem>
	struct get_elem_type
	{
		//using param_type = std::tuple_element<static_cast<int>(paramName), params_t>;
		using res = std::is_same<typename std::tuple_element<static_cast<int>(paramName), params_t>::type, tupleElem>;
	};

	#define STATIC_ASSERT_TUPLE_TYPES(paramName, className)								\
		static_assert(get_elem_type<paramName, className>::res::value					\
				, "paramName(className) param has error placement in tuple");			\

	STATIC_ASSERT_TUPLE_TYPES(paramsName::Q, Q_t);
	STATIC_ASSERT_TUPLE_TYPES(paramsName::RO, Ro_t);
	STATIC_ASSERT_TUPLE_TYPES(paramsName::ALPHA, Alpha_t);
	STATIC_ASSERT_TUPLE_TYPES(paramsName::BETA, Beta_t);
	STATIC_ASSERT_TUPLE_TYPES(paramsName::GAMMA, Gamma_t);
	STATIC_ASSERT_TUPLE_TYPES(paramsName::INITIAL_PHERAMONE, InitialPheramone_t);
	STATIC_ASSERT_TUPLE_TYPES(paramsName::ITERATIONS, Iterations_t);
	STATIC_ASSERT_TUPLE_TYPES(paramsName::COUNT_ANTS_IN_ITERATION, CountAntsInIteration_t);

	#undef STATIC_ASSERT_TUPLE_TYPES


}; //end AntColonyAlgorithmParamsInitializer




/***********************************************************************************************
* AntColonyAlgorithmParams
*                          - contains all params are used in the algorithm
* Do not able to create object params
*
* example:
*	
***********************************************************************************************/
class AntColonyAlgorithmParams
{
public:

	// delete constructor
	AntColonyAlgorithmParams(const AntColonyAlgorithmParams&) = delete;
	// delete move constructor
	AntColonyAlgorithmParams(const AntColonyAlgorithmParams&&) = delete;

	// but it's able to assignment for objects
	AntColonyAlgorithmParams& operator= (const AntColonyAlgorithmParams& other) = default;
	AntColonyAlgorithmParams& operator= (AntColonyAlgorithmParams&& other) = default;


	using AP = AntColonyAlgorithmParamsInitializer;


	//-----------------------------------------
	//--
	//-- Can be used to enable make_shared<> for private constructor
	//-- 
	//template<class _Ty>
	//friend class std::_Ref_count_obj;
	//-----------------------------------------

	// fabric functions to produce shared ptr to algorithm's params
	static decltype(auto) make_param(AP::Q_t&& Q_init
		, AP::Ro_t&& ro_init
		, AP::Alpha_t&& alpha_init
		, AP::Beta_t&& beta_init
		, AP::Gamma_t&& gamma_init
		, AP::InitialPheramone_t&& initial_pheromone
		, AP::Iterations_t&& iterations
		, AP::CountAntsInIteration_t&& ants_in_iteration)
	{
		return std::shared_ptr<AntColonyAlgorithmParams>(new AntColonyAlgorithmParams(
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

	static decltype(auto) make_param()
	{
		return std::shared_ptr<AntColonyAlgorithmParams>(new AntColonyAlgorithmParams());
	}


	// return a value for a requested param
	template<AP::paramsName name>
	decltype(auto) get() const
	{
		return AP::get<name>(params);
	}

	template<AP::paramsName name>
	void set(double value)
	{
		AP::get<name>(params) = value;
	}

private:
	// constructors in private to create only by the fabric function 'make_param'
	// to prevent creating much copies of the same object
	// all actions are able with pointer returned by the fabric function
	AntColonyAlgorithmParams(AP::Q_t&& Q_init
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

	AntColonyAlgorithmParams()
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
