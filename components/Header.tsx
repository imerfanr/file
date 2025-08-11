import React from 'react';

export default function Header(): React.ReactNode {
  return (
    <header style={{ 
      backgroundColor: 'var(--nc-highlight-bg)', 
      color: 'var(--nc-highlight-text)',
      textAlign: 'center',
      padding: '2px 0',
      width: '100%',
      fontSize: '20px',
      whiteSpace: 'nowrap',
    }}>
      --[ MinerHunter AI ]-- The Legendary All-in-One Crypto-Miner Detector --
    </header>
  );
}
