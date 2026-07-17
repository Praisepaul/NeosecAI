"use client";

import { useEffect, useState } from "react";

import { getDashboard } from "@/services/dashboard";
import { DashboardResponse } from "@/types/dashboard";

export function useDashboard() {
    const [dashboard, setDashboard] =
        useState<DashboardResponse | null>(null);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState<string | null>(null);

    useEffect(() => {
        async function loadDashboard() {
            try {
                const data = await getDashboard();

                setDashboard(data);
            } catch (error) {
                console.error(error);

                setError(
                    "Failed to load dashboard data"
                );
            } finally {
                setLoading(false);
            }
        }

        loadDashboard();
    }, []);

    return {
        dashboard,
        loading,
        error,
    };
}