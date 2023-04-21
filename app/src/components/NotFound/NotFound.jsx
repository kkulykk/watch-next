import { Spacer, Button, Text } from '@nextui-org/react';
import { useNavigate } from 'react-router-dom';

import styles from './not-found.module.css';

const NotFound = () => {
  const navigate = useNavigate();

  return (
    <div className={styles.background}>
      <div className={styles.container}>
        <Text h1 size={60} css={{ color: 'white' }} weight="bold">
          Oops...
        </Text>
        <Text h3>The page you are trying to reach seems to be missing</Text>
        <Spacer y={1} />
        <Button onPress={() => navigate('/feed')} css={{ background: '#3A1D51', width: '200px' }}>
          To feed
        </Button>
        <Spacer y={5} />
      </div>
    </div>
  );
};

export default NotFound;
