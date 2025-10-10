// frontend/next.config.js (このHMRポーリング設定が非常に重要です)
/** @type {import('next').NextConfig} */
const nextConfig = {
  // ... 他の Next.js 設定があればここに
  
  // Docker/Windowsでの遅延を解消するためのHMRポーリング設定
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.watchOptions = {
        poll: 1000, // 1秒ごとにチェック
        aggregateTimeout: 300, 
      };
    }
    return config;
  },
};

module.exports = nextConfig;