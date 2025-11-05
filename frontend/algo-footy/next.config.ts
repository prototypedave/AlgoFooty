import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "static.flashscore.com",
        pathname: "/res/image/data/**",
      },
    ],
  },
};

export default nextConfig;
