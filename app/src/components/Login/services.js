import { toast } from 'react-toastify';

import { validationErrors, validateEmail } from '../Signup/services';

export const validateLoginInput = (email, password) => {
  if (email === '' && name === '') {
    toast.error(validationErrors.noInformation, {
      position: toast.POSITION.BOTTOM_LEFT,
      theme: 'dark'
    });

    return false;
  } else if (email === '') {
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
