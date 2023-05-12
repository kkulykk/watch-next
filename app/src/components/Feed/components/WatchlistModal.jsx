import { useEffect, useState } from 'react';
import to from 'await-to-js';
import { Text, Grid, Button, Modal, Loading, Container } from '@nextui-org/react';

import WatchlistFilmCard from './WatchlistFilmCard';
import {
  getFilmDetails,
  getWatchlistFilms,
  putFilmsToWatchlist,
  removeFilmFromWatchlist
} from '../services/watchlists';
import { alert } from '../../alerts';

const WatchlistModal = (props) => {
  const { isVisible, visibilityHandler, name, watchlistId } = props;

  const [isWatchlistFilmsLoading, setIsWatchlistFilmsLoading] = useState(false);
  const [films, setFilms] = useState([]);

  const fetchWatchlistFilmsHandler = async () => {
    setIsWatchlistFilmsLoading(true);

    const [err, res] = await to(getWatchlistFilms(watchlistId));

    setIsWatchlistFilmsLoading(false);

    if (err) return alert('Error while fetching films in watchlists');

    const watchlistFilms = [];

    for (const film of res) {
      const [errDetails, filmDetails] = await to(getFilmDetails(film.movie_id));

      if (errDetails) return alert('Error while getting film details');

      watchlistFilms.push({
        id: film.movie_id,
        name: filmDetails.title,
        img: `https://image.tmdb.org/t/p/original/${filmDetails.poster_path}`
      });
    }

    return setFilms(watchlistFilms);
  };

  const addMovieToWatchlistHandler = async () => {
    setIsWatchlistFilmsLoading(true);

    const [err] = await to(putFilmsToWatchlist(watchlistId, '1087066'));

    setIsWatchlistFilmsLoading(false);

    if (err) return alert('Error while adding film t0 watchlists');

    return await fetchWatchlistFilmsHandler();
  };

  const removeFilmFromWatchlistHandler = async (movieId) => {
    setIsWatchlistFilmsLoading(true);

    const [err] = await to(removeFilmFromWatchlist(watchlistId, movieId));

    setIsWatchlistFilmsLoading(false);

    if (err) return alert('Error while removing film from watchlist');

    return await fetchWatchlistFilmsHandler();
  };

  useEffect(() => {
    fetchWatchlistFilmsHandler();
  }, []);

  return (
    <Modal
      scroll
      width="70vw"
      aria-labelledby="modal-title"
      aria-describedby="modal-description"
      open={isVisible}
      css={{ background: 'linear-gradient(180deg, #121212 5%, rgba(9, 4, 70, 0.97) 98.23%)' }}
      onClose={() => visibilityHandler(false)}
    >
      <Modal.Header css={{ justifyContent: 'flex-start', margin: '2% 3%' }}>
        <Container css={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
          <Container
            css={{
              display: 'flex',
              padding: '0',
              alignItems: 'center',
              gap: '35px'
            }}
          >
            <Text
              h1
              size={48}
              weight="bold"
              id="modal-title"
              css={{
                margin: '0'
              }}
            >
              {name}
            </Text>
            <Button auto>Edit</Button>
          </Container>
          <Container
            css={{
              display: 'flex',
              padding: '0',
              alignItems: 'flex-start',
              gap: '25px'
            }}
          >
            <Text color="gray">{films.length === 1 ? `${films.length} movie` : `${films.length} movies`}</Text>
            <Text color="gray">34 likes</Text>
          </Container>
        </Container>
      </Modal.Header>
      <Modal.Body css={{ justifyContent: 'flex-start', margin: '0 3%' }}>
        <Grid.Container gap={2} justify="flex-start" css={{ alignItems: 'center' }}>
          <Grid xs={6} sm={3}>
            <WatchlistFilmCard isCreate onPressHandler={addMovieToWatchlistHandler} />
          </Grid>
          {isWatchlistFilmsLoading ? (
            <Loading css={{ margin: '0 auto' }} color="currentColor" size="md" />
          ) : (
            films.map((film, index) => {
              return (
                <Grid xs={6} sm={3} key={index}>
                  <WatchlistFilmCard key={film.id} {...film} onRemoveHandler={removeFilmFromWatchlistHandler} />
                </Grid>
              );
            })
          )}
        </Grid.Container>
      </Modal.Body>
    </Modal>
  );
};

export default WatchlistModal;
