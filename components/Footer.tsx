import React from 'react';

interface FooterProps {
    onScan: () => void;
    onSuggest: () => void;
}

export default function Footer({ onScan, onSuggest }: FooterProps): React.ReactNode {
  const footerStyle: React.CSSProperties = {
    display: 'flex',
    backgroundColor: 'var(--nc-highlight-bg)',
    color: 'var(--nc-highlight-text)',
    padding: '2px 0',
    width: '100%',
    justifyContent: 'center',
    fontSize: '16px',
    flexShrink: 0,
    gap: '0.75rem'
  };

  const keyStyle: React.CSSProperties = {
    color: '#000000',
    backgroundColor: '#AAAAAA',
    padding: '0 4px',
  };
  
  const menuItemStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '0.25rem',
  };
  
  const clickableMenuItemStyle: React.CSSProperties = {
      ...menuItemStyle,
      cursor: 'pointer'
  };

  return (
    <footer style={footerStyle}>
        <div style={menuItemStyle}><span style={keyStyle}>1</span>Help</div>
        <div style={menuItemStyle}><span style={keyStyle}>2</span>Menu</div>
        <div style={menuItemStyle}><span style={keyStyle}>3</span>View</div>
        <div style={menuItemStyle}><span style={keyStyle}>4</span>Edit</div>
        <div onClick={onScan} style={clickableMenuItemStyle}><span style={keyStyle}>5</span>Scan</div>
        <div style={menuItemStyle}><span style={keyStyle}>6</span>Move</div>
        <div style={menuItemStyle}><span style={keyStyle}>7</span>Mkdir</div>
        <div onClick={onSuggest} style={clickableMenuItemStyle}><span style={keyStyle}>8</span>Suggest</div>
        <div style={menuItemStyle}><span style={keyStyle}>9</span>PullDn</div>
        <div style={menuItemStyle}><span style={keyStyle}>10</span>Quit</div>
    </footer>
  );
}
