import { useEffect, useState } from 'react';
import to from 'await-to-js';
import { Text, Grid, Button, Modal, Loading, Container } from '@nextui-org/react';

import WatchlistFilmCard from './WatchlistFilmCard';
import { getFilmDetails, getRecommendedFilms, putFilmsToWatchlist } from '../services/watchlists';
import { alert, success } from '../../alerts';

const FilmsModal = (props) => {
  const { isVisible, visibilityHandler, watchlistId, fetchWatchlistFilmsHandler } = props;

  const [isRecommendedFilmsLoading, setIsRecommendedFilmsLoading] = useState(false);
  const [films, setFilms] = useState([]);

  const fetchRecommendedFilmsHandler = async () => {
    setIsRecommendedFilmsLoading(true);

    const [err, res] = await to(getRecommendedFilms());

    setIsRecommendedFilmsLoading(false);

    if (err) return alert('Error while fetching films in watchlists');

    const recommendedFilms = [];

    for (const film of res.recommendations) {
      const [errDetails, filmDetails] = await to(getFilmDetails(film.id));

      if (errDetails) return alert('Error while getting film details');

      console.log(film);

      recommendedFilms.push({
        id: filmDetails.id,
        name: filmDetails.title,
        img: `https://image.tmdb.org/t/p/original/${filmDetails.poster_path}`
      });
    }

    return setFilms(recommendedFilms);
  };

  const addMovieToWatchlistHandler = async (movieId) => {
    console.log(movieId);
    visibilityHandler(false);

    const [err] = await to(putFilmsToWatchlist(watchlistId, movieId));

    if (err) return alert('Error while adding film to watchlist');

    success('Film has been successfully added');

    return await fetchWatchlistFilmsHandler();
  };

  useEffect(() => {
    fetchRecommendedFilmsHandler();
  }, []);

  return (
    <Modal
      scroll
      width="70vw"
      height="70vh"
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
              Choose the film to add
            </Text>
          </Container>
        </Container>
      </Modal.Header>
      <Modal.Body css={{ justifyContent: 'flex-start', margin: '0 3%' }}>
        <Grid.Container gap={2} justify="flex-start" css={{ alignItems: 'center' }}>
          {isRecommendedFilmsLoading ? (
            <Loading css={{ margin: '0 auto' }} color="currentColor" size="md" />
          ) : (
            films.map((film, index) => {
              return (
                <Grid xs={6} sm={3} key={index}>
                  <WatchlistFilmCard
                    hideRemove
                    id={film.id}
                    key={film.id}
                    {...film}
                    onPressHandler={addMovieToWatchlistHandler}
                  />
                </Grid>
              );
            })
          )}
        </Grid.Container>
      </Modal.Body>
    </Modal>
  );
};

export default FilmsModal;
