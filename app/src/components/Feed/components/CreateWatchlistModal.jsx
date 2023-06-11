import { useState } from 'react';
import to from 'await-to-js';
import { Text, Button, Modal, Loading, Input } from '@nextui-org/react';

import { createWatchlist } from '../services/watchlists';
import { alert } from '../../alerts';

const CreateWatchlistModal = (props) => {
  const { isVisible, visibilityHandler, fetchUserWatchlistsHandler } = props;

  const [watchlistName, setWatchlistName] = useState('');
  const [isWatchlistCreatingLoading, setIsWatchlistCreatingLoading] = useState(false);

  const createNewWatchlistHandler = async (watchlistName) => {
    if (!watchlistName) return alert('Watchlist name cannot be empty');

    setIsWatchlistCreatingLoading(true);

    const [err] = await to(createWatchlist(watchlistName));

    setIsWatchlistCreatingLoading(false);
    closeCreateWatchlistModalHandler();

    if (err) return alert('Error while creating watchlist');

    return fetchUserWatchlistsHandler();
  };

  const closeCreateWatchlistModalHandler = () => {
    setWatchlistName('');
    visibilityHandler(false);
  };

  return (
    <Modal
      closeButton
      aria-labelledby="modal-title"
      open={isVisible}
      onClose={() => closeCreateWatchlistModalHandler()}
    >
      <Modal.Header>
        <Text id="modal-title" size={18}>
          Create new watchlist
        </Text>
      </Modal.Header>
      <Modal.Body>
        <Input
          onChange={(e) => setWatchlistName(e.target.value)}
          clearable
          bordered
          fullWidth
          color="primary"
          size="lg"
          placeholder="Enter watchlist name"
        />
      </Modal.Body>
      <Modal.Footer>
        <Button auto flat color="error" onPress={() => closeCreateWatchlistModalHandler()}>
          Close
        </Button>
        <Button auto onPress={() => createNewWatchlistHandler(watchlistName)}>
          {isWatchlistCreatingLoading ? <Loading color="currentColor" size="sm" /> : 'Create'}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default CreateWatchlistModal;
