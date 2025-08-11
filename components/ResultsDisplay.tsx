import React from 'react';
import { Finding, Severity } from '../types';
import NCWindow from './NCWindow';

const severityColors: Record<Severity, string> = {
  Critical: '#FF5555',
  High: '#FFB86C',
  Medium: '#F1FA8C',
  Low: '#8BE9FD',
  Info: '#FFFFFF',
};

interface ResultsDisplayProps {
  findings: Finding[];
  isLoading: boolean;
}

export default function ResultsDisplay({ findings, isLoading }: ResultsDisplayProps): React.ReactNode {
  return (
    <NCWindow title="Scan Findings" style={{ flex: 1, width: '50%', minHeight: 0 }}>
      <div style={{ flex: 1, overflowY: 'auto' }}>
        {findings.length === 0 && !isLoading && (
          <p style={{ color: 'var(--nc-text)', textAlign: 'center', marginTop: '1rem' }}>
            Awaiting scan results...
          </p>
        )}
        {findings.map((finding) => (
          <div key={finding.id} style={{ marginBottom: '0.75rem', borderBottom: '1px dashed #5555AA', paddingBottom: '0.5rem' }}>
            <p style={{ margin: 0, fontWeight: 'bold' }}>
              <span style={{ color: severityColors[finding.severity] }}>[{finding.severity.toUpperCase()}]</span>
              <span style={{ color: 'var(--nc-text-alt)', marginLeft: '0.5rem' }}>{finding.description}</span>
            </p>
            <p style={{ margin: '2px 0 0 0', color: 'var(--nc-text)' }}>
              Target: {finding.target} | Source: {finding.source}
            </p>
             <p style={{ margin: '4px 0 0 0', color: 'var(--nc-text-alt)', whiteSpace: 'pre-wrap' }}>
              {finding.details}
            </p>
          </div>
        ))}
      </div>
    </NCWindow>
  );
}