"use client";

import { useCallback, useEffect, useState } from "react";
import { classifyApiError, ApiErrorType } from "@/lib/apiError";
import { getThreats } from "@/services/threatService";
import { ThreatSummary } from "@/types/threat";
import { logger } from "../lib/logger";

export function useThreats() {
    const [threats, setThreats] = useState<ThreatSummary[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<ApiErrorType | null>(null);

    const loadThreats = useCallback(async () => {
        try {
            setLoading(true);
            setError(null);

            const data = await getThreats();

            setThreats(data);
        } catch (error) {
            const classifiedError = classifyApiError(error);

            logger.error("Threats API request failed", classifiedError);

            setError(classifiedError.type);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        loadThreats();
    }, [loadThreats]);

    return {
        threats,
        loading,
        error,
        retry: loadThreats,
    };
}
