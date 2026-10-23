#include <fstream>
#include "personapi.h"

PersonCategory getPersonCategory(Person person)
{
    PersonCategory result;

    if (2026 - person.birthyear <= 12)
    {
        result = PersonCategory::CHILD;
    }
    else if (2026 - person.birthyear <= 18)
    {
        result = PersonCategory::TEEN;
    }
    else
    {
        result = PersonCategory::ADULT;
    }

    return result;
}

void savePersonToFile(Person person)
{
    std::ofstream fileChilds("C:\\C++\\Childs.txt", std::ios::app);
    std::ofstream fileTeens("C:\\C++\\Teens.txt", std::ios::app);
    std::ofstream fileAdults("C:\\C++\\Adults.txt", std::ios::app);

    if (getPersonCategory(person) == PersonCategory::CHILD)
    {
        fileChilds << person.firstname << " "
                   << person.surname << " "
                   << person.birthyear << "\n";
    }
    else if (getPersonCategory(person) == PersonCategory::TEEN)
    {
        fileTeens << person.firstname << " "
                  << person.surname << " "
                  << person.birthyear << "\n";
    }
    else if (getPersonCategory(person) == PersonCategory::ADULT)
    {
        fileAdults << person.firstname << " "
                   << person.surname << " "
                   << person.birthyear << "\n";
    }

}