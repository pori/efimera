import React from 'react';

const LinkPreview = ({ title, description, imageUrl, linkUrl }) => {
    const getDomain = (url) => {
        try {
            return new URL(url).hostname;
        } catch (e) {
            return url;
        }
    };

    const displayTitle = title || getDomain(linkUrl);
    const displayDescription = description || '';

    return (
        <a href={linkUrl} className="link-preview-card" target="_blank" rel="noopener noreferrer">
            {imageUrl && <img src={imageUrl} alt={displayTitle} className="link-preview-image" />}
            <div className="link-preview-content">
                <h3 className="link-preview-title">{displayTitle}</h3>
                {displayDescription && <p className="link-preview-description">{displayDescription}</p>}
            </div>
        </a>
    );
};

export default LinkPreviewCard;
