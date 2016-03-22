
#include "AntColonyAlgorithmParams.hpp"


namespace ant_colony
{
	AntColonyAlgorithmParams::AntColonyAlgorithmParams(AP::Q_t&& Q_init
		, AP::Ro_t&& ro_init
		, AP::Alpha_t&& alpha_init
		, AP::Beta_t&& beta_init
		, AP::Gamma_t&& gamma_init)
	{
		params.emplace(AP::paramsName::Q, Q_init.get());
		params.emplace(AP::paramsName::RO, ro_init.get());
		params.emplace(AP::paramsName::ALPHA, alpha_init.get());
		params.emplace(AP::paramsName::BETA, beta_init.get());
		params.emplace(AP::paramsName::GAMMA, gamma_init.get());

		//all params should be set
		assert(params.size() == static_cast<std::size_t>(AP::paramsName::LAST_ELEM));
	}


	AntColonyAlgorithmParams::AntColonyAlgorithmParams()
	{
		params.emplace(AP::paramsName::Q, 0.5);
		params.emplace(AP::paramsName::RO, 0.7);
		params.emplace(AP::paramsName::ALPHA, 1.0);
		params.emplace(AP::paramsName::BETA, 1.0);
		params.emplace(AP::paramsName::GAMMA, 2.0);

		//all params should be set
		assert(params.size() == static_cast<std::size_t>(AP::paramsName::LAST_ELEM));
	}


}//namespace ant_colony