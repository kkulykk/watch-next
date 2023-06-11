import to from 'await-to-js';
import Cookies from 'js-cookie';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Text, Loading, Container } from '@nextui-org/react';

import WatchlistCard from './components/WatchlistCard';
import CreateWatchlistModal from './components/CreateWatchlistModal';
import NavigationBar from '../NavigationBar/NavigationBar';
import { deleteWatchlist, getWatchlists } from './services/watchlists';
import { alert } from '../alerts';

import styles from './feed.module.css';

const Feed = () => {
  const navigate = useNavigate();
  const [userWatchlists, setUserWatchlists] = useState([]);
  const [isCreateWatchlistModalVisible, setIsCreateWatchlistModalVisible] = useState(false);
  const [isFetchingWatchlistLoading, setIsFetchingWatchlistLoading] = useState(false);

  useEffect(() => {
    const token = Cookies.get('accessToken');

    if (!token || token === 'undefined') {
      Cookies.remove('accessToken');

      return navigate('/login');
    }

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
      <NavigationBar />
      <CreateWatchlistModal
        isVisible={isCreateWatchlistModalVisible}
        visibilityHandler={setIsCreateWatchlistModalVisible}
        fetchUserWatchlistsHandler={fetchUserWatchlistsHandler}
      />
      <div style={{ minHeight: '20vh', margin: '2% 0', marginLeft: '15%' }}>
        <Text h5 size="$3xl">
          Profile
        </Text>
        <Text h1 size={60} css={{ color: 'white', maxWidth: 'fit-content', margin: 0 }} weight="bold">
          john.doe
        </Text>
        <Container display="flex" css={{ gap: '25px', padding: 0 }}>
          <Text>{`${userWatchlists.length} watchlists`}</Text>
          <Text>54 followers</Text>
          <Text>34 following</Text>
        </Container>
      </div>
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
