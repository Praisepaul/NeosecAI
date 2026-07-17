from app.assets.asset_models import create_asset

assets = [
    #
    # ------------------------------------------------------------------
    # Windows Engineering Workstation
    # ------------------------------------------------------------------
    #
    create_asset(
        hostname="WIN11-001",
        operating_system="Windows 11 22H2",
        vendor="Microsoft",
        products=[
            "windows",
            "python",
            "github",
            "crowdstrike",
            "jumpcloud",
            "google chrome",
            "visual studio code",
        ],
        packages=[],
        repositories=[],
        cloud=None,
        criticality="HIGH",
        internet_facing=False,
        owner="Engineering",
        tags=["workstation", "developer"],
    ),
    #
    # ------------------------------------------------------------------
    # Ubuntu AI Workstation
    # ------------------------------------------------------------------
    #
    create_asset(
        hostname="UBUNTU-AI-01",
        operating_system="Ubuntu 24.04",
        vendor="Canonical",
        products=["ubuntu", "python", "terraform", "docker", "github", "nvidia cuda"],
        packages=["openssl", "curl", "git"],
        repositories=["github.com/neospaceai/backend"],
        cloud="AWS",
        criticality="HIGH",
        internet_facing=False,
        owner="AI Platform",
        tags=["ai", "developer"],
    ),
    #
    # ------------------------------------------------------------------
    # Ubuntu Production Server
    # ------------------------------------------------------------------
    #
    create_asset(
        hostname="UBUNTU-SRV-01",
        operating_system="Ubuntu 22.04",
        vendor="Canonical",
        products=["ubuntu", "docker", "kubernetes", "nginx"],
        packages=["openssl", "curl"],
        repositories=[],
        cloud="AWS",
        criticality="CRITICAL",
        internet_facing=True,
        owner="Infrastructure",
        tags=["production", "server"],
    ),
    #
    # ------------------------------------------------------------------
    # Oracle HPC Cluster
    # ------------------------------------------------------------------
    #
    create_asset(
        hostname="OCI-HPC-01",
        operating_system="Oracle Linux",
        vendor="Oracle",
        products=["oracle linux", "oracle hpc"],
        packages=[],
        repositories=[],
        cloud="OCI",
        criticality="CRITICAL",
        internet_facing=False,
        owner="AI Infrastructure",
        tags=["hpc", "gpu"],
    ),
    #
    # ------------------------------------------------------------------
    # NVIDIA GB200 AI Machine
    # ------------------------------------------------------------------
    #
    create_asset(
        hostname="GB200-AI-01",
        operating_system="Ubuntu 24.04",
        vendor="NVIDIA",
        products=["gb200", "cuda", "nvidia driver"],
        packages=[],
        repositories=[],
        cloud=None,
        criticality="CRITICAL",
        internet_facing=False,
        owner="AI Research",
        tags=["gpu", "llm"],
    ),
    #
    # ------------------------------------------------------------------
    # AWS Production
    # ------------------------------------------------------------------
    #
    create_asset(
        hostname="AWS-EC2-01",
        operating_system="Amazon Linux",
        vendor="Amazon",
        products=["aws", "terraform", "docker"],
        packages=[],
        repositories=[],
        cloud="AWS",
        criticality="CRITICAL",
        internet_facing=True,
        owner="Cloud",
        tags=["production", "cloud"],
    ),
    #
    # ------------------------------------------------------------------
    # Kubernetes Cluster
    # ------------------------------------------------------------------
    #
    create_asset(
        hostname="K8S-CLUSTER-01",
        operating_system="Ubuntu",
        vendor="CNCF",
        products=["kubernetes", "docker"],
        packages=[],
        repositories=[],
        cloud="AWS",
        criticality="CRITICAL",
        internet_facing=True,
        owner="Platform",
        tags=["kubernetes", "containers"],
    ),
    #
    # ------------------------------------------------------------------
    # Fortinet Firewall
    # ------------------------------------------------------------------
    #
    create_asset(
        hostname="FORTINET-01",
        operating_system="FortiOS",
        vendor="Fortinet",
        products=["fortinet"],
        packages=[],
        repositories=[],
        cloud=None,
        criticality="CRITICAL",
        internet_facing=True,
        owner="Network",
        tags=["firewall", "security"],
    ),
    #
    # ------------------------------------------------------------------
    # macOS Executive Laptop
    # ------------------------------------------------------------------
    #
    create_asset(
        hostname="MAC-001",
        operating_system="macOS 26",
        vendor="Apple",
        products=["macos", "github", "google chrome"],
        packages=[],
        repositories=[],
        cloud=None,
        criticality="MEDIUM",
        internet_facing=False,
        owner="Management",
        tags=["executive"],
    ),
]
