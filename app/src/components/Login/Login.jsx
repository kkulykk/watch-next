import to from 'await-to-js';
import Cookies from 'js-cookie';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input, Spacer, Button, Text, Link, Loading } from '@nextui-org/react';

import { validateLoginInput } from './services';
import { alert, success } from '../alerts';
import { loginUser } from '../Signup/services';

import styles from './login.module.css';

const Login = () => {
  const navigate = useNavigate();
  const [isLoginLoading, setIsLoginLoading] = useState(false);
  const [userName, setUserName] = useState('');
  const [userPassword, setUserPassword] = useState('');

  const loginUserHandler = async (userName, userPassword) => {
    const [err, res] = await to(loginUser(userName, userPassword));

    if (!res.access_token) return alert('Error during login');

    console.log(res);

    Cookies.set('accessToken', res.access_token);

    success('You successfully logged in');

    return navigate('/feed');
  };

  const processLogin = async (userName, userPassword) => {
    setIsLoginLoading(true);

    if (!validateLoginInput(userName, userPassword)) return setIsLoginLoading(false);

    await loginUserHandler(userName, userPassword);

    setIsLoginLoading(false);
  };

  useEffect(() => {
    const token = Cookies.get('accessToken');

    if (token && token !== 'undefined') return navigate('/feed');
  }, []);

  return (
    <div className={styles.background}>
      <div className={styles.container}>
        <div className={styles.loginContainer}>
          <Text h1 size={60} css={{ color: 'white' }} weight="bold">
            Welcome Back
          </Text>
          <Text h3>Sign in to continue your progress</Text>
          <Spacer y={1} />
          <Input
            css={{ $$inputColor: '#282734' }}
            color="white"
            type="text"
            label="Username"
            placeholder="john.doe"
            width="400px"
            onChange={(e) => setUserName(e.target.value)}
          />
          <Spacer y={0.6} />
          <Input.Password
            css={{ $$inputColor: '#282734' }}
            type="password"
            label="Password"
            placeholder="*********"
            width="400px"
            onChange={(e) => setUserPassword(e.target.value)}
          />
          <Spacer y={1} />
          <Button
            onPress={() => processLogin(userName, userPassword)}
            disabled={isLoginLoading}
            css={{ background: '#3A1D51' }}
          >
            {isLoginLoading ? <Loading color="currentColor" size="sm" /> : 'Sign in'}
          </Button>
          <Spacer y={5} />
          <div className={styles.signup}>
            <Text size="$md">Don’t have an account?</Text>
            <Link color="text" css={{ fontWeight: 'bold' }} href="signup">
              Register Here
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
