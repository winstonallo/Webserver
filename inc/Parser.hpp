#ifndef PARSER_HPP
#define PARSER_HPP
#pragma once

#include "Headers.hpp"

// static class for abstractable parsing utils
class Parser
{
	public:

		static std::string	trim(const std::string& str);

	private:
		Parser();
		Parser(const Parser& rhs);
		Parser &operator=(const Parser& rhs);
};

#endif