import { useState, useEffect } from "react";

import { addNote, getNotes } from "./services/notes";

import Layout from './components/Layout';
import Grid from './components/Grid';
import Card from './components/Card';
// import SearchBar from './components/SearchBar';
import Editor from './components/Editor';
import ContentRenderer from "./components/Content";

import './App.css';

const App = () => {
    const [notes, setNotes] = useState([]);

    useEffect(() => {
        getNotes(1).then(setNotes);
    }, [getNotes]);

    // const handleSearch = (query) => {
    //     console.log('Searching for:', query);
    // };

    const handleSave = ({ text }) => {
        addNote(text);
    };

    return (
      <Layout>
        {/*<SearchBar onSearch={handleSearch} />*/}
        <Grid>
            <Card>
                <Editor initialValue="" onSave={handleSave} placeholder="Type here..." />
            </Card>
            {notes.map(note => <ContentRenderer key={note.id} {...note} />)}
        </Grid>
      </Layout>
    );
};

export default App;
