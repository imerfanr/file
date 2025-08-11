import React, { useEffect, useRef } from 'react';
import NCWindow from './NCWindow';

interface LogViewerProps {
  logs: string[];
  isLoading: boolean;
  error: string | null;
}

export default function LogViewer({ logs, isLoading, error }: LogViewerProps): React.ReactNode {
  const logContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [logs, error]);

  const getLogColor = (log: string) => {
    if (log.includes('[CRITICAL]')) return '#FF5555'; // Bright Red
    if (log.includes('[High]')) return '#FFB86C'; // Orange
    if (log.includes('[Medium]')) return '#F1FA8C'; // Yellow
    if (log.includes('[INFO]')) return '#8BE9FD'; // Cyan
    if (log.includes('Scan complete')) return '#50FA7B'; // Green
    return '#FFFFFF'; // White
  }

  return (
    <NCWindow title="Analysis Log" style={{ flex: 1, minHeight: 0 }}>
      <div
        ref={logContainerRef}
        style={{ flex: 1, overflowY: 'auto', color: 'var(--nc-text-alt)' }}
      >
        {logs.map((log, index) => (
          <p key={index} style={{ margin: 0, color: getLogColor(log), whiteSpace: 'pre-wrap' }}>{log}</p>
        ))}
        {error && <p style={{ margin: 0, color: '#FF5555', whiteSpace: 'pre-wrap' }}>{error}</p>}
        {isLoading && <div style={{ animation: 'blink 1s step-end infinite' }}>_</div>}
      </div>
       <style>{`
        @keyframes blink {
          from, to { opacity: 1 }
          50% { opacity: 0 }
        }
      `}</style>
    </NCWindow>
  );
}
