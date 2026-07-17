import axios from "axios";

export type ApiErrorType =
    | "NETWORK_OFFLINE"
    | "REQUEST_TIMEOUT"
    | "BACKEND_UNREACHABLE"
    | "UNAUTHORIZED"
    | "FORBIDDEN"
    | "NOT_FOUND"
    | "SERVER_ERROR"
    | "API_ERROR"
    | "UNKNOWN";

export interface ClassifiedApiError {
    type: ApiErrorType;
    status?: number;
    message: string;
}

export function classifyApiError(
    error: unknown
): ClassifiedApiError {

    if (!axios.isAxiosError(error)) {
        return {
            type: "UNKNOWN",
            message: "An unexpected error occurred.",
        };
    }

    /*
    |--------------------------------------------------------------------------
    | Request timed out
    |--------------------------------------------------------------------------
    */

    if (error.code === "ECONNABORTED") {
        return {
            type: "REQUEST_TIMEOUT",
            message:
                "The request took too long to complete.",
        };
    }

    /*
    |--------------------------------------------------------------------------
    | No response received
    |--------------------------------------------------------------------------
    */

    if (!error.response) {

        /*
        navigator.onLine tells us whether the device
        believes it has an active network connection.
        */

        if (
            typeof navigator !== "undefined" &&
            !navigator.onLine
        ) {
            return {
                type: "NETWORK_OFFLINE",
                message:
                    "No internet connection detected.",
            };
        }

        /*
        The computer may be connected to Wi-Fi,
        but the API itself could be unreachable.
        */

        return {
            type: "BACKEND_UNREACHABLE",
            message:
                "The security backend could not be reached.",
        };
    }

    /*
    |--------------------------------------------------------------------------
    | HTTP response errors
    |--------------------------------------------------------------------------
    */

    const status =
        error.response.status;

    if (status === 401) {
        return {
            type: "UNAUTHORIZED",
            status,
            message:
                "Authentication is required.",
        };
    }

    if (status === 403) {
        return {
            type: "FORBIDDEN",
            status,
            message:
                "You do not have permission to access this resource.",
        };
    }

    if (status === 404) {
        return {
            type: "NOT_FOUND",
            status,
            message:
                "The requested API endpoint was not found.",
        };
    }

    if (status >= 500) {
        return {
            type: "SERVER_ERROR",
            status,
            message:
                "The security backend encountered an internal error.",
        };
    }

    return {
        type: "API_ERROR",
        status,
        message:
            "The API returned an error.",
    };
}