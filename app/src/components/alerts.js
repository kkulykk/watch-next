import { toast } from 'react-toastify';

export const alert = (message = 'Oops, something went wrong') => {
  return toast.error(message, {
    position: toast.POSITION.BOTTOM_LEFT,
    theme: 'dark'
  });
};
