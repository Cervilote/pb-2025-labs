#include <iostream>
#include <fstream>
#include <sstream>
#include "personapi.h"

using namespace std;

int main()
{
    cout << "Hello World!" << endl;

    std::ifstream file("C:\\C++\\persons.txt");

    std::string line;
    while (std::getline(file, line)){

        std::string word;
        Person person;

        std::stringstream ss(line);
        ss >> person.firstname;
        ss >> person.surname;
        ss >> word;
        person.birthyear = std::stoi(word);

        cout << person.firstname << " " <<
            person.surname << " " <<
            person.birthyear << " " <<
            getPersonCategory(person) << endl;

        savePersonToFile(person);
    }

    return 0;
}