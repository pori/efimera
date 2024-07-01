import requests_mock

from efimera.extensions import db
from efimera.models import Note, Link, Tag

class Test:

    def test_notes_parsing(self, client):
        with requests_mock.Mocker() as m:
            # Mock the HTTP response for the URL
            m.get('https://example.com', text='<html><head><title>Example Title</title><meta property="og:description" content="Example Description"><meta property="og:image" content="https://example.com/image.jpg"></head></html>')

            # Test data
            data = {
                'text': 'https://example.com #tag1 #tag2'
            }

            # Make a POST request to the /parse endpoint
            response = client.post('/notes', json=data)
            print(response.json)
            assert response.status_code == 200
            assert response.json['message'] == 'Data saved successfully'

            # Check the Note in the database
            note = Note.query.first()
            assert note is not None
            assert note.text == data['text']

            # Check the Link in the database
            link = Link.query.first()
            assert link is not None
            assert link.url == 'https://example.com'
            assert link.title == 'Example Title'
            assert link.description == 'Example Description'
            assert link.image == 'https://example.com/image.jpg'
            assert link.note_id == note.id

            # Check the Tags in the database
            tags = Tag.query.all()
            assert len(tags) == 2
            assert tags[0].tag == '#tag1'
            assert tags[0].note_id == note.id
            assert tags[1].tag == '#tag2'
            assert tags[1].note_id == note.id

    def test_notes_pagination(self, client):
        # Add test data
        note1 = Note(text='Note 1 https://example1.com #tag1')
        note2 = Note(text='Note 2 https://example2.com #tag2')
        note3 = Note(text='Note 3 https://example3.com #tag3')
        db.session.add_all([note1, note2, note3])
        db.session.commit()

        # Add corresponding links and tags
        link1 = Link(url='https://example1.com', note_id=note1.id)
        link2 = Link(url='https://example2.com', note_id=note2.id)
        link3 = Link(url='https://example3.com', note_id=note3.id)
        db.session.add_all([link1, link2, link3])

        tag1 = Tag(tag='#tag1', note_id=note1.id)
        tag2 = Tag(tag='#tag2', note_id=note2.id)
        tag3 = Tag(tag='#tag3', note_id=note3.id)
        db.session.add_all([tag1, tag2, tag3])
        db.session.commit()

        # Make a GET request to the /notes endpoint with pagination
        response = client.get('/notes?page=1&per_page=2')
        assert response.status_code == 200
        data = response.json
        assert len(data['notes']) == 2
        assert data['total'] == 3
        assert data['pages'] == 2
        assert data['current_page'] == 1

    def test_search(self, client):
        # Add test data
        note1 = Note(text='Note 1 https://example1.com #tag1')
        note2 = Note(text='Note 2 https://example2.com #tag2')
        note3 = Note(text='Note 3 https://example3.com #tag3')
        db.session.add_all([note1, note2, note3])
        db.session.commit()

        # Add corresponding links and tags
        link1 = Link(url='https://example1.com', note_id=note1.id)
        link2 = Link(url='https://example2.com', note_id=note2.id)
        link3 = Link(url='https://example3.com', note_id=note3.id)
        db.session.add_all([link1, link2, link3])

        tag1 = Tag(tag='#tag1', note_id=note1.id)
        tag2 = Tag(tag='#tag2', note_id=note2.id)
        tag3 = Tag(tag='#tag3', note_id=note3.id)
        db.session.add_all([tag1, tag2, tag3])
        db.session.commit()

        # Make a GET request to the /notes endpoint with search
        response = client.get('/notes?search=Note 1')
        assert response.status_code == 200
        data = response.json
        assert len(data['notes']) == 1
        assert data['notes'][0]['text'] == 'Note 1 https://example1.com #tag1'
