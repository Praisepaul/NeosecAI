export const logger = {
    error(message: string, context?: unknown) {
        if (process.env.NODE_ENV !== "production") {
            console.error(message, context);
        }
    },

    warn(message: string, context?: unknown) {
        if (process.env.NODE_ENV !== "production") {
            console.warn(message, context);
        }
    },

    info(message: string, context?: unknown) {
        if (process.env.NODE_ENV !== "production") {
            console.info(message, context);
        }
    },
};