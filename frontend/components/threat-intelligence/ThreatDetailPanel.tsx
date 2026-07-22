"use client";

import {
  X,
  ExternalLink,
  ShieldCheck,
  ShieldAlert,
  ChevronDown,
} from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

import { Button } from "@/components/ui/button";

import { Threat } from "@/types/threat";
import RawJsonViewer from "./RawJsonViewer";

interface Props {
  threat: Threat;
  onClose: () => void;
}

export default function ThreatDetailPanel({ threat, onClose }: Props) {
  const formatDate = (date?: string | null) => {
    if (!date) {
      return "N/A";
    }

    return new Date(date).toLocaleString();
  };

  const formatPercent = (value?: number | null) => {
    if (value === null || value === undefined) {
      return "N/A";
    }

    return `${(value * 100).toFixed(3)}%`;
  };

  const getSeverityClass = (severity?: string | null) => {
    switch (severity?.toUpperCase()) {
      case "CRITICAL":
        return "text-red-600";

      case "HIGH":
        return "text-orange-600";

      case "MEDIUM":
        return "text-yellow-600";

      case "LOW":
        return "text-green-600";

      default:
        return "text-muted-foreground";
    }
  };

  const severity = threat.cvss?.severity?.toUpperCase();

  return (
    <aside className="w-full h-full bg-background">
      <div className="flex h-full flex-col">
        {/* ===================================================== */}
        {/* HEADER */}
        {/* ===================================================== */}

        <div className="flex items-start justify-between border-b p-4">
          <div className="min-w-0">
            <div className="flex items-center gap-2">
              <h2 className="font-semibold">{threat.cve}</h2>

              {threat.matched && (
                <span className="rounded-full bg-green-100 px-2 py-1 text-xs text-green-700 dark:bg-green-900/30 dark:text-green-400">
                  Relevant
                </span>
              )}
            </div>

            <div className="mt-2 flex flex-wrap items-center gap-2 text-sm">
              <span className={`font-semibold ${getSeverityClass(severity)}`}>
                {severity || "UNKNOWN"}
              </span>

              <span className="text-muted-foreground">•</span>

              <span>
                Risk Score: <strong>{threat.risk_score ?? "N/A"}</strong>
              </span>
            </div>
          </div>

          <Button variant="ghost" size="icon" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </div>

        {/* ===================================================== */}
        {/* SCROLLABLE CONTENT */}
        {/* ===================================================== */}

        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {/* ================================================= */}
          {/* RELEVANCE */}
          {/* ================================================= */}

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                {threat.matched ? (
                  <ShieldCheck className="h-5 w-5 text-green-600" />
                ) : (
                  <ShieldAlert className="h-5 w-5 text-muted-foreground" />
                )}
                Relevance
              </CardTitle>
            </CardHeader>

            <CardContent className="space-y-4">
              <div>
                <p className="text-sm text-muted-foreground">Status</p>

                <p className="font-medium">
                  {threat.matched
                    ? "This vulnerability matches your technology inventory."
                    : "No matching technology identified."}
                </p>
              </div>

              {threat.matched_assets?.length ? (
                <div>
                  <p className="mb-2 text-sm text-muted-foreground">
                    Matched Assets
                  </p>

                  <div className="space-y-2">
                    {threat.matched_assets.map((asset, index) => (
                      <div
                        key={`${asset.hostname}-${index}`}
                        className="rounded-lg border p-3"
                      >
                        <div className="flex items-center justify-between">
                          <span className="font-medium">{asset.hostname}</span>

                          <span className="text-sm text-muted-foreground">
                            Criticality: {asset.criticality}
                          </span>
                        </div>

                        {asset.matched_on?.length ? (
                          <p className="mt-1 text-xs text-muted-foreground">
                            Matched on: {asset.matched_on.join(", ")}
                          </p>
                        ) : null}

                        <p className="mt-1 text-xs text-muted-foreground">
                          Internet-facing:{" "}
                          {asset.internet_facing ? "Yes" : "No"}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              ) : null}

              {threat.matched_products?.length ? (
                <div>
                  <p className="mb-2 text-sm text-muted-foreground">
                    Matched Products (technology inventory)
                  </p>

                  <div className="space-y-2">
                    {threat.matched_products.map((product, index) => (
                      <div
                        key={`${product.name}-${index}`}
                        className="rounded-lg border p-3"
                      >
                        <div className="flex items-center justify-between">
                          <span className="font-medium">{product.name}</span>

                          {product.criticality !== undefined ? (
                            <span className="text-sm text-muted-foreground">
                              Criticality: {product.criticality}/5
                            </span>
                          ) : null}
                        </div>

                        {product.aliases?.length ? (
                          <p className="mt-1 text-xs text-muted-foreground">
                            Aliases: {product.aliases.join(", ")}
                          </p>
                        ) : null}

                        <p className="mt-1 text-xs text-muted-foreground">
                          Internet-facing:{" "}
                          {product.internet_facing ? "Yes" : "No"}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              ) : null}
            </CardContent>
          </Card>

          {/* ================================================= */}
          {/* DESCRIPTION */}
          {/* ================================================= */}

          <Card>
            <CardHeader>
              <CardTitle>Description</CardTitle>
            </CardHeader>

            <CardContent>
              <p className="text-sm leading-6 whitespace-pre-wrap">
                {threat.description || "No description available."}
              </p>
            </CardContent>
          </Card>

          {/* ================================================= */}
          {/* RISK & SECURITY METRICS */}
          {/* ================================================= */}

          <Card>
            <CardHeader>
              <CardTitle>Risk & Security Metrics</CardTitle>
            </CardHeader>

            <CardContent className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-muted-foreground">Risk Score</p>

                <p className="text-2xl font-bold">
                  {threat.risk_score ?? "N/A"}
                </p>
              </div>

              <div>
                <p className="text-sm text-muted-foreground">KEV</p>

                <p className="font-semibold">{threat.kev ? "Yes" : "No"}</p>
              </div>

              <div>
                <p className="text-sm text-muted-foreground">CVSS Score</p>

                <p className="font-semibold">{threat.cvss?.score ?? "N/A"}</p>
              </div>

              <div>
                <p className="text-sm text-muted-foreground">CVSS Severity</p>

                <p
                  className={`font-semibold ${getSeverityClass(
                    threat.cvss?.severity,
                  )}`}
                >
                  {threat.cvss?.severity || "UNKNOWN"}
                </p>
              </div>

              <div>
                <p className="text-sm text-muted-foreground">EPSS Score</p>

                <p className="font-semibold">
                  {formatPercent(threat.epss?.score)}
                </p>
              </div>

              <div>
                <p className="text-sm text-muted-foreground">EPSS Percentile</p>

                <p className="font-semibold">
                  {formatPercent(threat.epss?.percentile)}
                </p>
              </div>
            </CardContent>
          </Card>

          {/* ================================================= */}
          {/* CVSS DETAILS */}
          {/* ================================================= */}

          <Card>
            <CardHeader>
              <CardTitle>CVSS Details</CardTitle>
            </CardHeader>

            <CardContent className="space-y-3">
              <div>
                <p className="text-sm text-muted-foreground">Version</p>

                <p>{threat.cvss?.version || "N/A"}</p>
              </div>

              <div>
                <p className="text-sm text-muted-foreground">Vector</p>

                <code className="block break-all rounded bg-muted p-2 text-xs">
                  {threat.cvss?.vector || "N/A"}
                </code>
              </div>
            </CardContent>
          </Card>

          {/* ================================================= */}
          {/* AFFECTED TECHNOLOGY */}
          {/* ================================================= */}

          <Card>
            <CardHeader>
              <CardTitle>Affected Technology</CardTitle>
            </CardHeader>

            <CardContent className="space-y-4">
              <TechnologyList
                title="Vendors"
                values={threat.technology?.vendors}
              />

              <TechnologyList
                title="Products"
                values={threat.technology?.products}
              />

              <TechnologyList
                title="Packages"
                values={threat.technology?.packages}
              />

              <TechnologyList
                title="Repositories"
                values={threat.technology?.repositories}
              />

              <TechnologyList
                title="Ecosystems"
                values={threat.technology?.ecosystems}
              />

              <TechnologyList
                title="Versions"
                values={threat.technology?.versions}
              />
            </CardContent>
          </Card>

          {/* ================================================= */}
          {/* CWE */}
          {/* ================================================= */}

          <Card>
            <CardHeader>
              <CardTitle>Weaknesses</CardTitle>
            </CardHeader>

            <CardContent>
              {threat.cwes?.length ? (
                <div className="flex flex-wrap gap-2">
                  {threat.cwes.map((cwe, index) => (
                    <span
                      key={`${cwe}-${index}`}
                      className="rounded-md border px-2 py-1 text-sm"
                    >
                      {cwe}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">
                  No CWE information available.
                </p>
              )}
            </CardContent>
          </Card>

          {/* ================================================= */}
          {/* KEV DETAILS */}
          {/* ================================================= */}

          {threat.kev && (
            <Card>
              <CardHeader>
                <CardTitle>CISA Known Exploited Vulnerability</CardTitle>
              </CardHeader>

              <CardContent className="space-y-3">
                {threat.kev_details ? (
                  <RawJsonViewer
                    data={threat.kev_details}
                    fileName={`${threat.cve}-kev.json`}
                  />
                ) : (
                  <p className="text-sm text-muted-foreground">
                    This CVE is listed in CISA KEV.
                  </p>
                )}
              </CardContent>
            </Card>
          )}

          {/* ================================================= */}
          {/* TIMELINE */}
          {/* ================================================= */}

          <Card>
            <CardHeader>
              <CardTitle>Timeline</CardTitle>
            </CardHeader>

            <CardContent className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div>
                <p className="text-sm text-muted-foreground">Published</p>

                <p className="text-sm">{formatDate(threat.published)}</p>
              </div>

              <div>
                <p className="text-sm text-muted-foreground">Last Modified</p>

                <p className="text-sm">{formatDate(threat.modified)}</p>
              </div>
            </CardContent>
          </Card>

          {/* ================================================= */}
          {/* REFERENCES */}
          {/* ================================================= */}

          <Card>
            <CardHeader>
              <CardTitle>References</CardTitle>
            </CardHeader>

            <CardContent className="space-y-2">
              {threat.references?.length ? (
                threat.references.map((reference, index) => (
                  <a
                    key={`${reference}-${index}`}
                    href={reference}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-start gap-2 break-all text-sm text-blue-500 hover:underline"
                  >
                    <ExternalLink className="mt-0.5 h-4 w-4 shrink-0" />

                    <span>{reference}</span>
                  </a>
                ))
              ) : (
                <p className="text-sm text-muted-foreground">
                  No references available.
                </p>
              )}
            </CardContent>
          </Card>

          {/* ================================================= */
          /* INTELLIGENCE SOURCES */
          /* ================================================= */}

          <Card>
            <CardHeader>
              <CardTitle>Intelligence Sources</CardTitle>
            </CardHeader>

            <CardContent className="space-y-3">
              <SourceAccordion
                name="NVD"
                available={Boolean(threat.sources?.nvd)}
                data={threat.sources?.nvd}
              />

              <SourceAccordion
                name="GitHub Advisory Database"
                available={Boolean(threat.sources?.github)}
                data={threat.sources?.github}
              />

              <SourceAccordion
                name="CISA KEV"
                available={Boolean(threat.sources?.cisa)}
                data={threat.sources?.cisa}
              />

              <SourceAccordion
                name="EPSS"
                available={Boolean(threat.sources?.epss)}
                data={threat.sources?.epss}
              />
            </CardContent>
          </Card>
        </div>
      </div>
    </aside>
  );
}

/* ========================================================= */
/* HELPER COMPONENTS */
/* ========================================================= */

function TechnologyList({
  title,
  values,
}: {
  title: string;
  values?: string[];
}) {
  return (
    <div>
      <p className="mb-1 text-sm text-muted-foreground">{title}</p>

      {values?.length ? (
        <div className="flex flex-wrap gap-2">
          {values.map((value, index) => (
            <span
              key={`${value}-${index}`}
              className="rounded-md bg-muted px-2 py-1 text-xs"
            >
              {value}
            </span>
          ))}
        </div>
      ) : (
        <p className="text-sm text-muted-foreground">None</p>
      )}
    </div>
  );
}

function SourceAccordion({
  name,
  available,
  data,
}: {
  name: string;
  available: boolean;
  data: unknown;
}) {
  if (!available || !data) {
    return (
      <div className="flex items-center justify-between rounded-md border p-3">
        <span className="text-sm">{name}</span>

        <span className="text-sm text-muted-foreground">Not available</span>
      </div>
    );
  }

  const fileName = `${name.toLowerCase().replaceAll(" ", "-")}.json`;

  return (
    <details className="group overflow-hidden rounded-md border">
      <summary className="flex cursor-pointer list-none items-center justify-between p-3 hover:bg-muted/50">
        <div className="flex items-center gap-3">
          <span className="text-sm font-medium">{name}</span>

          <span className="text-xs text-green-600">Available</span>
        </div>

        <ChevronDown className="h-4 w-4 transition-transform group-open:rotate-180" />
      </summary>

      <div className="border-t bg-muted/30 p-4">
        <RawJsonViewer data={data} fileName={fileName} />
      </div>
    </details>
  );
}