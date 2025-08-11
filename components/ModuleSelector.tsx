import React from 'react';
import { ScanModule } from '../types';
import NCWindow from './NCWindow';

interface ModuleSelectorProps {
  modules: ScanModule[];
  selectedModules: Set<string>;
  onToggle: (moduleId: string) => void;
}

export default function ModuleSelector({ modules, selectedModules, onToggle }: ModuleSelectorProps): React.ReactNode {
  return (
    <NCWindow title="Detection Modules" style={{ flex: 1, minHeight: 0 }}>
      <div style={{ overflowY: 'auto', flex: 1 }}>
        {modules.map((module) => (
          <div
            key={module.id}
            onClick={() => onToggle(module.id)}
            style={{ 
              cursor: 'pointer', 
              padding: '2px 4px',
              color: selectedModules.has(module.id) ? 'var(--nc-highlight-text)' : 'var(--nc-text-alt)',
              backgroundColor: selectedModules.has(module.id) ? 'var(--nc-highlight-bg)' : 'transparent',
              display: 'flex',
              gap: '0.5rem',
            }}
          >
            <span>{selectedModules.has(module.id) ? '[*]' : '[ ]'}</span>
            <span>{module.name}</span>
          </div>
        ))}
      </div>
    </NCWindow>
  );
}
