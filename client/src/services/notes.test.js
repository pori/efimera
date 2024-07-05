import nock from 'nock';
import { addNote, getNotes } from './notes';

const API_BASE_URL = 'http://localhost:5000';

describe('notes service', () => {
    afterEach(() => {
        nock.cleanAll();
    });

    test('addNote should add a new note', async () => {
        const text = 'https://example.com #example #note';
        const mockResponse = { text };

        nock(API_BASE_URL)
            .post('/notes', { text })
            .reply(200, mockResponse);

        const response = await addNote(text);
        expect(response).toEqual(mockResponse);
    });

    test('getNotes should fetch paginated notes', async () => {
        const mockResponse = {
            notes: [
                {
                    id: 1,
                    text: 'Note 1',
                    links: [],
                    tags: []
                },
                {
                    id: 2,
                    text: 'Note 2',
                    links: [],
                    tags: []
                }
            ],
            total: 2,
            pages: 1,
            current_page: 1,
            next_page: null,
            prev_page: null
        };

        nock(API_BASE_URL)
            .get('/notes')
            .query({ page: 1, per_page: 10 })
            .reply(200, mockResponse);

        const response = await getNotes(1, 10);
        expect(response).toEqual(mockResponse);
    });
});
