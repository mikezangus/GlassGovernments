export interface TokenItem {
    token: string;
    states: string[];
};


export enum ContactType {
    Text = "text",
    Telegram = "telegram",
}


export enum Step {
    Tokens,
    States,
    Contact
}


export enum SubscribeStatus {
    Idle,
    Loading,
    Success,
    Fail
}
