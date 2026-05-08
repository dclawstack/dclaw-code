import type { NextConfig } from "next";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

const nextConfig: NextConfig = {
  output: "standalone",
  images: { unoptimized: true },
  async rewrites() {
    if (!API_BASE) return [];
    return [
      {
        source: "/api/:path*",
        destination: `${API_BASE}/:path*`,
      },
    ];
  },
};

export default nextConfig;
