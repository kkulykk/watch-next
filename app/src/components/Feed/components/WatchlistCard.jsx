import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import { Text, Card, Button, Row, Col } from '@nextui-org/react';

import WatchlistModal from './WatchlistModal';
import { useState } from 'react';

dayjs.extend(relativeTime);

const WatchlistCard = (props) => {
  const [isWatchlistDetailsModalVisible, setIsWatchlistDetailsModalVisible] = useState(false);

  return (
    <>
      <WatchlistModal
        isVisible={isWatchlistDetailsModalVisible}
        visibilityHandler={setIsWatchlistDetailsModalVisible}
        name={props.name}
        updatedAt={props.updatedAt}
        watchlistId={props.watchlist_id}
      />
      <Card
        onPress={() => setIsWatchlistDetailsModalVisible(true)}
        isPressable
        isHoverable
        css={{ maxWidth: '900px', width: '100%', height: '150px', background: 'rgba(15, 15, 27, 0.75)' }}
      >
        <Card.Body>
          <Text h4 size={32} css={{ margin: '0', marginLeft: '20px', overflowX: 'hidden' }}>
            {props.name}
          </Text>
        </Card.Body>
        <Card.Footer>
          <Row>
            <Col>
              <Text color="gray" css={{ marginLeft: '20px' }}>
                {`Last edited ${dayjs.unix(props.updatedAt).fromNow()}`}
              </Text>
            </Col>
            <Col>
              <Row justify="flex-end">
                <Button flat auto rounded color="error" onPress={() => props.onRemoveButtonHandler(props.watchlist_id)}>
                  <Text color="error" size={12} weight="bold" transform="uppercase">
                    Delete
                  </Text>
                </Button>
              </Row>
            </Col>
          </Row>
        </Card.Footer>
      </Card>
    </>
  );
};

export default WatchlistCard;
