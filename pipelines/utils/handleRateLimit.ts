import log from "./log";


interface RateLimitError extends Error {
    response?: { status: number };
}


export default async function handleRateLimit<T>(
    fetch: () => Promise<T>,
    id: string | null,
    maxAttempts: number,
    rateLimitStatus: number
): Promise<T | []>
{
    let attempt = 0;
    let delay = 10000;
    let status: number | null = null;
    let message: string = "";
    while (attempt <= maxAttempts) {
        try {
            return await fetch();
        } catch (err) {
            const error = err as RateLimitError;
            if (error.response?.status === rateLimitStatus) {
                console.warn(`⏳ ${id} [Attempt ${++attempt}/${maxAttempts}] Trying again in ${delay / 1000}s`);
                await new Promise(resolve => setTimeout(resolve, delay));
                delay *= 2;
            } else {
                status = error.response?.status ?? null;
                message = error.message || error.toString();
                console.warn(`❓ ${id} [${++attempt}/${maxAttempts}] Trying again now. Error:`, message);
            }
        }
    }
    console.error(`${id} Maximum attempts hit. Failed to fetch response.\nError:\n${message}`);
    log(`ID: ${id} | Status: ${status}`);
    return [];
}
