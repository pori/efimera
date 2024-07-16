import React from 'react';
import Markdown from 'react-markdown';

import Tag from '../Tag';
import Card from '../Card';
import Embed from '../Embed';

export default function Content({
    text,
    links,
    tags
}) {
    if (links.length === 1) {
        const [link] = links;

        return <Embed {...link } />
    }

    return (
        <Card>
            <Markdown>{text}</Markdown>
            {links.map(link => {
                return <Embed {...link } />
            })}
            {tags.map(tag => <Tag text={tag.tag} url={`/?search=#${text.tag}`} />)}
        </Card>
    );
}
