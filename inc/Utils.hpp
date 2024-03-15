#ifndef UTILS_HPP
#define UTILS_HPP

#include <vector>
#include <iostream>
#include <string>
#include <sstream>
#include <ostream>
#include <fstream>
#include <algorithm>
#include <unistd.h>

namespace Utils 
{
	bool											write_access(const std::string& path);
	bool											file_exists(const std::string& path);
	void											get_pair(const std::string& str, std::vector <std::pair <std::string, int> >& ret, size_t left, size_t right, int& line_number);
	std::string										trim(const std::string& str, const std::string& delimiters);
	std::string										trim_comment(const std::string& str, const std::string& delimiters);
	std::string										itoa(int num);
	std::vector <std::string>						split(const std::string& str, const std::string& delimiters);
	std::vector <std::string>						split_keep_quoted_words(const std::string& str, const std::string& delimiters);
	std::vector <std::pair <std::string, int> > 	split_keep_delimiters(const std::string& str, const std::string& delimiters);
	int												extract_numeric_value(const std::string& str);
	int												parse_client_max_body_size(const std::string& client_max_body_size);
};

#define UNCLOSED_QUOTE "unclosed quote sequence"

#endif