"use client";

import { useEffect, useMemo, useState } from "react";
import { RefreshCw } from "lucide-react";

import ThreatFilters from "@/components/threat-intelligence/ThreatFilters";
import ThreatTable from "@/components/threat-intelligence/ThreatTable";
import ThreatDetailPanel from "@/components/threat-intelligence/ThreatDetailPanel";
import AppErrorState from "@/components/errors/AppErrorState";
import { Button } from "@/components/ui/button";

import { useThreats } from "@/src/hooks/useThreats";
import { syncThreats } from "@/services/threatService";
import { classifyApiError } from "@/lib/apiError";
import { useThreatDetails } from "@/src/hooks/useThreatDetails";

export default function ThreatIntelPage() {
  const { threats, loading, error, retry } = useThreats();

  const [syncing, setSyncing] = useState(false);
  const [syncMessage, setSyncMessage] = useState<string | null>(null);

  const [kevOnly, setKevOnly] = useState(false);
  const [search, setSearch] = useState("");
  const [severity, setSeverity] = useState("ALL");

  const [selectedCve, setSelectedCve] = useState<string | null>(null);

  const {
    threat: selectedThreat,
    loading: detailLoading,
    error: detailError,
    retry: retryDetails,
  } = useThreatDetails(selectedCve);

  /*
    |--------------------------------------------------------------------------
    | Sorting
    |--------------------------------------------------------------------------
    */

  const [sortColumn, setSortColumn] = useState("severity");

  const [sortDirection, setSortDirection] = useState<"asc" | "desc">("desc");

  /*
    |--------------------------------------------------------------------------
    | Pagination
    |--------------------------------------------------------------------------
    */

  const [currentPage, setCurrentPage] = useState(1);

  const rowsPerPage = 10;

  /*
    |--------------------------------------------------------------------------
    | FILTERING
    |--------------------------------------------------------------------------
    */

  const filteredThreats = useMemo(() => {
    return threats.filter((threat) => {
      const searchValue = search.toLowerCase();

      const matchesSearch =
        threat.cve.toLowerCase().includes(searchValue) ||
        threat.title?.toLowerCase().includes(searchValue) ||
        threat.technology?.products?.some((product) =>
          product.toLowerCase().includes(searchValue),
        ) ||
        threat.technology?.vendors?.some((vendor) =>
          vendor.toLowerCase().includes(searchValue),
        );

      const matchesSeverity =
        severity === "ALL" || threat.cvss?.severity === severity;

      const matchesKev = !kevOnly || threat.kev === true;

      return matchesSearch && matchesSeverity && matchesKev;
    });
  }, [threats, search, severity, kevOnly]);

  /*
    |--------------------------------------------------------------------------
    | SORTING
    |--------------------------------------------------------------------------
    */

  const sortedThreats = useMemo(() => {
    const sorted = [...filteredThreats];

    const severityOrder: Record<string, number> = {
      CRITICAL: 5,
      HIGH: 4,
      MEDIUM: 3,
      LOW: 2,
      UNKNOWN: 1,
    };

    sorted.sort((a, b) => {
      let valueA: string | number;
      let valueB: string | number;

      switch (sortColumn) {
        case "cve":
          valueA = a.cve;
          valueB = b.cve;

          break;

        case "title":
          valueA = a.title || "";
          valueB = b.title || "";

          break;

        case "severity":
          valueA = severityOrder[a.cvss?.severity || "UNKNOWN"] || 0;

          valueB = severityOrder[b.cvss?.severity || "UNKNOWN"] || 0;

          break;

        case "cvss":
          valueA = a.cvss?.score ?? -1;

          valueB = b.cvss?.score ?? -1;

          break;

        case "risk":
          valueA = a.risk_score ?? 0;

          valueB = b.risk_score ?? 0;

          break;

        case "epss":
          valueA = a.epss?.score ?? -1;

          valueB = b.epss?.score ?? -1;

          break;

        case "assets":
          valueA = a.matched_assets?.length ?? 0;

          valueB = b.matched_assets?.length ?? 0;

          break;

        case "published":
          valueA = a.published ? new Date(a.published).getTime() : 0;

          valueB = b.published ? new Date(b.published).getTime() : 0;

          break;

        default:
          valueA = 0;
          valueB = 0;
      }

      let result: number;

      if (typeof valueA === "string" && typeof valueB === "string") {
        result = valueA.localeCompare(valueB);
      } else {
        result = Number(valueA) - Number(valueB);
      }

      return sortDirection === "asc" ? result : -result;
    });

    return sorted;
  }, [filteredThreats, sortColumn, sortDirection]);

  /*
    |--------------------------------------------------------------------------
    | PAGINATION
    |--------------------------------------------------------------------------
    */

  const totalPages = Math.ceil(sortedThreats.length / rowsPerPage);

  const paginatedThreats = useMemo(() => {
    const startIndex = (currentPage - 1) * rowsPerPage;

    return sortedThreats.slice(startIndex, startIndex + rowsPerPage);
  }, [sortedThreats, currentPage]);

  /*
    |--------------------------------------------------------------------------
    | RESET TO PAGE 1
    |--------------------------------------------------------------------------
    */

  useEffect(() => {
    setCurrentPage(1);
  }, [search, severity, kevOnly, sortColumn, sortDirection]);

  /*
    |--------------------------------------------------------------------------
    | SORT HANDLER
    |--------------------------------------------------------------------------
    */

  function handleSort(column: string) {
    if (sortColumn === column) {
      setSortDirection((previous) => (previous === "asc" ? "desc" : "asc"));
    } else {
      setSortColumn(column);

      setSortDirection("desc");
    }
  }

  function handleReset() {
    setSearch("");
    setSeverity("ALL");
    setKevOnly(false);

    setSortColumn("severity");
    setSortDirection("desc");

    setCurrentPage(1);
  }

  /*
    |--------------------------------------------------------------------------
    | SYNC
    |--------------------------------------------------------------------------
    */

  async function handleSync() {
    if (syncing) return;

    setSyncing(true);
    setSyncMessage(null);

    try {
      const result = await syncThreats();

      setSyncMessage(
        `Synced - ${result.downloaded} downloaded, ${result.stored} stored.`,
      );

      // Pull the freshly-synced data into the table.
      await retry();

      setTimeout(() => {
      setSyncMessage(null);
    }, 3000);

    } catch (err) {
      const classified = classifyApiError(err);

      setSyncMessage(`Sync failed: ${classified.message}`);

       setTimeout(() => {
         setSyncMessage(null);
       }, 5000);

    } finally {
      setSyncing(false);
    }
  }

  /*
    |--------------------------------------------------------------------------
    | LOADING
    |--------------------------------------------------------------------------
    */

  if (loading) {
    return <div className="p-6">Loading threat intelligence...</div>;
  }

  /*
    |--------------------------------------------------------------------------
    | ERROR
    |--------------------------------------------------------------------------
    */

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

  /*
    |--------------------------------------------------------------------------
    | PAGE
    |--------------------------------------------------------------------------
    */

  return (
    <div className="relative h-[calc(100vh-4rem)] overflow-hidden">
      {/* Main Threat Intelligence Area */}

      <main className="h-full min-w-0 overflow-hidden p-6">
        <div className="mb-6 flex items-start justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold">Threat Intelligence</h1>

            <p className="text-muted-foreground">
              Monitor vulnerabilities, exploitability, and affected
              technologies.
            </p>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            {syncMessage && (
              <p className="text-sm text-muted-foreground whitespace-nowrap">
                {syncMessage}
              </p>
            )}

            <Button onClick={handleSync} disabled={syncing} className="gap-2">
              <RefreshCw
                className={`h-4 w-4 ${syncing ? "animate-spin" : ""}`}
              />

              {syncing ? "Syncing..." : "Sync Now"}
            </Button>
          </div>
        </div>

        {/* Filters */}

        <div className="mb-4">
          <ThreatFilters
            search={search}
            severity={severity}
            onSearchChange={setSearch}
            onSeverityChange={(value) => setSeverity(value ?? "ALL")}
            kevOnly={kevOnly}
            onKevChange={setKevOnly}
            onReset={handleReset}
          />
        </div>

        {/* Table */}

        <div className="h-[calc(100%-140px)] overflow-hidden rounded-lg border">
          <ThreatTable
            threats={paginatedThreats}
            onSelect={(threat) => setSelectedCve(threat.cve)}
            sortColumn={sortColumn}
            sortDirection={sortDirection}
            onSort={handleSort}
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={setCurrentPage}
            totalThreats={sortedThreats.length}
            rowsPerPage={rowsPerPage}
          />
        </div>
      </main>

      {/* Foreground Overlay */}

      {selectedCve && (
        <div className="absolute inset-0 z-50 flex items-center justify-center">
          <div
            className="absolute inset-0 bg-black/50 backdrop-blur-sm"
            onClick={() => setSelectedCve(null)}
          />

          <div className="relative z-10 h-[90%] w-[90%] max-w-5xl overflow-hidden rounded-xl border bg-background shadow-2xl">
            {detailLoading ? (
              <div className="flex h-full items-center justify-center">
                Loading threat details...
              </div>
            ) : detailError ? (
              <AppErrorState type="api" onRetry={retryDetails} />
            ) : selectedThreat ? (
              <ThreatDetailPanel
                threat={selectedThreat}
                onClose={() => setSelectedCve(null)}
              />
            ) : null}
          </div>
        </div>
      )}
    </div>
  );
}
