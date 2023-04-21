import { Text } from '@nextui-org/react';

import styles from './feed.module.css';

const Feed = () => {
  return (
    <div className={styles.background}>
      <Text h1 size={60} css={{ color: 'white' }} weight="bold">
        Feed Page
      </Text>
    </div>
  );
};

export default Feed;
