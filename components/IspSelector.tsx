import React from 'react';
import { IspBlock } from '../types';
import NCWindow from './NCWindow';

interface IspSelectorProps {
  ispBlocks: IspBlock[];
  onFetch: () => void;
  onSelect: (cidr: string) => void;
  isFetching: boolean;
  isDisabled: boolean;
}

export default function IspSelector({ ispBlocks, onFetch, onSelect, isFetching, isDisabled }: IspSelectorProps): React.ReactNode {
  return (
    <NCWindow title="ISP Network Blocks">
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <button
            type="button"
            onClick={onFetch}
            disabled={isFetching || isDisabled}
        >
            {isFetching ? 'Fetching...' : 'Fetch ISP Blocks'}
        </button>
        <div style={{ maxHeight: '120px', overflowY: 'auto', border: '1px solid var(--nc-border)', padding: '2px'}}>
            {ispBlocks.length === 0 && !isFetching && (
                <div style={{color: 'var(--nc-text)', textAlign: 'center'}}>Select location first</div>
            )}
            {ispBlocks.map((block) => (
                <div 
                    key={block.cidr}
                    onClick={() => onSelect(block.cidr)}
                    style={{
                        cursor: 'pointer',
                        padding: '2px 4px',
                        color: 'var(--nc-text-alt)',
                        backgroundColor: 'transparent',
                        borderBottom: '1px solid #000055'
                    }}
                    onMouseEnter={e => (e.currentTarget.style.backgroundColor = 'var(--nc-highlight-bg)')}
                    onMouseLeave={e => (e.currentTarget.style.backgroundColor = 'transparent')}
                >
                    <div><strong>{block.name}</strong> ({block.description})</div>
                    <div style={{color: 'var(--nc-text)'}}>{block.cidr}</div>
                </div>
            ))}
        </div>
      </div>
    </NCWindow>
  );
}
