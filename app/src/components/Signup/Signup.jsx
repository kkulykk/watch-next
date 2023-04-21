import { useState } from 'react';
import { Input, Spacer, Button, Text, Link, Loading } from '@nextui-org/react';

import { validateSignupInput } from './services';

import styles from './signup.module.css';

const Signup = () => {
  const [isSignUpLoading, setIsSignUpLoading] = useState(false);
  const [userName, setUserName] = useState('');
  const [userAge, setUserAge] = useState('');
  const [userEmail, setUserEmail] = useState('');
  const [userPassword, setUserPassword] = useState('');

  const processSignUp = (userName, userAge, userEmail, userPassword) => {
    setIsSignUpLoading(true);

    if (!validateSignupInput(userName, userAge, userEmail, userPassword)) return setIsSignUpLoading(false);

    console.log('call service function');

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
            type="email"
            label="Full Name"
            placeholder="John Doe"
            width="300px"
            onChange={(e) => setUserName(e.target.value)}
          />
          <Spacer x={0.6} />
          <Input
            css={{ $$inputColor: '#282734' }}
            color="white"
            type="email"
            label="Age"
            placeholder="25"
            width="88px"
            onChange={(e) => setUserAge(e.target.value)}
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
          onPress={() => processSignUp(userName, userAge, userEmail, userPassword)}
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
