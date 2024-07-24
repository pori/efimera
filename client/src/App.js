import { mutate } from 'swr';
import useSWRInfinite from "swr/infinite";
import InfiniteScroll from "react-infinite-scroller";

import { addNote, getNotes } from "./services/notes";

import Layout from './components/Layout';
import Grid from './components/Grid';
import Card from './components/Card';
// import SearchBar from './components/SearchBar';
import Editor from './components/Editor';
import ContentRenderer from "./components/Content";

import './App.css';

/**
 *
 * @param url
 * @returns {Promise<any>}
 */
const fetcher = async ([page]) => {
    return await getNotes(page);
};

/**
 *
 * @param pageIndex
 * @param previousPageData
 * @returns {string|null}
 */
const getKey = (pageIndex, previousPageData) => {
    if (previousPageData && !previousPageData.length) return null; // reached the end
    return [pageIndex + 1, 'notes']; // SWR uses 0-based index, and our API uses 1-based index
};

const App = () => {
    const { data, error, size, setSize } = useSWRInfinite(getKey, fetcher);

    // const handleSearch = (query) => {
    //     console.log('Searching for:', query);
    // };

    const handleSave = async ({ text }) => {
        await addNote(text);

        mutate(getKey(0, null));
    };
    
    const notes = data ? [].concat(...data) : [];
    const isLoading = !data && !error
    const isLoadingMore =
        isLoading || (size > 0 && data && !data[size - 1])
    const hasMore = !!(
        data &&
        data[data.length - 1] &&
        data[data.length - 1].length === 12
    )

    return (
      <Layout>
          {/*<SearchBar onSearch={handleSearch} />*/}
          <InfiniteScroll
              pageStart={0}
              loadMore={() => {
                  if (isLoadingMore || !size || !setSize) {
                      return;
                  }

                  setSize(size + 1);
              }}
              hasMore={hasMore}
          >
            <Grid>
                <Card>
                    <Editor initialValue="" onSave={handleSave} placeholder="Type here..." />
                </Card>

                {notes.map(note => <ContentRenderer key={note.id} {...note} />)}
            </Grid>
          </InfiniteScroll>
      </Layout>
    );
};

export default App;
