export interface TokenItem {
    token: string;
    states: string[];
};


export enum ContactMethod {
    Text = "text",
    Telegram = "telegram",
}


export enum Step {
    Tokens,
    States,
    Contact
}


export enum SubscriptionStatus {
    Idle,
    Loading,
    Success,
    Fail
}
