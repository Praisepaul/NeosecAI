"use client";

import DashboardCards from "@/components/dashboard/DashboardCards";
import SeverityChart from "@/components/dashboard/SeverityChart";
import VendorChart from "@/components/dashboard/VendorChart";

import { useDashboard } from "@/src/hooks/useDashboard";
import AppErrorState from "@/components/errors/AppErrorState";

export default function DashboardPage() {
    const { dashboard, loading, error, retry } = useDashboard();
    if (loading) {
        return (
            <div className="p-6">
                Loading dashboard...
            </div>
        );
    }

    if (error) {
      let errorType: "network" | "timeout" | "backend" | "api" | "unknown";

      switch (error) {
        case "NETWORK_OFFLINE":
          errorType = "network";
          break;

        case "REQUEST_TIMEOUT":
          errorType = "timeout";
          break;

        case "BACKEND_UNREACHABLE":
          errorType = "backend";
          break;

        case "UNAUTHORIZED":
        case "FORBIDDEN":
        case "NOT_FOUND":
        case "SERVER_ERROR":
        case "API_ERROR":
          errorType = "api";
          break;

        default:
          errorType = "unknown";
      }

      return <AppErrorState type={errorType} onRetry={retry} />;
    }

    if (!dashboard) {
      return <AppErrorState type="unknown" onRetry={retry} />;
    }

    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Security Dashboard</h1>

          <p className="text-muted-foreground">
            Real-time overview of your security posture
          </p>
        </div>

        <DashboardCards summary={dashboard.summary} />

        <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
          <div className="rounded-xl border bg-card p-6">
            <div className="mb-4">
              <h2 className="text-lg font-semibold">Severity Distribution</h2>

              <p className="text-sm text-muted-foreground">
                Current threats by severity
              </p>
            </div>

            <SeverityChart data={dashboard.severity_distribution} />
          </div>

          <div className="rounded-xl border bg-card p-6">
            <div className="mb-4">
              <h2 className="text-lg font-semibold">Top Vendors</h2>

              <p className="text-sm text-muted-foreground">
                Vendors with the most tracked vulnerabilities
              </p>
            </div>

            <VendorChart vendors={dashboard.top_vendors} />
          </div>
        </div>
      </div>
    );
}