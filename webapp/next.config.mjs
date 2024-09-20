/** @type {import('next').NextConfig} */

const prefix = process.env.NODE_ENV === 'production' ? 'https://world-headlines.github.io/' : ''


const nextConfig = {
    output: 'export',
    assetPrefix: prefix,
    images: {
      remotePatterns: [
        {
          protocol: 'http',
          hostname: '**',
          port: '',
          pathname: '**',
        },
        {
            protocol: 'https',
            hostname: '**',
            port: '',
            pathname: '**',
          },
      ],
    },
};

export default nextConfig;
