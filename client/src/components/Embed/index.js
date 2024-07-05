import React from 'react';

import LinkPreview from "../LinkPreview";

import providers from './providers';

const Embed = (props) => {
    const resolve = () => {
        const provider = providers.find(p => p.tester(props.url));

        if (provider) {
            const Component = provider.component;

            return <Component {...props} />
        }

        const {
            title,
            description,
            image: previewUrl,
            url: linkUrl
        } = props;

        return <LinkPreview title={title} description={description} imageUrl={previewUrl} linkUrl={linkUrl} />;
    };

    return <div className="embed-container">{resolve()}</div>;
};

export default Embed;
