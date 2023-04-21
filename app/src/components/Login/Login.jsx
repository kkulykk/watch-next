import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input, Spacer, Button, Text, Link, Loading } from '@nextui-org/react';

import { validateLoginInput } from './services';

import styles from './login.module.css';

const Login = () => {
  const navigate = useNavigate();
  const [isLoginLoading, setIsLoginLoading] = useState(false);
  const [userEmail, setUserEmail] = useState('');
  const [userPassword, setUserPassword] = useState('');

  const processLogin = (userEmail, userPassword) => {
    setIsLoginLoading(true);

    if (!validateLoginInput(userEmail, userPassword)) return setIsLoginLoading(false);

    console.log('call service function');

    setIsLoginLoading(false);

    return navigate('/feed');
  };

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
            type="email"
            label="Email"
            placeholder="john.doe@email.com"
            width="400px"
            onChange={(e) => setUserEmail(e.target.value)}
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
            onPress={() => processLogin(userEmail, userPassword)}
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
