import React from "react";

const extractInstagramPostId = (url) => {
    const postIdRegex = /^https:\/\/www\.instagram\.com\/p\/([^\/]+)\/?$/;
    const match = url.match(postIdRegex);
    return match ? match[1] : null;
};

export const isInstagramUrl = (url) => {
    const instagramRegex = /^https:\/\/www\.instagram\.com\/p\/[^\/]+\/?$/;
    return instagramRegex.test(url);
};

export default function Instagram({ url }) {
    return (
        <iframe
            src={`https://www.instagram.com/p/${extractInstagramPostId(url)}/embed`}
            width="400"
            height="480"
            frameBorder="0"
            scrolling="no"
            allowTransparency="true"
            title="Instagram post"
        ></iframe>
    );
}
