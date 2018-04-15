export interface CallbackInterface {
    (error: Error, result?: any) : void;
}

export interface TweetData {
    text: string;
    tweetUrl: string;
}

export interface InstagramData {
    caption: string;
    picture: string;
}

export interface NewsData {
    title: string;
    description: string;
    url: string;
    imageUrl: string;
    source: string;
}