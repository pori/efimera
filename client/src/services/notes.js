const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;;

/**
 * add a note
 *
 * @param text
 * @returns {Promise<void>}
 */
export async function addNote(text) {
    const response = await fetch(`${API_BASE_URL}/notes`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text })
    });
    const data = await response.json();

    return data;
}


/**
 * get notes
 *
 * @param page
 * @param perPage
 * @returns {Promise<any>}
 */
export async function getNotes(page = 1, perPage = 10) {
    const response = await fetch(`${API_BASE_URL}/notes?page=${page}&per_page=${perPage}`);
    const data = await response.json();

    return data.notes;
}
