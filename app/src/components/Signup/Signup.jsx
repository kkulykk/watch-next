import to from 'await-to-js';
import Cookies from 'js-cookie';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { Input, Spacer, Button, Text, Link, Loading } from '@nextui-org/react';

import { alert, success } from '../alerts';
import { createUser, validateSignupInput } from './services';

import styles from './signup.module.css';

const Signup = () => {
  const navigate = useNavigate();
  const [isSignUpLoading, setIsSignUpLoading] = useState(false);
  const [userName, setUserName] = useState('');
  const [userEmail, setUserEmail] = useState('');
  const [userPassword, setUserPassword] = useState('');

  const createNewUserHandler = async (userName, userEmail, userPassword) => {
    const [err, res] = await to(createUser(userName, userEmail, userPassword));

    if (!res) return alert('Error while creating user');

    Cookies.set('accessToken', res.access_token);

    success('User successfully registered');

    return navigate('/feed');
  };

  const processSignUp = async (userName, userEmail, userPassword) => {
    setIsSignUpLoading(true);

    if (!validateSignupInput(userName, userEmail, userPassword)) return setIsSignUpLoading(false);

    await createNewUserHandler(userName, userEmail, userPassword);

    setIsSignUpLoading(false);
  };

  return (
    <div className={styles.background}>
      <div className={styles.container}>
        <Text h1 size={60} css={{ color: 'white' }} weight="bold">
          Register
        </Text>
        <Text h3>Begin your journey with us today</Text>
        <Spacer y={1} />
        <div className={styles.signupContainer}>
          <Input
            css={{ $$inputColor: '#282734' }}
            color="white"
            type="text"
            label="Nickname"
            placeholder="john.doe"
            width="300px"
            onChange={(e) => setUserName(e.target.value)}
          />
        </div>
        <Spacer y={0.6} />
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
          onPress={() => processSignUp(userName, userEmail, userPassword)}
          disabled={isSignUpLoading}
          auto
          css={{ background: '#3A1D51', width: '200px' }}
        >
          {isSignUpLoading ? <Loading color="currentColor" size="sm" /> : 'Sign up'}
        </Button>
        <Spacer y={5} />
        <div className={styles.login}>
          <Text size="$md">Already signed up?</Text>
          <Link color="text" css={{ fontWeight: 'bold' }} href="login">
            Login Here
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Signup;
