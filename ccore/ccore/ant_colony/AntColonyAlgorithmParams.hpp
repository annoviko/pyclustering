

/*
* ant_colony.h
*
*  Created on: Mar 21, 2016
*      Author: alex
*/

#pragma once

#include <memory>
#include <unordered_map>
#include <cassert>

#include "city_distance.hpp"


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
		Q
		, RO
		, ALPHA
		, BETA
		, GAMMA

		, LAST_ELEM // should be always last
					// using to check what all params are set 
	};

	/*
	*	Base class for all params
	*/
	class Base_t
	{
	public:
		Base_t(double init)
			:value{ init }
		{}

		auto get() const { return value; }

	private:
		double value;
	};//end class Base_t

	// All params should take one argument -> value
	// and forward it to base class
	#define CREATE_CLASS_WITH_BASE_T_CONSTRACTOR(name)	\
				class name : public Base_t				\
				{										\
				public:									\
					name(double init)					\
					:Base_t(init)						\
					{}									\
				};										

	//Should be declared all params from 'enum class paramsName'
	CREATE_CLASS_WITH_BASE_T_CONSTRACTOR(Q_t);
	CREATE_CLASS_WITH_BASE_T_CONSTRACTOR(Ro_t);
	CREATE_CLASS_WITH_BASE_T_CONSTRACTOR(Alpha_t);
	CREATE_CLASS_WITH_BASE_T_CONSTRACTOR(Beta_t);
	CREATE_CLASS_WITH_BASE_T_CONSTRACTOR(Gamma_t);

	#undef CREATE_CLASS_WITH_BASE_T_CONSTRACTOR

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
		, AP::Gamma_t&& gamma_init)
	{
		return std::shared_ptr<AntColonyAlgorithmParams>(new AntColonyAlgorithmParams(
			std::move(Q_init)
			, std::move(ro_init)
			, std::move(alpha_init)
			, std::move(beta_init)
			, std::move(gamma_init))
			);
	}

	static decltype(auto) make_param()
	{
		return std::shared_ptr<AntColonyAlgorithmParams>(new AntColonyAlgorithmParams());
	}


	// return a value for a requested param
	decltype(auto) get(AP::paramsName name) const
	{
		return params.find(name)->second;
	}

	void set(AP::paramsName name, double value)
	{
		params[name] = value;
	}

private:
	// constructors in private to create only by the fabric function 'make_param'
	// to prevent creating much copies of the same object
	// all actions are able with pointer returned by the fabric function
	AntColonyAlgorithmParams(AP::Q_t&& Q_init
		, AP::Ro_t&& ro_init
		, AP::Alpha_t&& alpha_init
		, AP::Beta_t&& beta_init
		, AP::Gamma_t&& gamma_init);

	AntColonyAlgorithmParams();


private:

	std::unordered_map<AntColonyAlgorithmParamsInitializer::paramsName, double> params;
};

}//namespace ant_colony