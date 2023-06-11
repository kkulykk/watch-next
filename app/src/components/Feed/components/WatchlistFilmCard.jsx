import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import { Text, Card, Button, Row, Col } from '@nextui-org/react';

dayjs.extend(relativeTime);

const WatchlistFilmCard = (props) => {
  const { isCreate, onPressHandler, onRemoveHandler, img, name, id } = props;
  return isCreate ? (
    <Card
      isPressable
      isHoverable
      onPress={() => onPressHandler()}
      css={{
        maxWidth: '200px',
        width: '100%',
        height: '280px',
        justifyContent: 'center',
        alignItems: 'center',
        background: 'rgba(90, 60, 114, 0.45)'
      }}
    >
      <Card.Body>
        <Text size={32} weight="bold">
          +
        </Text>
      </Card.Body>
    </Card>
  ) : (
    <Card isPressable isHoverable css={{ maxWidth: '200px', width: '100%', height: '280px' }}>
      <Card.Header
        css={{
          position: 'absolute',
          zIndex: 1,
          background: 'linear-gradient(black, transparent)'
        }}
      >
        <Col>
          <Text size={12} weight="bold" transform="uppercase" color="#ffffffAA">
            Film
          </Text>
          <Text h4 color="white">
            {name}
          </Text>
        </Col>
      </Card.Header>
      <Card.Footer
        css={{
          position: 'absolute',
          borderTop: '$borderWeights$light solid $gray800',
          bottom: 0,
          zIndex: 1
        }}
      >
        <Row justify="flex-end">
          <Button flat auto rounded color="error" onPress={() => onRemoveHandler(id)}>
            <Text color="error" size={12} weight="bold" transform="uppercase">
              R
            </Text>
          </Button>
        </Row>
      </Card.Footer>
      <Card.Image src={img} width="100%" height={285} objectFit="cover" alt="Card image background" />
    </Card>
  );
};

export default WatchlistFilmCard;
