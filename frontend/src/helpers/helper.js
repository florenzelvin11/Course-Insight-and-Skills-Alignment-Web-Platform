// File for adding helper function

import { 
    invalidEmailErrorMessage,
    missingFieldsErrorMessage,
    nonMatchingPasswordErrorMessage,
    invalidPasswordErrorMessage, 
    invalidZId,
    invalidFirstName,
    invalidLastName
} from "../constants/constants";
// import { mockServer } from "./mockServer";

const port = require('../config.json').BACKEND_PORT;
export const apiUrl = `http://localhost:${port}`;

export async function apiCall(method, path, data) {
    // ##  The below is for testing purposes ##
    // return mockServer(method, path, data, false);
    try {
        const response = await runFetch(method, path, data);
        return response;
    } catch (error) {          
        return({ 'error': error.message });
    }
}

export async function runFetch (method, path, data) {
    try {
        const response = await fetch(
            `${apiUrl}${path}`,
            getOptions(method, data)
        );
        const responseData = await response.json();
    
        if (!response.ok) {
            throw new Error(`Error: ${responseData.error}`);
        }
    
        return responseData;
    } catch (error) {
        throw new Error(`Error making ${method} request to ${path}: ${error.message}`);
    }
}

export function getOptions(method, data) {
    const userData = getUserData();
    const options = {
        method,
        headers: {
          'Content-Type': 'application/json',
          ...(userData === null ? {} : {Authorization: `Bearer ${userData.token}`}),
        },
        ...(data && {body: JSON.stringify(data)})
    };
    return options;
}

export function setUserData (data) {
    localStorage.setItem("userData", JSON.stringify({...getUserData(), ...data}));
}

export function getUserData() {
    const userData = localStorage.getItem("userData");
    return userData ? JSON.parse(userData) : null;
}

export function clearUserData() {
    localStorage.removeItem("userData");
}

export async function logOut() {
    await apiCall('POST', '/logout');
    clearUserData();
}

export function canAdd() {
    return getUserData()?.userType === 'academic' || getUserData()?.userType ===  'admin';
}

export function isAdmin() {
    return getUserData()?.userType === 'admin';
}

export function getUserType() {
    return getUserData()?.userType;
}

export function getHighestUserType() {
    return getUserData()?.highestUserType;
}

export function setUserType(userType) {
    localStorage.setItem("userData", JSON.stringify({...getUserData(), userType: userType}));
}

export function isValidSignUpData(signUpData) {
    if (!isValidZid(signUpData.zId)) {
        return invalidZId;
    } else if (!isValidName(signUpData.firstName)) {
        return invalidFirstName;
    } else if (!isValidName(signUpData.lastName)) {
        return invalidLastName;
    } else if (!isValidEmail(signUpData.email)) {
        return invalidEmailErrorMessage;
    } else if (!isValidPassword(signUpData.password)) {
        return invalidPasswordErrorMessage;
    } else if (!(signUpData.password === signUpData.confirmedPassword)) {
        return nonMatchingPasswordErrorMessage;
    }  else if (hasEmptyValue(signUpData)) {
        return missingFieldsErrorMessage;
    }
}

export function isValidLoginData(loginData) {
    if (!isValidEmail(loginData.email)) {
        return invalidEmailErrorMessage;
    } else if (hasEmptyValue(loginData)) {
        return missingFieldsErrorMessage;
    }
}

export function isValidPassword(password) {
    return password.length >= 8
}

function isValidZid(zId) {
    const zIdPattern = /^z\d{7}$/;
    return zIdPattern.test(zId);
}

export function isValidName(name) {
    const namePattern = /^[A-Za-z]+$/;
    return namePattern.test(name) && name.length > 0;
}

export function hasEmptyValue(obj) {
    return Object.values(obj).some(value => value === '');
}

//  https://regexr.com/3e48o
export function isValidEmail(email) {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailPattern.test(email);
}

export function isValidCourseCode(email) {
    const emailPattern = /^[A-Z]{4}\d{4}$/;
    return emailPattern.test(email);
}

function isValidYear(year) {
    return year >= 0 && year <= 9999;
}
export function validateCourseData(courseData, skills, knowledge, topics) {
    if (hasEmptyValue(courseData)) {
      return 'All Fields are required.';
    }

    if (!isValidCourseCode(courseData.code)) {
        return 'Enter a valid course code.';
    }

    if (!isValidYear(courseData.year)) {
        return 'Enter a valid year.';
    }

    // Check if there are valid skills, knowledge and topics
    if (!Array.isArray(skills) || !Array.isArray(knowledge) | !Array.isArray(topics)) {
      return 'Topics, Skills and/or knowledge are incorrect.';
    }

    // Check if each skill and knowledge has a name and weight
    for (let item of [...skills, ...knowledge]) {
      if (!item.name || !item.weight) {
        return 'Each skill and knowledge should have a name and a weight.';
      }
    }

    return null;
}

export function validateProjectData(projectData, skills, knowledge, topics) {
    if (hasEmptyValue(projectData)) {
      return 'All Fields are required.';
    }

    // Check if there are valid skills, knowledge and topics
    if (!Array.isArray(skills) || !Array.isArray(topics)|| !Array.isArray(knowledge)) {
      return 'Topics, Skills and/or knowledge are incorrect.';
    }
  
    // Check if each skill and has a name and weight
    for (let item of [...skills]) {
      if (!item.name || !item.weight) {
        return 'Each skill should have a name and a weight.';
      }
    }

     // Check if each knowledge and has a name and weight
     for (let item of [...knowledge]) {
        if (!item.name || !item.weight) {
          return 'Each knowledge should have a name and a weight.';
        }
      }
    return null;
}

export function arrayToObject(arr) {
    let obj = {};
    arr.forEach(item => {
      obj[item.name] = item.weight;
    });
    return obj;
}

export function objectToArray(obj) {
    let arr = [];
    for (let key in obj) {
      arr.push({ name: key, weight: obj[key] });
    }
    return arr;
}

export function transformProjectList(projectList) {
    return projectList.map(project => {
        if (project.knowledge) {
            let sortedKnowledgeKeys = Object.entries(project.knowledge)
                .sort((a, b) => b[1] - a[1])
                .map(entry => entry[0]);
            return {...project, knowledge: sortedKnowledgeKeys};
        }
        return project;
    });
}
