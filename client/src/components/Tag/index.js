import React from 'react';

const Tag = ({ text, url }) => {
    return (
        <a href={url} className="tag">
            {text}
        </a>
    );
};

export default Tag;
