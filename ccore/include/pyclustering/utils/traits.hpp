/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#pragma once


#include <string>
#include <type_traits>


namespace pyclustering {

namespace utils {

namespace traits {


/*!

@brief   Utility metafunction that maps a sequence of any types to the type `void`.

*/
template<class...>
using void_t = void;


/*!

@brief   Checks whether `TypeRawString` is a raw-string type. 
@details Provides the member constant value which is equal to `true`, if `TypeRawString` is the 
          type `char *`, `wchar_t *`, including any cv-qualified variants. Otherwise, value is equal to `false`.

@tparam TypeRawString: a type to check.

*/
template <typename TypeRawString>
struct is_raw_string : std::integral_constant<bool,
    std::is_pointer<TypeRawString>::value &&
    (std::is_same<char, typename std::remove_cv<typename std::remove_pointer<TypeRawString>::type>::type>::value ||
    std::is_same<wchar_t, typename std::remove_cv<typename std::remove_pointer<TypeRawString>::type>::type>::value)
> { };


/*!

@brief   Checks whether `TypeRawString` is a string type.
@details Provides the member constant value which is equal to `true`, if `TypeRawString` is the
type `std::string`, `std::wstring`, including any cv-qualified variants. Otherwise, value is equal to `false`.

@tparam TypeString: a type to check.

*/
template <typename TypeString>
struct is_string : std::integral_constant<bool,
    std::is_same<std::string, typename std::remove_cv<TypeString>::type>::value ||
    std::is_same<std::wstring, typename std::remove_cv<TypeString>::type>::value
> { };


/*!

@brief   Checks whether `Type` is a container and its elements type is fundamental.
@details Provides the member constant value which is equal to `true`, if `TypeContainer` is the
          has `value_type`, `size_type`, `const_iterator`, `cbegin()`, `cend()`. Otherwise, value is equal to `false`.

@tparam Type: a type to check.

*/
template <typename, typename = void_t<>>
struct is_container_with_fundamental_content : std::false_type { };


/*!

@brief   Checks whether `Type` is a container and its elements type is fundamental.
@details Provides the member constant value which is equal to `true`, if `TypeContainer` is the
          has `value_type`, `size_type`, `const_iterator`, `cbegin()`, `cend()`. Otherwise, value is equal to `false`.

@tparam Type: a type to check.

*/
template <typename Type>
struct is_container_with_fundamental_content <
    Type, void_t<
        typename Type::value_type,
        typename Type::size_type,
        typename Type::const_iterator,
        decltype(std::declval<Type>().cbegin()),
        decltype(std::declval<Type>().cend())
    >
> : std::is_fundamental<typename Type::value_type> { };


/*!

@brief   Removes pointer, `const`, `volatile` from type `Type` if they have a place in the type.

@tparam Type: a type to update.

*/
template <typename Type>
using remove_cvp = std::remove_cv<typename std::remove_pointer<Type>::type>;


/*!

@brief   Helper type that removes pointer, `const`, `volatile` from type `Type` if they have a place in the type.

@tparam Type: a type to update.

*/
template <typename Type>
using remove_cvp_t = typename remove_cvp<Type>::type;


}

}

}