#ifndef PERSONAPI_H
#define PERSONAPI_H

#include <iostream>


enum PersonCategory{CHILD, TEEN, ADULT};

struct Person {
    std::string firstname;
    std::string surname;
    int birthyear;
    PersonCategory pCategory;

};
PersonCategory getPersonCategory(Person person);
void savePersonToFile(Person person);

#endif
