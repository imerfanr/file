import React from 'react';

interface NCWindowProps {
  title: string;
  children: React.ReactNode;
  style?: React.CSSProperties;
}

export default function NCWindow({ title, children, style }: NCWindowProps): React.ReactNode {
  return (
    <div className="nc-window" style={{ ...style }}>
      <div className="nc-window-title">{title}</div>
      {children}
    </div>
  );
}
