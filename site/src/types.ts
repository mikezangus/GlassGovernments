export type Step = 1 | 2 | 3;


export type WordAndStates = {
    word: string;
    states: string[];
};


export type WordAndState = {
    word: string;
    state: string;
};


export enum ContactMethod {
    Text = "text",
    Telegram = "telegram",
}


export enum SubmitStatus {
    Idle,
    Loading,
    Success,
    Fail
}


export type TelegramMessage = {
    message_id: number;
    from: {
        id: number;
        is_bot?: boolean;
        first_name?: string;
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
    first_name?: string;
    last_name?: string;
    username?: string;
    type?: "private" | "group" | "supergroup" | "channel";
}


export type NotificationsQueueRow = {
    user_id: string;
    bill_id: string;
    token: string;
    state: string;
    last_pubdate: string;
    sent_at: string | null;
}
