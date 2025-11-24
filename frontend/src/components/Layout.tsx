import React, { FC } from 'react';
interface LayoutProps {
  backgroundImageUrl?: string;
  children: React.ReactNode;
}

const Layout: FC<LayoutProps> = ({ children, backgroundImageUrl }) => {
      const backgroundStyle: React.CSSProperties = backgroundImageUrl 
    ? {
        backgroundImage: `url(${backgroundImageUrl})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        minHeight: '100vh',
        width: '100%',
      }
    : {
        backgroundColor: '#FFFFFF',
        minHeight: '100vh',
        width: '100%',
      };

  return (
    <div style={backgroundStyle}>
      {children}
    </div>
  );
};

export default Layout;