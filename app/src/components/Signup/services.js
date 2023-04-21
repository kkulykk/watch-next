import { toast } from 'react-toastify';

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

export const validateSignupInput = (name, age, email, password) => {
  if (email === '' && age === '' && name === '') {
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
  } else if (age === '') {
    toast.error(validationErrors.invalidAge, {
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
