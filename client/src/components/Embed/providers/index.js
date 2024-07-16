import Image, { isImageUrl } from './Image';
import Instagram, { isInstagramUrl } from './Instagram';
import YouTube, { isYouTubeUrl } from "./YouTube";

const providers = [
    { tester: isImageUrl, component: Image },
    { tester: isInstagramUrl, component: Instagram },
    { tester: isYouTubeUrl, component: YouTube }
    // TODO: include vendor provided embeds
];

export default providers;
