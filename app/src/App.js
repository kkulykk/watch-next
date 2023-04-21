import { Route, BrowserRouter as Router, Routes, Navigate } from 'react-router-dom';
import { createTheme, NextUIProvider } from '@nextui-org/react';
import { ToastContainer } from 'react-toastify';

import Login from './components/Login/Login';
import Signup from './components/Signup/Signup';
import Feed from './components/Feed/Feed';
import NotFound from './components/NotFound/NotFound';

import 'react-toastify/dist/ReactToastify.css';
import './App.css';

const theme = createTheme({
  type: 'dark',
  theme: {
    colors: {
      primaryLight: '$green200',
      primaryLightHover: '$green300',
      primaryLightActive: '$green400',
      primaryLightContrast: '$green600',
      primary: '#3A1D51',
      violetDark: '#3A1D51',
      inputDark: '#282734',
      primaryBorder: '$green500',
      primaryBorderHover: '$green600',
      primarySolidHover: '$green700',
      primarySolidContrast: '$white',
      primaryShadow: '$green500',
      gradient: 'linear-gradient(112deg, $blue100 -25%, $pink500 -10%, $purple500 80%)'
    },
    space: {},
    fonts: {}
  }
});

function App() {
  return (
    <NextUIProvider theme={theme}>
      <ToastContainer />
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/feed" element={<Feed />} />
          <Route path="/404" element={<NotFound />} />
          <Route path="*" element={<Navigate to="/404" replace />} />
        </Routes>
      </Router>
    </NextUIProvider>
  );
}

export default App;
