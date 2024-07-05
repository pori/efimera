import React from "react";

export const isImageUrl = (url) => {
    return /\.(jpeg|jpg|gif|png)$/.test(url);
};

export default function Image({ url }) {
    return <img src={url} alt="Rendered content" />;
}