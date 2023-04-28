import to from 'await-to-js';
import { useState, useEffect } from 'react';
import { Button, Text, Loading } from '@nextui-org/react';

import WatchlistCard from './components/WatchlistCard';
import CreateWatchlistModal from './components/CreateWatchlistModal';
import { deleteWatchlist, getWatchlists } from './services/watchlists';
import { alert } from '../alerts';

import styles from './feed.module.css';

const Feed = () => {
  const [userWatchlists, setUserWatchlists] = useState([]);
  const [isCreateWatchlistModalVisible, setIsCreateWatchlistModalVisible] = useState(false);
  const [isFetchingWatchlistLoading, setIsFetchingWatchlistLoading] = useState(false);

  useEffect(() => {
    fetchUserWatchlistsHandler();
  }, []);

  const fetchUserWatchlistsHandler = async () => {
    setIsFetchingWatchlistLoading(true);

    const [err, res] = await to(getWatchlists());

    setIsFetchingWatchlistLoading(false);

    if (err) return alert('Error while fetching watchlists');

    return setUserWatchlists([
      ...res.sort(function (x, y) {
        return y.last_edit_timestamp - x.last_edit_timestamp;
      })
    ]);
  };

  const removeWatchlistHandler = async (watchlistId) => {
    setIsFetchingWatchlistLoading(true);

    const [err] = await to(deleteWatchlist(watchlistId));

    setIsFetchingWatchlistLoading(false);

    if (err) return alert('Error while deleting watchlist');

    return fetchUserWatchlistsHandler();
  };

  return (
    <div className={styles.background}>
      <CreateWatchlistModal
        isVisible={isCreateWatchlistModalVisible}
        visibilityHandler={setIsCreateWatchlistModalVisible}
        fetchUserWatchlistsHandler={fetchUserWatchlistsHandler}
      />
      <Text size="$3xl">Profile</Text>
      <Text h1 size={60} css={{ color: 'white' }} weight="bold">
        Roman Kulyk
      </Text>
      <Text>{`${userWatchlists.length} watchlists`}</Text>
      <Text>54 followers</Text>
      <Text>34 following</Text>
      <div className={styles.watchlistBackground}>
        <div className={styles.watchlistButtons}>
          <Text h3 color="white">
            Watchlists
          </Text>
          <Button onPress={() => setIsCreateWatchlistModalVisible(true)}>Create new watchlist</Button>
        </div>
        <div className={styles.watchlistItems}>
          {isFetchingWatchlistLoading ? (
            <Loading color="currentColor" size="md" />
          ) : (
            userWatchlists.map((watchlist) => {
              return (
                <WatchlistCard
                  {...watchlist}
                  key={watchlist.watchlist_id}
                  name={watchlist.watchlist_name}
                  updatedAt={watchlist.last_edit_timestamp}
                  refetchWatchlistsHandler={fetchUserWatchlistsHandler}
                  onRemoveButtonHandler={removeWatchlistHandler}
                />
              );
            })
          )}
        </div>
      </div>
    </div>
  );
};

export default Feed;
