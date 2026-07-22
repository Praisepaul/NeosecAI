"use client";

import { useCallback, useEffect, useState } from "react";

import { classifyApiError, ApiErrorType } from "@/lib/apiError";
import { getThreatByCve } from "@/services/threatService";
import { Threat } from "@/types/threat";

export function useThreatDetails(cve: string | null) {
    const [threat, setThreat] = useState<Threat | null>(null);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState<ApiErrorType | null>(null);

    const loadThreat = useCallback(async () => {

        if (!cve) {
    setThreat(null);
    setError(null);
    setLoading(false);
    return;
}

        try {
            setLoading(true);
            setError(null);

            const data = await getThreatByCve(cve);

            setThreat(data);

        } catch (error) {

            const classifiedError = classifyApiError(error);

            console.error(
                "Threat detail API error:",
                classifiedError,
            );

            setError(classifiedError.type);

        } finally {
            setLoading(false);
        }

    }, [cve]);

    useEffect(() => {
        loadThreat();
    }, [loadThreat]);

    return {
        threat,
        loading,
        error,
        retry: loadThreat,
    };
}