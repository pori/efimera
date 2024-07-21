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

    const handleSave = ({ text }) => {
        addNote(text);
    };

    const notes = data ? [].concat(...data) : [];
    const isLoadingInitialData = !data && !error;
    const isLoadingMore = isLoadingInitialData || (data && typeof data[size - 1] === "undefined");
    const isEmpty = data?.[0]?.length === 0;
    const isReachingEnd = isEmpty || (data && data[data.length - 1]?.length < 10)

    return (
      <Layout>
        {/*<SearchBar onSearch={handleSearch} />*/}
          <InfiniteScroll
              pageStart={0}
              loadMore={setSize}
              hasMore={!isLoadingMore && !isReachingEnd}
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
