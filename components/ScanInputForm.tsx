import React from 'react';
import NCWindow from './NCWindow';

interface ScanInputFormProps {
  target: string;
  setTarget: (target: string) => void;
  onScan: () => void;
  isLoading: boolean;
}

export default function ScanInputForm({ target, setTarget, onScan, isLoading }: ScanInputFormProps): React.ReactNode {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!isLoading) {
      onScan();
    }
  };

  return (
    <NCWindow title="Scan Target">
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <div>
          <label htmlFor="target" style={{ color: 'var(--nc-text)' }}>
            IP/CIDR/Hostname:
          </label>
          <input
            id="target"
            type="text"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            disabled={isLoading}
          />
        </div>
        <button
          type="submit"
          disabled={isLoading}
        >
          {isLoading ? 'Scanning...' : '[ F5 Scan ]'}
        </button>
      </form>
    </NCWindow>
  );
}
