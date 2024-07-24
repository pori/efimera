import React, { useState } from 'react';

const Editor = ({ initialValue, onSave, placeholder }) => {
    const [text, setText] = useState(initialValue);

    const handleSubmit = (e) => {
        e.preventDefault();
        onSave({ text });
        setText('');
    };

    return (
        <form onSubmit={handleSubmit} className="editor-form">
            <textarea
              name="content"
              className="editor-textarea"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder={placeholder}
              required
            />
            <button type="submit" className="editor-button">Save</button>
        </form>
    );
};

export default Editor;
