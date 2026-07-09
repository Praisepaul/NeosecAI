export interface DashboardStats {
  securityScore: number;

  alerts: {
    critical: number;
    high: number;
    medium: number;
  };

  incidents: {
    open: number;
    investigating: number;
    resolvedToday: number;
  };

  vulnerabilities: {
    critical: number;
    high: number;
    medium: number;
  };

  assets: {
    total: number;
    online: number;
    offline: number;
  };

  threatIntel: {
    newThreats: number;
    exploitedCVEs: number;
  };
}