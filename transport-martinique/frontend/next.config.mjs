const backendInternalUrl = process.env.BACKEND_INTERNAL_URL || "http://backend:8000";

/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: "/backend/:path*",
        destination: `${backendInternalUrl}/:path*`
      }
    ];
  }
};

export default nextConfig;
