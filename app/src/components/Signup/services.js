import { toast } from 'react-toastify';
import { checkResponse, userMsUrl } from '../apiUrl';

export const EMAIL_REGEX_EXP = new RegExp(
  // eslint-disable-next-line
  /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i
);

export const validationErrors = {
  noInformation: 'None of the fields are filled in',
  invalidName: 'Invalid name',
  invalidEmail: 'Invalid email address',
  invalidAge: 'Invalid age',
  invalidPassword: 'Invalid password'
};

/**
 * Check if email matches the corresponding regex
 * @param email
 * @returns {boolean}
 */
export const validateEmail = (email) => EMAIL_REGEX_EXP.test(email);

export const validateSignupInput = (name, email, password) => {
  if (email === '' && name === '') {
    toast.error(validationErrors.noInformation, {
      position: toast.POSITION.BOTTOM_LEFT,
      theme: 'dark'
    });

    return false;
  } else if (name === '') {
    toast.error(validationErrors.invalidName, {
      position: toast.POSITION.BOTTOM_LEFT,
      theme: 'dark'
    });

    return false;
  } else if (email === '' || !validateEmail(email)) {
    toast.error(validationErrors.invalidEmail, {
      position: toast.POSITION.BOTTOM_LEFT,
      theme: 'dark'
    });

    return false;
  } else if (password === '' || password.length < 8) {
    toast.error(validationErrors.invalidPassword, {
      position: toast.POSITION.BOTTOM_LEFT,
      theme: 'dark'
    });

    return false;
  }

  return true;
};

export const loginUser = async (username, password) => {
  const url = `${userMsUrl()}/login`;

  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);

  return fetch(url, {
    method: 'POST',
    'Content-Type': 'application/json',
    body: formData
  }).then(checkResponse);
};

export const createUser = async (username, email, password) => {
  const url = `${userMsUrl()}/create`;

  const formData = new FormData();
  formData.append('username', username);
  formData.append('email', email);
  formData.append('password', password);

  return fetch(url, {
    method: 'POST',
    'Content-Type': 'application/json',
    body: formData
  }).then(checkResponse);
};
