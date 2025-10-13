<<<<<<< HEAD:frontend/pages/_app.tsx
import "../styles/globals.css";
import type { AppProps } from "next/app";

export default function MyApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}
=======
import '../styles/global.css';

function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />;
}

export default MyApp;
>>>>>>> origin/main:frontend/src/pages/_app.tsx
