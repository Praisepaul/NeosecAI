"use client";

import { useCallback, useEffect, useState } from "react";

import {
    classifyApiError,
    ApiErrorType,
} from "@/lib/apiError";

import { getDashboard } from "@/services/dashboard";
import { DashboardResponse } from "@/types/dashboard";

export function useDashboard() {
    const [dashboard, setDashboard] =
        useState<DashboardResponse | null>(null);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState<ApiErrorType | null>(null);

    const loadDashboard = useCallback(async () => {
        try {
            setLoading(true);
            setError(null);

            const data =
                await getDashboard();

            setDashboard(data);

        } catch (error) {
            const classifiedError =
                classifyApiError(error);

            console.error(
                "Dashboard API error:",
                classifiedError
            );

            setError(
                classifiedError.type
            );

        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        loadDashboard();
    }, [loadDashboard]);

    return {
        dashboard,
        loading,
        error,
        retry: loadDashboard,
    };
}