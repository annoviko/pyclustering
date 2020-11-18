/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <cstddef>
#include <stdexcept>
#include <sstream>
#include <string>
#include <type_traits>
#include <vector>

#include <pyclustering/definitions.hpp>
#include <pyclustering/utils/traits.hpp>


/*!

@brief  Enumerates types that are supported by pyclustering package.

@see    pyclustering_package

*/
enum pyclustering_data_t {
    PYCLUSTERING_TYPE_INT               = 0,    /**< Represents basic `int` type. */
    PYCLUSTERING_TYPE_UNSIGNED_INT      = 1,    /**< Represents basic `unsigned int` type. */
    PYCLUSTERING_TYPE_FLOAT             = 2,    /**< Represents basic `float` type. */
    PYCLUSTERING_TYPE_DOUBLE            = 3,    /**< Represents basic `double` type. */
    PYCLUSTERING_TYPE_LONG              = 4,    /**< Represents basic `long` type. */
    PYCLUSTERING_TYPE_CHAR              = 5,    /**< Represents basic `char` type. */
    PYCLUSTERING_TYPE_LIST              = 6,    /**< Represents `pyclustering_package` type. */
    PYCLUSTERING_TYPE_SIZE_T            = 7,    /**< Represents basic `std::size_t` type. */
    PYCLUSTERING_TYPE_WCHAR_T           = 8,    /**< Represents basic `wchar_t` type. */
    PYCLUSTERING_TYPE_UNDEFINED         = 9     /**< Indicates incorrect type. */
};


/*!

@class  pyclustering_package pyclustering_package.hpp pyclustering/interface/pyclustering_package.hpp

@brief  Container that is used as data storage to communicate with the Python implementation of the library.
@details The package uses dynamic memory allocation and user of the package is responsible for the deallocation to avoid memory leakage.

*/
struct DECLARATION pyclustering_package {
public:
    std::size_t     size      = 0;          /**< Amount of elements that are contained by the package. */
    unsigned int    type      = static_cast<unsigned int>(PYCLUSTERING_TYPE_UNDEFINED); /**< Type of elements that are contained by the package. */
    void            * data    = nullptr;    /**< Pointer to elements that are contained by the package. */

public:
    /*!
    
    @brief  Default constructor of the package.

    */
    pyclustering_package() = default;

    /*!

    @brief  Constructor of the package that contains elements with specific type.

    @param[in] package_type: type of elements that are contained by the package.

    */
    explicit pyclustering_package(const pyclustering_data_t package_type);

    /*!

    @brief  Destructor of the package.

    */
    ~pyclustering_package();

public:
    /*!
    
    @brief  Returns reference to package element at the specified position like in case of array or vector.

    @param[in] index: index of an element in the package.

    @return Reference to the element in the package.

    @throw  `std::out_of_range` if the package does not have element with index `index`.

    */
    template <class TypeValue>
    auto & at(const std::size_t index) const {
        if (size <= index) {
            throw std::out_of_range("pyclustering_package::at() [" + std::to_string(__LINE__) + "]: index '" + std::to_string(index) + "' out of range (size: '" + std::to_string(size) + "').");
        }

        return ((TypeValue *) data)[index];
    }

    /*!

    @brief  Returns reference to package element at the specified position like in case of two-dimensional array or vector.

    @param[in] index_row: row index in the package where required element is located.
    @param[in] index_column: column index in the package where required element is located.

    @return Reference to the element in the package.

    @throw  `std::out_of_range` if the package does not have row with index `index_row` or does not have column with index `index_column`.

    */
    template <class TypeValue>
    auto & at(const std::size_t index_row, const std::size_t index_column) const {
        if (size <= index_row) {
            throw std::out_of_range("pyclustering_package::at() [" + std::to_string(__LINE__) + "]: index '" + std::to_string(index_row) + "' out of range (size: '" + std::to_string(size) + "').");
        }

        pyclustering_package * package = at<pyclustering_package *>(index_row);
        return ((TypeValue *) package->data)[index_column];
    }

    /*!

    @brief   Extract content of the package to standard container.
    @details Extraction is a copying procedure.

    @param[in] container: container that is used as a destination for the extraction procedure.

    */
    template <class TypeValue>
    void extract(std::vector<TypeValue> & container) const {
        extract(container, this);
    }

    /*!

    @brief   Extract content of the package to standard container.
    @details Extraction is a copying procedure.

    @param[in] container: container that is used as a destination for the extraction procedure.

    */
    template <class TypeValue>
    void extract(std::vector<std::vector<TypeValue>> & container) const {
        if (type != PYCLUSTERING_TYPE_LIST) {
            throw std::invalid_argument("pyclustering_package::extract() [" + std::to_string(__LINE__) + "]: argument is not 'PYCLUSTERING_TYPE_LIST').");
        }

        for (std::size_t i = 0; i < size; i++) {
            std::vector<TypeValue> subcontainer = { };
            extract(subcontainer, at<pyclustering_package *>(i));
            container.push_back(subcontainer);
        }
    }

private:
    /*!

    @brief   Extract content of the package to standard container from specific pyclustering package.

    @param[in] container: container that is used as a destination for the extraction procedure.
    @param[in] package: package that is used as a source for the extraction procedure.

    */
    template <class TypeValue>
    void extract(std::vector<TypeValue> & container, const pyclustering_package * const package) const {
        for (std::size_t i = 0; i < package->size; i++) {
            container.push_back(package->at<TypeValue>(i));
        }
    }
};


/*!

@brief   Create pyclustering package with specified size that defines amount of elements that are going to be
          stored in the package.

@param[in] p_size: package size that defines amount of elements.

@return  Pointer to created pyclustering package.

*/
pyclustering_package * create_package_container(const std::size_t p_size);


/*!

@brief   Returns data type of the pyclustering package.
@details If the template parameter of the function contains unsupported data type then `PYCLUSTERING_TYPE_UNDEFINED` is returned.

@return  Data type of the pyclustering package.

*/
template <class TypeValue>
pyclustering_data_t get_package_type() {
    pyclustering_data_t type_package = PYCLUSTERING_TYPE_UNDEFINED;
    if (std::is_same<TypeValue, int>::value) {
        type_package = pyclustering_data_t::PYCLUSTERING_TYPE_INT;
    }
    // cppcheck-suppress multiCondition ; 'int' and 'unsigned int' are not the same.
    else if (std::is_same<TypeValue, unsigned int>::value) {
        type_package = pyclustering_data_t::PYCLUSTERING_TYPE_UNSIGNED_INT;
    }
    else if (std::is_same<TypeValue, float>::value) {
        type_package = pyclustering_data_t::PYCLUSTERING_TYPE_FLOAT;
    }
    else if (std::is_same<TypeValue, double>::value) {
        type_package = pyclustering_data_t::PYCLUSTERING_TYPE_DOUBLE;
    }
    else if (std::is_same<TypeValue, long>::value) {
        type_package = pyclustering_data_t::PYCLUSTERING_TYPE_LONG;
    }
    else if (std::is_same<TypeValue, char>::value) {
        type_package = pyclustering_data_t::PYCLUSTERING_TYPE_CHAR;
    }
    else if (std::is_same<TypeValue, wchar_t>::value) {
        type_package = pyclustering_data_t::PYCLUSTERING_TYPE_WCHAR_T;
    }
    // cppcheck-suppress multiCondition ; 'std::size_t' and 'long' are not the same for x64.
    else if (std::is_same<TypeValue, std::size_t>::value) {
        type_package = pyclustering_data_t::PYCLUSTERING_TYPE_SIZE_T;
    }

    return type_package;
}


/*!

@brief   Create pyclustering package with specified size and data type.

@param[in] p_size: package size that defines amount of elements.

@return  Pointer to created pyclustering package.

*/
template <class TypeValue>
pyclustering_package * create_package(const std::size_t p_size) {
    const pyclustering_data_t type_package = get_package_type<TypeValue>();
    if (type_package == pyclustering_data_t::PYCLUSTERING_TYPE_UNDEFINED) {
        return nullptr;
    }

    pyclustering_package * package = new pyclustering_package(type_package);

    package->size = p_size;
    package->data = new TypeValue[package->size];

    return package;
}


/*!

@brief   Create pyclustering package with specified size, data type and default value for each elements in the package.

@param[in] p_size: package size that defines amount of elements.
@param[in] p_value: default value for each element in the package.

@return  Pointer to created pyclustering package.

*/
template <class TypeValue>
pyclustering_package * create_package(const std::size_t p_size, const TypeValue & p_value) {
    pyclustering_package * package = create_package<TypeValue>(p_size);
    if (package) {
        for (std::size_t i = 0; i < p_size; i++) {
            ((TypeValue *) package->data)[i] = p_value;
        }
    }

    return package;
}


/*!

@brief   Create pyclustering package using pointer to one-dimensional container with fundamental data and that container supports `std::begin`, `std::end` methods and incremental iterators.
@details All data from the container will be copied to the package.

@param[in] data: a pointer to container that is used to create pyclustering container.

@tparam TypeContainer: a pointer type to a container.

@return  Pointer to created pyclustering package.

*/
template <typename TypeContainer,
    typename std::enable_if<
        std::is_pointer<TypeContainer>::value &&
        !pyclustering::utils::traits::is_string<TypeContainer>::value &&
        pyclustering::utils::traits::is_container_with_fundamental_content<
            typename pyclustering::utils::traits::remove_cvp_t<TypeContainer>
        >::value
    >::type* = nullptr
>
pyclustering_package * create_package(TypeContainer data) {
    using container_t = typename std::remove_pointer<TypeContainer>::type;
    using contaner_data_t = typename container_t::value_type;

    pyclustering_package * package = create_package<contaner_data_t>(data->size());
    if (package) {
        std::size_t index = 0;
        for (auto iter = std::begin(*data); iter != std::end(*data); iter++, index++) {
            static_cast<contaner_data_t *>(package->data)[index] = *iter;
        }
    }

    return package;
}


/*!

@brief   Create pyclustering package using pointer to a two-dimensional vector container.
@details All data from the container will be copied to the package.

@param[in] data: container that is used to create pyclustering container.

@tparam TypeObject: an object type that is used by the container.

@return  Pointer to created pyclustering package.

*/
template <typename TypeObject>
pyclustering_package * create_package(const std::vector< std::vector<TypeObject> > * const data) {
    pyclustering_package * package = new pyclustering_package(pyclustering_data_t::PYCLUSTERING_TYPE_LIST);

    package->size = data->size();
    package->data = new pyclustering_package * [package->size];

    for (size_t i = 0; i < package->size; i++) {
        ((pyclustering_package **) package->data)[i] = create_package(&(*data)[i]);
    }

    return package;
}


/*!

@brief   Create pyclustering package using pointer to a two-dimensional vector container that uses pointers for internal elements.
@details All data from the container will be copied to the package.

@param[in] data: container that is used to create pyclustering container.

@tparam TypeObject: an object type that is used by the container.

@return  Pointer to created pyclustering package.

*/
template <typename TypeObject>
pyclustering_package * create_package(const std::vector< std::vector<TypeObject> * > * const data) {
   pyclustering_package * package = new pyclustering_package(pyclustering_data_t::PYCLUSTERING_TYPE_LIST);

   package->size = data->size();
   package->data = new pyclustering_package * [package->size];

   for (size_t i = 0; i < package->size; i++) {
       ((pyclustering_package **) package->data)[i] = create_package((*data)[i]);
   }

   return package;
}


/*!

@brief   Create pyclustering package using raw string such as `char *`, `wchar_t *` including any cv-qualified variants.
@details All data from the raw string will be copied to the package.

@param[in] p_message: string line that is used to create pyclustering package.

@tparam TypeRawString: a character type that is used by the string line.

@return  Pointer to created pyclustering package.

*/
template <typename TypeRawString, 
    typename std::enable_if<
        pyclustering::utils::traits::is_raw_string<TypeRawString>::value
    >::type* = nullptr
>
pyclustering_package * create_package(TypeRawString p_message) {
    using element_string_t = typename std::remove_cv<typename std::remove_pointer<TypeRawString>::type>::type;

    const std::size_t length = std::char_traits<element_string_t>::length(p_message);
    pyclustering_package * package = create_package<element_string_t>(length + 1);

    if (package) {
        std::char_traits<element_string_t>::copy(static_cast<element_string_t *>(package->data), p_message, length);
        static_cast<element_string_t *>(package->data)[package->size - 1] = static_cast<element_string_t>(0);
    }

    return package;
}


/*!

@brief   Create pyclustering package using standard string line such as `std::string`, `std::wstring` including any cv-qualified variants.
@details All data from the raw string will be copied to the package.

@param[in] p_message: string line that is used to create pyclustering container.

@tparam TypeString: a string type that is used to create pyclustering container.

@return  Pointer to created pyclustering package.

*/
template <typename TypeString,
    typename std::enable_if<
        pyclustering::utils::traits::is_string<TypeString>::value
    >::type* = nullptr
>
pyclustering_package * create_package(TypeString & p_message) {
    return create_package(p_message.c_str());
}
