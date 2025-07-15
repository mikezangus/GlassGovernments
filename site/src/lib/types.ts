export interface TokenItem {
    token: string;
    states: string[];
};


export interface TokenItemRow {
    token: string;
    state: string;
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


export type TelegramMessage = {
    message_id: number;
    from: {
        id: number;
        is_bot: boolean;
        first_name: string;
        last_name?: string;
        username?: string;
        language_code?: string;
        is_premium?: boolean;
    };
    chat: TelegramMessageChat;
    date: number;
    text?: string;
    entities?: {
        offset: number;
        length: number;
        type: string;
    }[];
};


export type TelegramMessageChat = {
    id: number;
    first_name: string;
    last_name?: string;
    username?: string;
    type: "private" | "group" | "supergroup" | "channel";
}
